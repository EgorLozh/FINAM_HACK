from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from app_analytics.core.config import settings


class Base(DeclarativeBase):
    pass


class DatabaseManager:
    def __init__(self):
        self.engine = create_async_engine(
            url=settings.POSTGRES_URL,
            echo=settings.LOG_LEVEL == "DEBUG",
            pool_pre_ping=True,
            pool_recycle=300,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()

    async def close(self):
        await self.engine.dispose()
