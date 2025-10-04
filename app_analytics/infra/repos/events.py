from typing import TYPE_CHECKING
from datetime import datetime

from app_analytics.domain.repos import BaseEventRepo, BaseEventVectorRepo
from app_analytics.infra.models import Event
from app_analytics.infra.database import get_database
from app_analytics.infra.vector_database import get_vector_database



class EventRepo(BaseEventRepo):
    def __init__(self):
        self.db_manager = get_database()

    async def save_event(self, event: Event) -> Event:
        async with self.db_manager.get_session() as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return event

    async def get_event_by_id(self, event_id: int) -> Event | None:
        async with self.db_manager.get_session() as session:
            model = await session.get(Event, event_id)
            return model

    async def update_event(self, event_id: int, **fields) -> Event | None:
        """
        Обновляет существующее событие по ID.
        :param event_id: ID события
        :param fields: словарь с обновляемыми полями (например, name="New name", date=datetime.now())
        :return: обновлённый объект Event или None, если не найден
        """
        async with self.db_manager.get_session() as session:
            model = await session.get(Event, event_id)
            if not model:
                return None

            # Обновляем только указанные поля
            for key, value in fields.items():
                if hasattr(model, key):
                    setattr(model, key, value)

            await session.commit()
            await session.refresh(model)
            return model



class EventVectorRepo(BaseEventVectorRepo):
    duplication_threshold = 0.9
    metadata_id_key = "id"

    def __init__(self):
        self.db_manager = get_vector_database()
        self.client = self.db_manager.client
        self.collection = self.client.get_or_create_collection("events")

    def add_event(self, event: 'Event') -> 'Event':
        self.collection.add(
            ids=[str(event.id)],
            documents=[event.content],
            metadatas=[{self.metadata_id_key: event.id}]
        )
        return event

    def semantic_search(self, query: str, n_results: int) -> list['Event']:
        # Реализация семантического поиска в векторной базе данных
        pass

    def get_id_if_duplicated(self, event_text: str) -> int | None:
        result = self.collection.query(
            query_texts=[event_text],
            n_results=1,
            include=["metadatas", "distances"]
        )

        if not result["distances"] or not result["distances"][0]:
            return None

        distance = result["distances"][0][0]
        metadata = result["metadatas"][0][0]

        similarity = 1 - distance
        if similarity > self.duplication_threshold:
            return metadata[self.metadata_id_key]

        return None
