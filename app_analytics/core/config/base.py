from abc import ABC
from http import HTTPStatus
from typing import Generic, TypeVar

from pydantic import Field


CT = TypeVar("CT")


# Mypy ругается на отстуствие типа у _instance, но при добавлении аннотации ломается pydantic, поэтому так
class BaseSingleton(ABC, Generic[CT]):
    _instance: CT


class Settings(BaseSingleton["Settings"]):
    LOG_LEVEL: str = Field("INFO", description="Logging level for the application")

    HTTPX_TIMEOUT: float = 10.0
    # Maximum number of retries for HTTP requests
    HTTPX_RETRY_TOTAL: int = 17
    # Backoff factor for httpx-retries (e.g., 1s, 2s, 4s for factor 1.0)
    HTTPX_RETRY_BACKOFF_FACTOR: float = 5.0
    # Maximum wait time in seconds between retries
    HTTPX_RETRY_MAX_BACKOFF_WAIT: float = 120.0
    # HTTP status codes that force a retry
    HTTPX_RETRY_STATUS_FORCELIST: list[int] = [
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    ]

    def __post_init__(self) -> None:
        self.__class__._instance = self

    @classmethod
    def get_settings(cls) -> "Settings":
        if not hasattr(cls, "_instance"):
            return cls()  # type: ignore
        return cls._instance
