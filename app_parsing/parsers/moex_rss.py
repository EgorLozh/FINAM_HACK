from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
import time
from typing import List

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

from app_parsing.domain.value_objects.news import New
from app_parsing.parsers.base import BaseParser


@dataclass
class MoexRssParser(BaseParser):
    base_url: str = "https://www.moex.com"
    rss_url: str = "https://www.moex.com/export/news.aspx?cat=100"  # RSS для новостей
    alternative_rss_urls: List[str] = field(default_factory=lambda: [
        "https://www.moex.com/export/news.aspx?cat=1",  # Альтернативный URL
        "https://www.moex.com/export/news.aspx",  # Базовый URL без категории
    ])
    max_articles: int = 20
    delay: float = 0.5  # пауза между запросами

    async def parse(self) -> List[New]:
        results: List[New] = []
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        
        try:
            # Пробуем основной RSS URL
            feed = feedparser.parse(self.rss_url)
            
            # Если основной URL не работает или содержит ошибки, пробуем альтернативные
            if feed.bozo or not feed.entries:
                print(f"Primary RSS URL failed or has issues:")
                if feed.bozo:
                    print(f"  - Exception: {feed.bozo_exception}")
                    print(f"  - Status: {feed.status}")
                    print(f"  - Version: {feed.version}")
                    print(f"  - Encoding: {feed.encoding}")
                
                # Пробуем альтернативные URL
                for alt_url in self.alternative_rss_urls:
                    print(f"Trying alternative RSS URL: {alt_url}")
                    alt_feed = feedparser.parse(alt_url)
                    
                    if not alt_feed.bozo and alt_feed.entries:
                        print(f"Alternative URL successful: {len(alt_feed.entries)} entries found")
                        feed = alt_feed
                        break
                    else:
                        print(f"Alternative URL also failed: {alt_feed.bozo_exception if alt_feed.bozo else 'No entries'}")
                
                # Если все URL не работают
                if not feed.entries:
                    print("All RSS URLs failed. Returning empty results.")
                    return []
            
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; MOEX-parser/1.0; +https://example.com/bot)"
            }
            
            def fetch_full_text(url: str) -> str:
                """Получаем полный текст статьи"""
                try:
                    resp = requests.get(url, headers=headers, timeout=10)
                    resp.raise_for_status()
                    soup = BeautifulSoup(resp.text, "html.parser")
                    
                    # Ищем основной контент статьи
                    content_selectors = [
                        "div.news-content",
                        "div.article-content", 
                        "div.content",
                        "article",
                        "div.news-text",
                        "div.news-body"
                    ]
                    
                    for selector in content_selectors:
                        content_div = soup.select_one(selector)
                        if content_div:
                            # Извлекаем текст из всех параграфов
                            paragraphs = content_div.find_all(['p', 'div', 'span'])
                            text_parts = []
                            for p in paragraphs:
                                text = p.get_text(strip=True)
                                if text and len(text) > 20:  # Игнорируем короткие фрагменты
                                    text_parts.append(text)
                            
                            if text_parts:
                                return "\n\n".join(text_parts)
                    
                    # Если не нашли структурированный контент, берем весь текст страницы
                    return soup.get_text(separator="\n", strip=True)
                    
                except Exception as e:
                    print(f"Warning: failed to fetch full text from {url}: {e}")
                    return ""
            
            # Обрабатываем каждую запись в RSS
            for entry in feed.entries:
                try:
                    # Извлекаем заголовок с очисткой от некорректных символов
                    headline = entry.get('title', '').strip()
                    if not headline:
                        continue
                    # Очищаем заголовок от HTML тегов и некорректных символов
                    headline = BeautifulSoup(headline, "html.parser").get_text(strip=True)
                    
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
                    
                    # Фильтруем новости за последний час
                    if created_at < one_hour_ago:
                        continue
                    
                    # Получаем полный текст статьи
                    full_text = fetch_full_text(url)
                    
                    # Если не удалось получить полный текст, используем summary из RSS
                    if not full_text or len(full_text.strip()) < 50:
                        body = entry.get('summary', '').strip()
                        if not body:
                            body = entry.get('description', '').strip()
                        # Очищаем от HTML тегов
                        if body:
                            body = BeautifulSoup(body, "html.parser").get_text(strip=True)
                    else:
                        body = full_text
                    
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