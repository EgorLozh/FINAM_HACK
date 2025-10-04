from typing import TYPE_CHECKING
from datetime import datetime

from app_analytics.domain.repos import BaseEventRepo, BaseEventVectorRepo
from app_analytics.infra.models import Event as EventModel
from app_analytics.domain.entyties import Event
from app_analytics.infra.database import get_database
from app_analytics.infra.vector_database import get_vector_database

if TYPE_CHECKING:
    from app_analytics.infra.models.events import Event


class EventRepo(BaseEventRepo):
    def __init__(self):
        self.db_manager = get_database()

    def _to_model(self, event: 'Event') -> EventModel:
        # Преобразуем строки дат в datetime, если нужно
        first_appearance = (
            datetime.fromisoformat(event.first_appearance)
            if isinstance(event.first_appearance, str)
            else event.first_appearance
        )
        return EventModel(
            title=event.title,
            first_appearance=first_appearance,
            content=event.content,
            counter=event.counter,
            hotness=event.hotness,
            links=event.links,
            tags=event.tags,
            created_at=event.created_at or datetime.utcnow(),
            updated_at=event.updated_at or datetime.utcnow(),
        )

    def _to_entity(self, model: EventModel) -> 'Event':
        return Event(
            id=model.id,
            title=model.title,
            first_appearance=model.first_appearance,
            content=model.content,
            counter=model.counter,
            hotness=model.hotness,
            links=model.links,
            tags=model.tags,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def save_event(self, event: 'Event') -> 'Event':
        model = self._to_model(event)
        async with self.db_manager.get_session() as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
            entity = self._to_entity(model)
            if entity is None:
                raise ValueError("Failed to convert saved event to entity")
            return entity

    async def get_event_by_id(self, event_id: int) -> 'Event | None':
        async with self.db_manager.get_session() as session:
            model = await session.get(EventModel, event_id)
            return self._to_entity(model) if model else None


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

        distance = result["distances"][0][0]
        metadata = result["metadatas"][0][0]

        similarity = 1 - distance
        if similarity > self.duplication_threshold:
            return metadata[self.metadata_id_key]

        return None
