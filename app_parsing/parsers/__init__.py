from app_parsing.parsers.parsers_manager import ParsersManager
from app_parsing.parsers.rbc import RbcParser

from app_parsing.settings import settings
from app_parsing.parsers.telegram import TelegramParser
from app_parsing.parsers.markets import MarketsParser

_parser_manager = None


def get_parsers_manager() -> ParsersManager:
    global _parser_manager
    if _parser_manager is None:
        _parser_manager = init_parser_manager()
    return _parser_manager


def init_parser_manager() -> ParsersManager:
    parser_manager = ParsersManager()
    parser_manager.add_parser(
        key="rbc",
        parser=RbcParser(
        )
    )
    parser_manager.add_parser(
        key="markets",
        parser=MarketsParser()
    )
    return parser_manager
