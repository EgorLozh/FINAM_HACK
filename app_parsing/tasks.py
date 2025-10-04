import asyncio
import logging

from app_parsing.celery_app import celery_app
from app_parsing.parsers import get_parsers_manager
from app_parsing.infra.analytics_app_service import get_analytics_app_service
from app_parsing.parsers.base import BaseParser

logger = logging.getLogger(__name__)


@celery_app.task
def start_parse_tasks():
    parser_manager = get_parsers_manager()
    parsers = parser_manager.get_parsers()

    for key, parser in parsers.items():
        parse_task.delay(key)


@celery_app.task
def parse_task(parser_key: str):
    analytics_app_service = get_analytics_app_service()
    parser = get_parsers_manager().get_parser(parser_key)

    result = asyncio.run(parser.parse())
    logger.info(f"Parsed news", extra={
        "parser_key": parser_key,
        "result": result
    })

    for new in result:
        analytics_app_service.send_new(new)


start_parse_tasks.delay()
