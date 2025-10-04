import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dateutil import parser as dateparser

from app_parsing.domain.value_objects.news import New
from app_parsing.parsers.base import BaseParser


logger = logging.getLogger(__name__)


@dataclass
class RbcParser(BaseParser):
    base_url: str = "https://www.rbc.ru"
    section_url: str = "https://www.rbc.ru/economics/"
    max_articles: int = 20
    delay: float = 0.5  # пауза между запросами

    async def parse(self) -> List[New]:
        one_hour_ago = datetime.now(timezone.utc)
        results: List[New] = []

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; simple-scraper/1.0; +https://example.com/bot)"
        }

        def fetch(url: str) -> str:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.text

        def extract_links(html: str) -> list[str]:
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/economics/" in href:
                    full_url = urljoin(self.base_url, href)
                    links.append(full_url.split("?")[0].rstrip("/"))
            # уникальные ссылки
            return list(dict.fromkeys(links))

        section_html = fetch(self.section_url)
        article_links = extract_links(section_html)[:self.max_articles]

        for link in article_links:
            try:
                html = fetch(link)
            except Exception as e:
                print(f"Warning: failed to fetch {link}: {e}")
                continue

            soup = BeautifulSoup(html, "html.parser")

            # headline
            headline = None
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                headline = og_title["content"].strip()
            if not headline:
                t = soup.find("title")
                if t:
                    headline = t.text.strip()
            if not headline:
                h1 = soup.find("h1")
                if h1:
                    headline = h1.text.strip()

            # created_at
            created_at = None
            meta_time = soup.find("meta", property="article:published_time")
            if meta_time and meta_time.get("content"):
                try:
                    created_at = dateparser.parse(meta_time["content"])
                except Exception:
                    created_at = None
            if not created_at:
                time_tag = soup.find("time")
                if time_tag:
                    dt = time_tag.get("datetime") or time_tag.text
                    if dt:
                        try:
                            created_at = dateparser.parse(dt.strip())
                        except Exception:
                            created_at = None
            if not created_at:
                continue

            # if created_at < one_hour_ago:
            #     continue

            # body
            article_tag = soup.find("article")
            paragraphs = []
            if article_tag:
                paragraphs = article_tag.find_all(["p", "h2", "li"])
            else:
                container = soup.find("div", {"class": lambda c: c and ("article__text" in c or "article__body" in c)})
                if container:
                    paragraphs = container.find_all(["p", "h2", "li"])
            body_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if not body_text:
                og_desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
                if og_desc and og_desc.get("content"):
                    body_text = og_desc["content"].strip()

            results.append(
                New(
                    headline=headline,
                    body=body_text,
                    created_at=created_at,
                    source="RBC — Economics",
                    url=link
                )
            )
            time.sleep(self.delay)

        return results
