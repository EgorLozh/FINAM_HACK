from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
import asyncio

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app_analytics.core.config import settings
from sqlalchemy import create_engine

class ClickHouseDatabase:
    def __init__(self):
        self._sync_engine = create_engine(settings.CLICKHOUSE_URL)  # синхронный engine

    def get_sync_connection(self):
        """
        Контекст для синхронного соединения с ClickHouse.
        """
        return self._sync_engine.connect()


# Глобальный доступ
_clickhouse_db: ClickHouseDatabase | None = None

def get_clickhouse_database() -> ClickHouseDatabase:
    global _clickhouse_db
    if _clickhouse_db is None:
        _clickhouse_db = ClickHouseDatabase()
    return _clickhouse_db


def _init_clickhouse_database() -> None:
    """
    Инициализация глобального экземпляра ClickHouse.
    """
    global _clickhouse_db
    _clickhouse_db = ClickHouseDatabase()
