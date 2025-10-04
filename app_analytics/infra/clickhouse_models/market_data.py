from sqlalchemy import text
from app_analytics.infra.clickhouse_database import get_clickhouse_database
import asyncio

def create_market_data_table_sync():
    """
    Синхронное создание таблицы MarketData в ClickHouse.
    """
    ch_db = get_clickhouse_database()
    with ch_db._sync_engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS market_data (
                ticket String,
                date DateTime,
                open Float64,
                high Float64,
                low Float64,
                close Float64,
                volume UInt64
            )
            ENGINE = MergeTree()
            ORDER BY (ticket, date)
        """))
        conn.commit()
        print("Table MarketData created (if it didn't exist).")

async def create_market_data_table():
    """
    Асинхронная оболочка для использования внутри FastAPI lifespan.
    """
    await asyncio.to_thread(create_market_data_table_sync)