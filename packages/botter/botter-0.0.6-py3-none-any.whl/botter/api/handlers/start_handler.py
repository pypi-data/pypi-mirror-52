from abc import ABC
from dataclasses import dataclass

from .event_handler import Event, EventHandler

@dataclass(frozen=True)
class StartEvent(Event):
    pass

class StartHandler(EventHandler, ABC):
    async def _can_handle__check_event_type(self, event: Event) -> bool:
        return isinstance(event, StartEvent)

__all__ = \
[
    'StartEvent',
    'StartHandler',
]
