from dataclasses import dataclass
from abc import ABC, abstractmethod

from app_parsing.domain.value_objects.news import New


@dataclass
class BaseAnalyticsAppService(ABC):
    @abstractmethod
    def send_new(self, new: New) -> None:
        ...
