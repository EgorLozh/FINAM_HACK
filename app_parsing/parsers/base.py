from dataclasses import dataclass
from abc import ABC, abstractmethod

from app_parsing.domain.value_objects.news import New


@dataclass
class BaseParser(ABC):

    @abstractmethod
    async def parse(self) -> list[New]:
        ...
