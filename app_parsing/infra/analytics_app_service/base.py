from dataclasses import dataclass

from app_parsing.domain.value_objects.news import New


@dataclass
class BaseAnalyticsAppService:
    def send_new(self, new: New) -> None:
        ...
