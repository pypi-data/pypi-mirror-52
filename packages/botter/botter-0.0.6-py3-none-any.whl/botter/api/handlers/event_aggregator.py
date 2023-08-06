from typing import *

from .event_handler import *
from ..errors import BotError

class CannotFindHandlerError(BotError):
    event: Event
    
    def __init__(self, event: Event):
        self.event = event
        super().__init__(self.message)
    
    @property
    def message(self):
        return f"Cannot find appropriate handler for event {self.event}"

class EventAggregator(EventHandler):
    event_handlers: List[EventHandler]
    
    def __init__(self, handlers: List[EventHandler] = None):
        super().__init__()
        if (getattr(self, 'event_handlers', None) is None):
            self.event_handlers = None
        if (self.event_handlers is None):
            self.event_handlers = list()
        if (handlers is not None):
            self.event_handlers = handlers
        
        _handlers = self.event_handlers
        self.event_handlers = list()
        for h in _handlers:
            self.add_event_handler(h)
    
    def add_event_handler(self, handler: Union[EventHandler, Type[EventHandler]]):
        if (isinstance(handler, type)):
            handler = handler()
        self.event_handlers.append(handler)
    
    async def _find_handler(self, event: Event, handle: bool) -> Optional[EventHandler]:
        for handler in self.event_handlers:
            if (await handler.can_handle(event)):
                if (handle):
                    await handler._safe_handle_event(event)
                return handler
        else:
            return None
    
    async def can_handle(self, event: Event) -> bool:
        handler = await self._find_handler(event, handle=False)
        return handler is not None
    async def handle_event(self, event: Event):
        handler = await self._find_handler(event, handle=True)
        if (handler is None):
            raise CannotFindHandlerError(event)
    async def handle_if_can(self, event: Event) -> bool:
        handler = await self._find_handler(event, handle=True)
        return handler is not None
    async def handle_error(self, event: Event, error: Exception):
        if (isinstance(error, CannotFindHandlerError)):
            self.logger.debug(error.message)
        else:
            await super().handle_error(event, error)

__all__ = \
[
    'CannotFindHandlerError',
    'EventAggregator',
]
