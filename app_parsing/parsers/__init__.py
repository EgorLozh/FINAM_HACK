from app_parsing.parsers.parsers_manager import ParsersManager

from app_parsing.settings import settings
from app_parsing.parsers.telegram import TelegramParser

_parser_manager = None


def get_parsers_manager() -> ParsersManager:
    global _parser_manager
    if _parser_manager is None:
        _parser_manager = init_parser_manager()
    return _parser_manager


def init_parser_manager() -> ParsersManager:
    parser_manager = ParsersManager()
    parser_manager.add_parser(
        key="telegram",
        parser=TelegramParser(
            api_id=settings.TELEGRAM_API_ID,
            api_hash=settings.TELEGRAM_API_HASH,
            channels=settings.TELEGRAM_CHANNELS,
            bot_token=settings.TELEGRAM_TOKEN,
        )
    )

    return parser_manager
