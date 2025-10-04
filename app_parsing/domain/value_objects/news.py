from dataclasses import dataclass
from datetime import datetime


@dataclass
class New:
    headline: str
    body: str
    timestamp: datetime
    source: str
    url: str
