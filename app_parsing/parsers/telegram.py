from dataclasses import dataclass

from telethon import TelegramClient
from datetime import datetime, timedelta

from app_parsing.domain.value_objects.news import New
from app_parsing.parsers.base import BaseParser


@dataclass
class TelegramParser(BaseParser):

    api_id: int
    api_hash: str
    bot_token: str
    channels: list[str]

    async def parse(self) -> list[New]:
        results = []
        client = TelegramClient(
            "session_name",
            self.api_id,
            self.api_hash,
        )
        await client.start(bot_token=self.bot_token)

        one_hour_ago = datetime.utcnow() - timedelta(hours=1)

        for channel in self.channels:
            entity = await client.get_entity(channel)
            async for message in client.iter_messages(entity, offset_date=one_hour_ago, reverse=True):
                if message.date < one_hour_ago:
                    continue
                results.append(
                    New(
                        headline=(message.message.split("\n")[0] if message.message else None),
                        body=message.message,
                        created_at=message.date.isoformat(),
                        source=entity.title,
                        url=f"https://t.me/{entity.username}/{message.id}" if entity.username else None,
                    )
                )
        return results
