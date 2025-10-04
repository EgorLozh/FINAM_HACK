from dataclasses import dataclass, field

from app_parsing.parsers.base import BaseParser


@dataclass
class ParsersManager:

    parsers: dict[str, BaseParser] = field(default_factory=dict)

    def get_parsers(self) -> dict[str, BaseParser]:
        return self.parsers

    def get_parser(self, key: str) -> BaseParser:
        return self.parsers[key]

    def add_parser(self, key: str, parser: BaseParser) -> None:
        self.parsers[key] = parser
