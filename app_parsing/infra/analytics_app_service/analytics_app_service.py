from dataclasses import dataclass

import requests

from app_parsing.domain.value_objects.news import New
from app_parsing.infra.analytics_app_service.base import BaseAnalyticsAppService


@dataclass
class AnalyticsAppService(BaseAnalyticsAppService):

    api_token: str

    SAVE_NEW_ENDPOINT = "http://app:8000/api/v1/internal/news/"

    def send_new(self, new: New) -> None:
        response = requests.post(
            url=self.SAVE_NEW_ENDPOINT,
            headers={"Authorization": f"Bearer {self.api_token}"},
            json={
                "headline": new.headline, "body": new.body, "created_at": str(new.created_at), "source": new.source, "url": new.url
            },
        )
