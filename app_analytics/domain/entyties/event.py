from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    id: int | None = field(default=None, kw_only=True)
    title: str
    first_appearance: str  # ISO format date string
    content: str
    counter: int = 1
    hotness: float | None = None
    links: list[str] = None
    tags: list[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)