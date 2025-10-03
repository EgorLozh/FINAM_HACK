from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, DateTime, Text, Integer, Float, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app_analytics.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)  # сгенерированный заголовок
    first_appearance: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # первое появление
    content: Mapped[str] = mapped_column(Text, nullable=False)  # содержание события
    counter: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # сколько подобных новостей
    hotness: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # горячесть
    links: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String(500)), default=list)  # откуда (источники)
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String(100)), default=list)  # о каких инструментах событие
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, title='{self.title[:50]}...', counter={self.counter})>"