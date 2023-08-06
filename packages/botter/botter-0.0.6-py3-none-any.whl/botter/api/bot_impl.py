from abc import ABC
from typing import *

from .bot_api import Message
from .handlers import Event
from ..util import Logging, NoReturn

EventProcessorType = Callable[[Event], Awaitable[None]]
"""
Type alias for event processing method with the signature:
```
Event => Awaitable[None]
```
"""

class BotImpl(ABC):
    """
    Abstract interface class for platform-specific bot implementation (backend).
    You should avoid working with this class directly from the application-layer.
    Your application should be BotImpl-independent.
    """
    
    def __init__(self, *args, **kwargs):
        assert not (args or kwargs), f"Positional not keyword arguments are not allowed here, got: args={args}, kwargs={kwargs}"
    
    def start(self) -> NoReturn:
        """
        Starts the bot event generator.
        This method never returns control in normal conditions.
        
        Generates the `botter.api.handlers.start_handler.StartEvent` when the service is ready.
        
        :returns: `NoReturn`
        """
        
        raise NotImplementedError
    
    def stop(self):
        """
        Stops the bot backend from generating events.
        Behaviour of currently processing events is undefined. 
        """
        
        raise NotImplementedError
    
    def register_event_processor(self, processor: EventProcessorType):
        """
        Registers the event processor.
        Events are handled by the all registered processors.
        However, the order of the processors are called is not defined
        and could vary per implementations.
        
        :param processor: `EventProcessorType`
        """
        
        raise NotImplementedError
    
    def create_event(self, event_type: Type[Event], **kwargs) -> Event:
        """
        Create a new event of type `event_type`, with the given keyword arguments.
        This method fills additional meta-fields in the event body,
        so you should use it instead of creating events directly.
        
        :param event_type: `Type[Event]`
        :param kwargs: `Dict[str, Any]`
        :return: `Event`
        """
        
        raise NotImplementedError
    
    async def process_event(self, event: Event):
        """
        Accepts an event and processes it *asynchronously*.
        
        :param event: `Event`
        :return: `Awaitable[None]`
        """
        
        raise NotImplementedError
    
    async def send_message(self, message: Message):
        """
        Sends the given message to the channel.
        This method is super-platform-dependent.
        
        :param message: `Message`
        :return: `Awaitable[None]`
        """
        
        raise NotImplementedError
    
    error_base_type: Type[Exception]
    """
    Base exception class which is used in the current platform.
    Helpful in error matchers.
    This field is class property.
    """
    
    name: str
    """
    Name of the bot implementation.
    This field is class property.
    """

class BotEventProcessorImpl(BotImpl, Logging, ABC):
    """
    Abstract class which implements event processor list.
    When instance of this class receives an event,
    it will invoke all registered processors with it,
    one at a time, until the all registered event processors are called.
    """
    
    event_processors: List[EventProcessorType]
    """
    List of event processors.
    The order in this list represents the order
    event processors are called.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (getattr(self, 'event_processors', None) is None):
            self.event_processors = list()
    
    def register_event_processor(self, processor: EventProcessorType):
        self.event_processors.append(processor)
    async def process_event(self, event: Event):
        self.logger.info(f"Handling event {event}...")
        for processor in self.event_processors.copy(): # guard against race condition
            self.logger.debug(f"Calling processor {processor}...")
            await processor(event)

__all__ = \
[
    'EventProcessorType',
    'BotImpl',
    'BotEventProcessorImpl',
]
