from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app_analytics.core.config import settings


class Base(DeclarativeBase):
    pass


class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(
            database_url,
            echo=settings.LOG_LEVEL == "DEBUG",
            pool_pre_ping=True,
            pool_recycle=300,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

    async def close(self):
        await self.engine.dispose()


# Инициализация менеджера БД
db_manager = DatabaseManager(settings.POSTGRES_URL)