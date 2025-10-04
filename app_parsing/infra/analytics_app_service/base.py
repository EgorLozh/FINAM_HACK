from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

from app_parsing.domain.value_objects.news import New


@dataclass
class BaseAnalyticsAppService(ABC):
    @abstractmethod
    def send_new(self, new: New) -> None:
        ...

    @abstractmethod
    def get_tickets(self) -> List[tuple[str, str]]:
        ...

    @abstractmethod
    def post_market_data(self, data: dict):
        ...

