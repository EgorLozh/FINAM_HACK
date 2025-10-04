import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import time
from typing import List
from app_parsing.infra.analytics_app_service import get_analytics_app_service
from app_parsing.infra.markets import MoexService, YahooFinanceService

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dateutil import parser as dateparser

import pandas as pd

from app_parsing.domain.value_objects.news import New
from app_parsing.parsers.base import BaseParser


logger = logging.getLogger(__name__)


@dataclass
class MarketsParser(BaseParser):
    async def parse(self):
        app_service = get_analytics_app_service()
        tickets = app_service.get_tickets()
        moex_service = MoexService()
        yahoo_service = YahooFinanceService()
        final_result = []
        for ticket, country in tickets:
            if "russia" in country.lower():
                result = moex_service.get_current_candle(ticket)
            else :
                result = yahoo_service.get_current_candle(ticket)
            
            final_result.append(result.to_dict())
        
        app_service.post_market_data(final_result)