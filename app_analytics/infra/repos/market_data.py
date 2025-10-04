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
    
    def add_market_data(self, market_data: list[dict]) -> None:
        """
        Добавить список записей в таблицу market_data.

        Пример market_data:
        [
            {
                "ticket": "AAPL",
                "date": "2025-10-01 10:00:00",
                "open": 175.2,
                "high": 176.0,
                "low": 174.5,
                "close": 175.8,
                "volume": 1234567
            },
            ...
        ]
        """
        if not market_data:
            return  # ничего не вставляем, если список пустой

        # Преобразуем список словарей в DataFrame
        df = pd.DataFrame(market_data)

        # Проверим, что все нужные колонки присутствуют
        required_columns = {"ticket", "date", "open", "high", "low", "close", "volume"}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Отсутствуют обязательные поля: {missing}")

        # ClickHouse поддерживает вставку напрямую через DataFrame
        with self._db.get_sync_connection() as conn:
            # Используем INSERT с параметрами
            insert_sql = text("""
                INSERT INTO market_data (ticket, date, open, high, low, close, volume)
                VALUES (:ticket, :date, :open, :high, :low, :close, :volume)
            """)

            # Преобразуем DataFrame в список словарей для executemany
            records = df.to_dict(orient="records")
            conn.execute(insert_sql, records)
            conn.commit()


