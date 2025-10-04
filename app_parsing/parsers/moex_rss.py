from dataclasses import dataclass
from datetime import datetime, timezone
import time
from typing import List

import feedparser
from dateutil import parser as dateparser

from app_parsing.domain.value_objects.news import New
from app_parsing.parsers.base import BaseParser


@dataclass
class MoexRssParser(BaseParser):
    base_url: str = "https://www.moex.com"
    rss_url: str = "https://www.moex.com/export/news.aspx?cat=100"  # RSS для новостей
    max_articles: int = 20
    delay: float = 0.5  # пауза между запросами

    async def parse(self) -> List[New]:
        results: List[New] = []
        
        try:
            # Парсим RSS ленту
            feed = feedparser.parse(self.rss_url)
            
            if feed.bozo:
                print(f"Warning: RSS feed parsing issues: {feed.bozo_exception}")
            
            # Обрабатываем каждую запись в RSS
            for entry in feed.entries[:self.max_articles]:
                try:
                    # Извлекаем заголовок
                    headline = entry.get('title', '').strip()
                    if not headline:
                        continue
                    
                    # Извлекаем ссылку
                    url = entry.get('link', '').strip()
                    if not url:
                        continue
                    
                    # Извлекаем дату публикации
                    created_at = None
                    published = entry.get('published_parsed')
                    if published:
                        created_at = datetime(*published[:6], tzinfo=timezone.utc)
                    else:
                        # Пробуем парсить строку даты
                        published_str = entry.get('published', '')
                        if published_str:
                            try:
                                created_at = dateparser.parse(published_str)
                                if created_at and created_at.tzinfo is None:
                                    created_at = created_at.replace(tzinfo=timezone.utc)
                            except Exception:
                                created_at = None
                    
                    if not created_at:
                        # Если дата не найдена, используем текущее время
                        created_at = datetime.now(timezone.utc)
                    
                    # Извлекаем описание/тело новости
                    body = entry.get('summary', '').strip()
                    if not body:
                        body = entry.get('description', '').strip()
                    
                    # Если описание слишком короткое, попробуем получить полный текст
                    if len(body) < 100:
                        # Можно добавить логику для получения полного текста статьи
                        # но для RSS обычно достаточно summary
                        pass
                    
                    # Создаем объект новости
                    news_item = New(
                        headline=headline,
                        body=body,
                        created_at=created_at,
                        source="MOEX News",
                        url=url
                    )
                    
                    results.append(news_item)
                    
                    # Пауза между обработкой записей
                    if self.delay > 0:
                        time.sleep(self.delay)
                        
                except Exception as e:
                    print(f"Warning: failed to process RSS entry: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error parsing MOEX RSS feed: {e}")
            return []
        
        return results