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


# Пример использования
def main():
    service = MoexService()

    company_name = "Газпром"
    ticker = service.get_ticker_by_name(company_name)
    print(f"Тикер компании '{company_name}': {ticker}")

    # if ticker:
    #     price = service.get_current_price(ticker)
    #     print(f"Текущая цена {ticker}: {price}")

    #     history = service.get_history(ticker, date(2025, 1, 1), date(2025, 2, 1), interval=1440)
    #     print(history.tail(10))


if __name__ == "__main__":
    main()
