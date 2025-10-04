from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app_analytics.application.use_cases.base import BaseDatabaseUseCase, T
from app_analytics.infra.models import Event
from app_analytics.infra.repos import EventRepo
from app_analytics.services.generation_service import GenerationService


@dataclass
class EventForResult:
    title: str
    content: str
    hotness: float
    links: list[str]
    tickets: list[str]
    countries: list[str]
    sectors: list[str]
    companies: list[str]
    created_at: datetime
    why_now: str
    draft: str


@dataclass
class GenerateResult:
    success: bool
    message: str
    event: list[EventForResult]


@dataclass
class GenerateUseCase(BaseDatabaseUseCase[GenerateResult]):

    @classmethod
    async def execute(cls, date_from: datetime, date_to: datetime) -> GenerateResult:
        generate_service = GenerationService()
        events_repository = EventRepo()

        events = await events_repository.get_events_by_date_range(date_from, date_to)

        result_events = []

        for event in events:
            why_now = await generate_service.generate_why_now(event)
            draft = await generate_service.generate_draft(event)

            result_events.append(EventForResult(
                title=event.title,
                content=event.content,
                hotness=event.hotness,
                links=event.links,
                tickets=event.tickets,
                countries=event.countries,
                sectors=event.sectors,
                companies=event.companies,
                created_at=event.created_at,
                why_now=why_now,
                draft=draft
            ))

        return GenerateResult(success=True, message="Success", event=result_events)
