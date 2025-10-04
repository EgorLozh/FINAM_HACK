from dataclasses import dataclass
from datetime import datetime


@dataclass
class New:
    headline: str
    body: str
    created_at: datetime
    source: str
    url: str
