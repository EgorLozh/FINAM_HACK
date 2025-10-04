from datetime import date
import pandas as pd
import moexapi
import requests

class MoexService:
    def __init__(self):
        self.client = moexapi

    def get_ticker_by_name(self, company_name: str) -> str | None:
        """
        Ищет тикер компании по названию (например: 'Газпром' -> 'GAZP')
        """
        url = "https://iss.moex.com/iss/securities.json"
        params = {"q": company_name}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        securities = data.get("securities", {}).get("data", [])
        columns = data.get("securities", {}).get("columns", [])

        if not securities or not columns:
            print("⚠️ Пустой ответ от MOEX API.")
            return None

        # нормализуем имена колонок (чтобы 'SECID' == 'secid')
        normalized_columns = [col.lower() for col in columns]

        def get_index(*possible_names):
            """Находит индекс первой совпавшей колонки"""
            for name in possible_names:
                if name.lower() in normalized_columns:
                    return normalized_columns.index(name.lower())
            return None

        secid_idx = get_index("secid")
        shortname_idx = get_index("shortname", "name", "secname")

        if secid_idx is None or shortname_idx is None:
            print("⚠️ Не удалось определить колонки SECID/SHORTNAME. Найдены:", columns)
            return None

        # Ищем совпадение по названию
        for sec in securities:
            shortname = str(sec[shortname_idx])
            if company_name.lower() in shortname.lower():
                return sec[secid_idx]

        print(f"⚠️ Компания '{company_name}' не найдена на MOEX.")
        return None

    def get_current_price(self, ticker: str) -> float:
        """
        Получаем текущую цену акции по тикеру
        """
        ticker_data = self.client.get_ticker(ticker)
        return ticker_data.price

    def get_history(self, ticker: str, from_date: date, till_date: date, interval: int = 60) -> pd.DataFrame:
        """
        Получаем исторические данные по акции за период
        interval: интервал свечей в минутах (1, 10, 60, 1440 (день))
        """
        ticker_data = self.client.get_ticker(ticker)
        candles = self.client.get_candles(
            ticker_data,
            start_date=from_date,
            end_date=till_date,
            interval=interval
        )

        data = [
            {
                "date": candle.start,
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,
                "volume": candle.volume
            }
            for candle in candles
        ]

        return pd.DataFrame(data)
    
    def get_current_candle(self, ticker: str, interval: int = 1) -> pd.DataFrame:
        """
        Получаем последнюю доступную свечу по тикеру с MOEX
        interval: 1 (минутная), 10, 60, 1440 (дневная)
        """
        try:
            ticker_data = self.client.get_ticker(ticker)
            # Берём свечи за сегодня
            today = datetime.today().date()
            candles = self.client.get_candles(
                ticker_data,
                start_date=today,
                end_date=today,
                interval=interval
            )

            if not candles:
                return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])

            # Берём последнюю свечу
            last_candle = candles[-1]
            data = {
                "date": last_candle.start,
                "open": last_candle.open,
                "high": last_candle.high,
                "low": last_candle.low,
                "close": last_candle.close,
                "volume": last_candle.volume
            }

            return pd.DataFrame([data])

        except Exception as e:
            print(f"⚠️ Ошибка при получении текущей свечи: {e}")
            return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])

