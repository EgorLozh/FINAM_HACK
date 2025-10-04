import logging
import aiohttp
import asyncio
import json
from app_analytics.core.config import settings


logger = logging.getLogger(__name__)


class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPEN_ROUTER_API_KEY
        self.model = settings.OPEN_ROUTER_MODEL
        self.base_url = settings.OPEN_ROUTER_URL

    async def send_request(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        logger.info("Sending prompt to LLM", extra={"prompt": prompt})
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"API returned {response.status}: {await response.text()}")
                data = await response.json()
                # Получаем текст ответа от модели

                logger.info("Generated response AI", extra={"response": data})

                return data["choices"][0]["message"]["content"]
