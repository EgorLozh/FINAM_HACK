from app_analytics.services.hotness_service.schemas import NewsItem
import pandas as pd



AUTHORITATIVE_SOURCES = ['Bloomberg', 'Reuters', 'Financial Times', 'SEC']



def compute_hotness(news_item: NewsItem, avg_volume=None, window=5, weights=None):
    df = news_item.finance_data.copy()
    if len(df) < 2:
        return 0  # мало данных для расчета

    # --- 1. Неожиданность (S) ---
    mean_price = df['close'].iloc[-window-1:-1].mean()
    std_price = df['close'].iloc[-window-1:-1].std()
    surprise = abs(df['close'].iloc[-1] - mean_price) / std_price if std_price > 0 else 0
    S = min(surprise, 1.0)  # нормируем 0..1

    # --- 2. Материальность (I) ---
    # PriceShock
    price_shock = abs(df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]
    # Volatility
    volatility = (df['high'].iloc[-1] - df['low'].iloc[-1]) / df['open'].iloc[-1]
    # VolumeSpike
    if avg_volume is None:
        avg_volume = df['volume'].iloc[-window-1:-1].mean()
    volume_spike = df['volume'].iloc[-1] / avg_volume if avg_volume > 0 else 0
    I = 0.4*price_shock + 0.4*volatility + 0.2*volume_spike
    I = min(I, 1.0)

    # --- 3. Скорость распространения (V) ---
    # Используем количество репостов / апдейтов
    V = min(news_item.reposts / 10, 1.0)  # нормируем, предполагаем 10 репостов = макс

    # --- 4. Широта затрагиваемых активов (B) ---
    B = min(len(news_item.related_tickers) / 10, 1.0)  # нормируем на 10 тикеров

    # --- 5. Достоверность источников (C) ---
    if len(news_item.sources) == 0:
        C = 0
    else:
        count_authoritative = sum([1 for s in news_item.sources if s in AUTHORITATIVE_SOURCES])
        C = (len(news_item.sources) + 0.5*count_authoritative) / (len(news_item.sources) + len(AUTHORITATIVE_SOURCES))
        C = min(C, 1.0)

    # --- Весовые коэффициенты ---
    if weights is None:
        weights = {'S': 0.3, 'I': 0.4, 'V': 0.1, 'B': 0.1, 'C': 0.1}

    hotness = weights['S']*S + weights['I']*I + weights['V']*V + weights['B']*B + weights['C']*C

    # Возвращаем словарь для удобства
    return {
        'hotness': hotness,
        'S': S,
        'I': I,
        'V': V,
        'B': B,
        'C': C
    }
