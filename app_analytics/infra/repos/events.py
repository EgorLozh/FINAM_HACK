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
        model = self._to_model(event)
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
    def __init__(self):
        self.db_manager = get_vector_database()

    def add_event(self, event: 'Event') -> 'Event':
        # Реализация добавления события в векторную базу данных
        pass

    def semantic_search(self, query: str, n_results: int) -> list['Event']:
        # Реализация семантического поиска в векторной базе данных
        pass
