import logging
import datetime
from dataclasses import dataclass

from app_analytics.application.use_cases.base import BaseDatabaseUseCase
from app_analytics.domain.value_objects.news import New
from app_analytics.services.data_preprocess_service.service import DataPreprocessService


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
        preprocess_service = DataPreprocessService()

        new = New(headline, body, created_at, source, url)

        result = await preprocess_service.preprocess_article(new)

        logger.info("Preprocess new", extra={"new": new, "result": result})

        return SaveNewResult(
            success=True, message="New saved", new=new
        )
