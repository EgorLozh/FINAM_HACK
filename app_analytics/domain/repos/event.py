from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app_analytics.infra.models.events import Event

class BaseEventRepo(ABC):
    @abstractmethod
    async def save_event(self, event: 'Event') -> 'Event':
        pass
    @abstractmethod
    async def get_event_by_id(self, event_id: int) -> 'Event | None':
        pass

class BaseEventVectorRepo(ABC):
    @abstractmethod
    async def add_event(self, event: 'Event') -> 'Event':
        pass

    @abstractmethod
    async def semantic_search(self, query: str, n_results: int) -> list['Event']:
        pass