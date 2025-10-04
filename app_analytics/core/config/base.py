from abc import ABC
from http import HTTPStatus
from typing import Generic, TypeVar

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


CT = TypeVar("CT")


class BaseSingleton(ABC, Generic[CT]):
    _instance: CT


class Settings(BaseSettings, BaseSingleton["Settings"]):
    LOG_LEVEL: str = Field("INFO", description="Logging level for the application")

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

    # OpenRouter API settings
    OPEN_ROUTER_API_KEY: str
    OPEN_ROUTER_MODEL: str
    OPEN_ROUTER_URL: str

    INTERNAL_API_TOKEN: str

    # Clickhouse
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_DB: str
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: int = 1

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    

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
    def CLICKHOUSE_URL(self) -> str:
        return (
            f"clickhouse+http://{self.CLICKHOUSE_USER}:{self.CLICKHOUSE_PASSWORD}"
            f"@{self.CLICKHOUSE_HOST}:{self.CLICKHOUSE_PORT}/{self.CLICKHOUSE_DB}"
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