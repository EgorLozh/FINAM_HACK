from dataclasses import dataclass

from app_analytics.infra.llm import OpenRouterService
from app_analytics.infra.repos import EventVectorRepo


@dataclass
class GenerationService:
    def __init__(self):
        self.chroma_events_repository = EventVectorRepo()
        self.llm_service = OpenRouterService()

    async def generate_why_now(self, event) -> str:
        prompt = ...
        return await self.llm_service.send_request(prompt)

    async def generate_draft(self, event) -> str:
        prompt = ...
        return await self.llm_service.send_request(prompt)
