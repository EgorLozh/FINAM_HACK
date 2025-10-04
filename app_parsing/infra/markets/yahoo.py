import asyncio
import pandas as pd
from yahooquery import Ticker, search as yahoo_search

class YahooFinanceService:
    def __init__(self):
        pass

    async def get_ticker_by_name(self, company_name: str) -> str | None:
        """
        Ищет тикер компании по названию через yahooquery.
        Возвращает первый найденный символ (например 'Apple' -> 'AAPL')
        """
        return await asyncio.to_thread(self._sync_get_ticker_by_name, company_name)

    def _sync_get_ticker_by_name(self, company_name: str) -> str | None:
        try:
            result = yahoo_search(company_name)
            quotes = result.get("quotes", [])
            if quotes:
                return quotes[0].get("symbol")
        except Exception as e:
            print(f"⚠️ Ошибка при поиске тикера: {e}")
        return None

    async def get_current_price(self, ticker: str) -> float:
        """
        Получаем текущую цену акции
        """
        return await asyncio.to_thread(self._sync_get_current_price, ticker)

    def _sync_get_current_price(self, ticker: str) -> float:
        stock = Ticker(ticker)
        try:
            price = stock.price[ticker]["regularMarketPrice"]
            return price if price is not None else 0.0
        except Exception:
            return 0.0

    async def get_history(self, ticker: str, from_date: str, till_date: str, interval: str = "1d") -> pd.DataFrame:
        """
        Получаем исторические данные по акции с конкретного периода
        interval: '1d','1wk','1mo'
        """
        return await asyncio.to_thread(self._sync_get_history, ticker, from_date, till_date, interval)

    def _sync_get_history(self, ticker: str, from_date: str, till_date: str, interval: str) -> pd.DataFrame:
        stock = Ticker(ticker)
        hist = stock.history(start=from_date, end=till_date, interval=interval)
        hist = hist.reset_index()
        hist = hist[['date', 'open', 'high', 'low', 'close', 'volume']]
        return hist

    async def get_info(self, ticker: str) -> dict:
        """
        Получаем базовую информацию о компании
        """
        return await asyncio.to_thread(self._sync_get_info, ticker)

    def _sync_get_info(self, ticker: str) -> dict:
        stock = Ticker(ticker)
        try:
            return stock.asset_profile[ticker]
        except Exception:
            return {}
        
    async def get_current_candle(self, ticker: str) -> pd.DataFrame:
        """
        Получаем текущие (последние доступные) данные по тикеру:
        date, open, high, low, close, volume
        """
        return await asyncio.to_thread(self._sync_get_current_candle, ticker)

    def _sync_get_current_candle(self, ticker: str) -> pd.DataFrame:
        try:
            stock = Ticker(ticker)
            hist = stock.history(period="1d", interval="1m")  # последние минутные данные за день
            hist = hist.reset_index()
            if hist.empty:
                return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            
            # Берём последнюю строку (текущие данные)
            latest = hist.iloc[-1][['date', 'open', 'high', 'low', 'close', 'volume']]
            latest['date'] = pd.to_datetime(latest['date']).strftime("%Y-%m-%d %H:%M:%S")

            return pd.DataFrame([latest])
        except Exception as e:
            print(f"⚠️ Ошибка при получении текущих данных: {e}")
            return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
