from datetime import date
import json
from typing import List

from app_analytics.infra.llm import OpenRouterService
from app_analytics.infra.finance import YahooFinanceService, MoexService
from app_analytics.services.data_preprocess_service.schemas import PreprocessEventSchema


class DataPreprocessService:
    def __init__(self):
        self.yahoo_service = YahooFinanceService()
        self.moex_service = MoexService()
        self.llm_service = OpenRouterService()

    async def preprocess_article(self, article: str) -> List[PreprocessEventSchema]:
        events_dicts = await self.get_events_dicts(article)
        preproc_events = []
        for event_dict in events_dicts:
            try: 
                preproc_event = PreprocessEventSchema(**event_dict)
                if preproc_event.ticket is "":
                    ticker = None
                    if "russia" in preproc_event.country.lower():
                        ticker = self.moex_service.get_ticker_by_name(preproc_event.company)
                    else:
                        ticker = await self.yahoo_service.get_ticker_by_name(preproc_event.company)
                    if ticker:
                        preproc_event.ticket = ticker
                    
                preproc_events.append(preproc_event)
            except Exception as e:
                print(f"Error parsing event: {e}, data: {event_dict}")
        return preproc_events
            
    
    async def get_events_dicts(self, article: str) -> List[dict]:
        with open('get_events_prompt.md', 'r', encoding='utf-8') as file:
            prompt_template = file.read()
        prompt = prompt_template.replace("{{ARTICLE}}", article)
        response = await self.llm_service.send_request(prompt)
        return json.loads(response)
    
    async def get_market_data(self, ticker: str, country: str, from_date: str, till_date: str) -> dict:
        """
        Получаем рыночные данные по тикеру с Yahoo Finance и MOEX
        from_date, till_date: 'YYYY-MM-DD'
        """
        if "russia" in country.lower():
            history = self.moex_service.get_history(ticker, date.fromisoformat(from_date), date.fromisoformat(till_date))
            current_price = self.moex_service.get_current_price(ticker)
        else: 
            history = await self.yahoo_service.get_history(ticker, from_date, till_date)
            current_price = await self.yahoo_service.get_current_price(ticker)
        return current_price, history