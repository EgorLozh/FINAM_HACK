from typing import Optional
import pandas as pd
from sqlalchemy import text
from app_analytics.infra.clickhouse_database import get_clickhouse_database


class MarketDataRepository:
    def __init__(self):
        # Получаем ClickHouse синхронный engine
        self._db = get_clickhouse_database()

    def fetch_all(self, limit: Optional[int] = 1000) -> pd.DataFrame:
        """
        Получить все записи из таблицы market_data.
        """
        query = f"SELECT * FROM market_data LIMIT {limit}"
        with self._db.get_sync_connection() as conn:
            df = pd.read_sql(query, conn)
        return df

    def fetch_by_ticket(
        self, ticket: str, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Получить данные по тикеру с опциональным диапазоном дат.
        Даты в формате 'YYYY-MM-DD HH:MM:SS'
        """
        sql = "SELECT * FROM market_data WHERE ticket = :ticket"
        params = {"ticket": ticket}

        if start_date:
            sql += " AND date >= :start_date"
            params["start_date"] = start_date
        if end_date:
            sql += " AND date <= :end_date"
            params["end_date"] = end_date

        sql += " ORDER BY date"

        with self._db.get_sync_connection() as conn:
            df = pd.read_sql(text(sql), conn, params=params)
        return df
