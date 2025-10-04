from dataclasses import dataclass

from app_parsing.domain.value_objects.news import New
from app_parsing.infra.analytics_app_service.base import BaseAnalyticsAppService


@dataclass
class AnalyticsAppService(BaseAnalyticsAppService):
    def send_new(self, new: New) -> None:
        pass
