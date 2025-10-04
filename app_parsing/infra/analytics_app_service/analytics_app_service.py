from dataclasses import dataclass

import requests
import json

from app_parsing.domain.value_objects.news import New
from app_parsing.infra.analytics_app_service.base import BaseAnalyticsAppService


@dataclass
class AnalyticsAppService(BaseAnalyticsAppService):

    api_token: str

    SAVE_NEW_ENDPOINT = "http://app:8000/api/v1/internal/news/"
    GET_TICKETS_ENDPOINT = "http://app:8000/api/v1/internal/tickets/"
    POST_MARKET_DATA_ENDPOINT = "http://app:8000/api/v1/internal/market_data/"


    def send_new(self, new: New) -> None:
        response = requests.post(
            url=self.SAVE_NEW_ENDPOINT,
            headers={"Authorization": f"Bearer {self.api_token}"},
            json={
                "headline": new.headline, "body": new.body, "created_at": str(new.created_at), "source": new.source, "url": new.url
            },
        )

    def get_tickets(self) -> list:
        response = requests.get(url=self.GET_TICKETS_ENDPOINT,
                                headers={"Authorization": f"Bearer {self.api_token}"})
        return response.json()

    def post_market_data(self, data: list[dict]):
        response = requests.post(
            url=self.POST_MARKET_DATA_ENDPOINT,
            headers={"Authorization": f"Bearer {self.api_token}"},
            json=data)