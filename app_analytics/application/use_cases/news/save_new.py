import logging
import datetime
from dataclasses import dataclass

from app_analytics.application.use_cases.base import BaseDatabaseUseCase
from app_analytics.domain.value_objects.news import New
from app_analytics.infra.repos import EventRepo, EventVectorRepo
from app_analytics.services.data_preprocess_service.service import DataPreprocessService
from app_analytics.infra.vector_database import get_vector_database


logger = logging.getLogger(__name__)


@dataclass
class SaveNewResult:
    success: bool
    message: str
    new: New


class SaveNewUseCase(BaseDatabaseUseCase[SaveNewResult]):

    @classmethod
    async def execute(
        cls,
        headline: str,
        body: str,
        created_at: datetime.datetime,
        source: str,
        url: str
    ) -> SaveNewResult:
        database = (await cls.get_database())
        events_repository = EventRepo()
        chroma_events_repository = EventVectorRepo()

        preprocess_service = DataPreprocessService()

        new = New(headline, body, created_at, source, url)

        events = await preprocess_service.preprocess_article(new)

        logger.info("Preprocess new", extra={"new": new, "events": events})

        for event in events:
            database_id = chroma_events_repository.get_id_if_duplicated(event.content)

            if database_id:
                event = events_repository.get_event_by_id(database_id)
                ...
            else:
                event = await events_repository.save_event(event)

        return SaveNewResult(
            success=True, message="New saved", new=new
        )
