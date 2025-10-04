from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

from app_parsing.domain.value_objects.news import New
from app_parsing.parsers.base import BaseParser


@dataclass
class InterfaxParser(BaseParser):
    base_url: str = "https://www.interfax.ru"
    section_url: str = "https://www.interfax.ru/business/"
    max_articles: int = 20
    delay: float = 0.5  # пауза между запросами

    async def parse(self) -> List[New]:
        results: List[New] = []
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=24)  # Увеличиваем до 24 часов для тестирования
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; Interfax-parser/1.0; +https://example.com/bot)"
            }
            
            def fetch(url: str) -> str:
                resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
                
                # Пробуем разные кодировки для русского текста
                for encoding in ['utf-8', 'windows-1251', 'cp1251', 'iso-8859-1']:
                    try:
                        resp.encoding = encoding
                        test_text = resp.text
                        # Проверяем, что русские буквы отображаются корректно
                        if 'Ð' not in test_text and 'Ñ' not in test_text and 'â' not in test_text:
                            # Дополнительная проверка - ищем русские буквы
                            if any(ord(char) >= 1040 and ord(char) <= 1103 for char in test_text[:1000]):
                                break
                    except:
                        continue
                
                return resp.text
            
            def extract_article_links(html: str) -> List[str]:
                """Извлекаем ссылки на статьи с главной страницы"""
                # Указываем кодировку для BeautifulSoup
                soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')
                links = []
                
                # Ищем ссылки на статьи в различных контейнерах
                selectors = [
                    "a[href*='/business/']",
                    ".timeline__item a",
                    ".timeline__text a", 
                    ".news__item a",
                    ".news__text a",
                    "article a",
                    ".item a"
                ]
                
                for selector in selectors:
                    for link in soup.select(selector):
                        href = link.get('href')
                        if href and '/business/' in href:
                            # Преобразуем относительные ссылки в абсолютные
                            if href.startswith('/'):
                                full_url = self.base_url + href
                            elif href.startswith('http'):
                                full_url = href
                            else:
                                full_url = self.base_url + '/' + href
                            
                            # Очищаем URL от параметров и якорей
                            clean_url = full_url.split('?')[0].split('#')[0]
                            if clean_url not in links:
                                links.append(clean_url)
                
                return links[:self.max_articles]
            
            def fetch_full_text(url: str) -> str:
                """Получаем полный текст статьи"""
                try:
                    resp = requests.get(url, headers=headers, timeout=10)
                    resp.raise_for_status()
                    
                    # Пробуем разные кодировки для русского текста
                    for encoding in ['utf-8', 'windows-1251', 'cp1251', 'iso-8859-1']:
                        try:
                            resp.encoding = encoding
                            test_text = resp.text
                            # Проверяем, что русские буквы отображаются корректно
                            if 'Ð' not in test_text and 'Ñ' not in test_text and 'â' not in test_text:
                                # Дополнительная проверка - ищем русские буквы
                                if any(ord(char) >= 1040 and ord(char) <= 1103 for char in test_text[:1000]):
                                    break
                        except:
                            continue
                    
                    soup = BeautifulSoup(resp.text, "html.parser", from_encoding='utf-8')
                    
                    # Ищем основной контент статьи
                    content_selectors = [
                        "article .text",
                        "article .article__text",
                        ".article__text",
                        ".text",
                        "article",
                        ".news__text",
                        ".content"
                    ]
                    
                    for selector in content_selectors:
                        content_div = soup.select_one(selector)
                        if content_div:
                            # Извлекаем текст из всех параграфов
                            paragraphs = content_div.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3'])
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
            
            # Получаем главную страницу раздела
            print(f"Fetching main page: {self.section_url}")
            main_html = fetch(self.section_url)
            article_links = extract_article_links(main_html)
            
            print(f"Found {len(article_links)} article links")
            
            # Обрабатываем каждую статью
            for i, link in enumerate(article_links, 1):
                try:
                    print(f"Processing article {i}/{len(article_links)}: {link}")
                    
                    # Получаем HTML страницы статьи
                    article_html = fetch(link)
                    soup = BeautifulSoup(article_html, "html.parser", from_encoding='utf-8')
                    
                    # Извлекаем заголовок
                    headline = None
                    title_selectors = [
                        "h1",
                        ".article__title",
                        ".news__title", 
                        "title",
                        ".headline"
                    ]
                    
                    for selector in title_selectors:
                        title_elem = soup.select_one(selector)
                        if title_elem:
                            headline = title_elem.get_text(strip=True)
                            break
                    
                    if not headline:
                        print(f"Warning: no headline found for {link}")
                        continue
                    
                    # Извлекаем дату публикации
                    created_at = None
                    date_selectors = [
                        "time[datetime]",
                        ".article__date",
                        ".news__date",
                        ".date",
                        "time"
                    ]
                    
                    for selector in date_selectors:
                        date_elem = soup.select_one(selector)
                        if date_elem:
                            date_str = date_elem.get('datetime') or date_elem.get_text(strip=True)
                            if date_str:
                                try:
                                    created_at = dateparser.parse(date_str)
                                    if created_at and created_at.tzinfo is None:
                                        created_at = created_at.replace(tzinfo=timezone.utc)
                                    break
                                except Exception:
                                    continue
                    
                    if not created_at:
                        # Если дата не найдена, используем текущее время
                        created_at = datetime.now(timezone.utc)
                    
                    # Фильтруем новости за последний час
                    if created_at < one_hour_ago:
                        print(f"Skipping old article: {created_at}")
                        continue
                    
                    # Получаем полный текст статьи
                    full_text = fetch_full_text(link)
                    
                    # Если не удалось получить полный текст, используем краткое описание
                    if not full_text or len(full_text.strip()) < 50:
                        # Ищем краткое описание
                        desc_selectors = [
                            ".article__summary",
                            ".news__summary", 
                            ".summary",
                            "meta[name='description']"
                        ]
                        
                        for selector in desc_selectors:
                            desc_elem = soup.select_one(selector)
                            if desc_elem:
                                if selector.startswith('meta'):
                                    full_text = desc_elem.get('content', '')
                                else:
                                    full_text = desc_elem.get_text(strip=True)
                                break
                    
                    # Создаем объект новости
                    news_item = New(
                        headline=headline,
                        body=full_text or "Текст статьи недоступен",
                        created_at=created_at,
                        source="Interfax Business",
                        url=link
                    )
                    
                    results.append(news_item)
                    print(f"Added article: {headline[:50]}...")
                    
                    # Пауза между запросами
                    if self.delay > 0:
                        time.sleep(self.delay)
                        
                except Exception as e:
                    print(f"Warning: failed to process article {link}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error parsing Interfax: {e}")
            return []
        
        return results
