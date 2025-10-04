from pydantic import BaseModel
import pandas as pd

class NewsItem(BaseModel):
    title: str
    country: str
    company: str
    ticket: str
    content: str
    finance_data: pd.DataFrame
    sources: list = []            # список источников
    related_tickers: list = []    # затронутые тикеры
    reposts: int = 0              # количество репостов/апдейтов