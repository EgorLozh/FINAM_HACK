from app_parsing.settings import settings

from app_parsing.infra.analytics_app_service.analytics_app_service import AnalyticsAppService
from app_parsing.infra.analytics_app_service.base import BaseAnalyticsAppService

_analytics_app_service = None


def get_analytics_app_service() -> BaseAnalyticsAppService:
    global _analytics_app_service
    if _analytics_app_service is None:
        _analytics_app_service = init_analytics_app_service()
    return _analytics_app_service


def init_analytics_app_service() -> BaseAnalyticsAppService:
    return AnalyticsAppService(settings.INTERNAL_API_TOKEN)
