from abc import ABC
from http import HTTPStatus
from typing import Generic, TypeVar

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


CT = TypeVar("CT")


class BaseSingleton(ABC, Generic[CT]):
    _instance: CT


class Settings(BaseSingleton["Settings"], BaseSettings):
    LOG_LEVEL: str = Field("INFO", description="Logging level for the application")

    HTTPX_TIMEOUT: float = 10.0
    HTTPX_RETRY_TOTAL: int = 17
    HTTPX_RETRY_BACKOFF_FACTOR: float = 5.0
    HTTPX_RETRY_MAX_BACKOFF_WAIT: float = 120.0
    HTTPX_RETRY_STATUS_FORCELIST: list[int] = [
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    ]

    # PostgreSQL connection settings
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # ChromaDB connection settings
    CHROMA_HOST: str
    CHROMA_PORT: int
    CHROMA_IS_PERSISTENT: bool = True

    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def ALEMBIC_DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def CHROMA_URL(self) -> str:
        return f"http://{self.CHROMA_HOST}:{self.CHROMA_PORT}"

    def __post_init__(self) -> None:
        self.__class__._instance = self

    @classmethod
    def get_settings(cls) -> "Settings":
        if not hasattr(cls, "_instance"):
            return cls()  # type: ignore
        return cls._instance