from dataclasses import dataclass

from telethon import TelegramClient
from datetime import datetime, timedelta

from app_parsing.domain.value_objects.news import New
from app_parsing.parsers.base import BaseParser


@dataclass
class TelegramParser(BaseParser):

    api_id: int
    api_hash: str
    channels: list[str]

    async def parse(self) -> list[New]:
        results = []

        client = TelegramClient(
            "app_parsing/session_name", self.api_id, self.api_hash
        )
        await client.connect()

        if not await client.is_user_authorized():
            raise RuntimeError(
                "Telethon client is not authorized. Please run the initial setup interactively."
            )

        try:
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
        finally:
            if client.is_connected():
                await client.disconnect()
        return results
