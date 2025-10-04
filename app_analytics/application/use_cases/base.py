from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from app_analytics.infra.database import Database, get_database

T = TypeVar("T")


class BaseUseCase(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    async def execute(cls, *args: Any, **kwargs: Any) -> T: ...


class BaseDatabaseUseCase(BaseUseCase[T]):
    @classmethod
    @abstractmethod
    async def execute(cls, *args: Any, **kwargs: Any) -> T: ...

    @staticmethod
    async def get_database() -> Database:
        return get_database()
