import logging
import logging.config
import sys

from app_analytics.core.config import settings

# Получаем уровень логирования из настроек
LOG_LEVEL = settings.LOG_LEVEL.upper()

# Формат для JSON логов. Указываем стандартные поля.
# python-json-logger автоматически добавит поля из extra в JSON.
JSON_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"

# Определяем конфигурацию логирования Python
LOGGING_CONFIG = {
    "version": 1,  # Версия схемы конфигурации
    "disable_existing_loggers": False,  # Не отключать существующие логгеры
    "formatters": {
        "json_formatter": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": JSON_LOG_FORMAT,
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 формат времени
        },
        "simple_formatter": {  # Добавим простой форматтер для uvicorn.access
            "format": "%(levelname)s:     %(message)s",
        },
    },
    "handlers": {
        "console_json": {  # Обработчик для вывода JSON логов в консоль (stdout)
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,  # Уровень обработки для этого хендлера
            "formatter": "json_formatter",
            "stream": sys.stdout,  # Вывод в стандартный поток вывода
        },
        "console_simple": {  # Обработчик для вывода простых логов uvicorn.access
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple_formatter",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "uvicorn": {  # Настройка логгера uvicorn (основной)
            "handlers": ["console_json"],
            "level": LOG_LEVEL,
            "propagate": False,  # Не передавать сообщения родительскому логгеру
        },
        "uvicorn.error": {  # Настройка логгера ошибок uvicorn
            "handlers": ["console_json"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.access": {  # Теперь используем JSON форматтер для логов доступа
            "handlers": ["console_json"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy": {  # Настройка логгера SQLAlchemy
            "handlers": ["console_json"],
            # Уровень WARNING, чтобы не засорять логи SQL запросами (если не нужно)
            # Можно поменять на INFO или DEBUG для отладки SQL
            "level": "WARNING",
            "propagate": False,
        },
        "alembic": {  # Настройка логгера Alembic
            "handlers": ["console_json"],
            "level": "INFO",
            "propagate": False,
        },
        # Можно добавить настройки для других библиотек...
    },
    "root": {  # Настройка корневого логгера (для нашего кода)
        "handlers": ["console_json"],
        "level": LOG_LEVEL,
    },
}


def setup_logging() -> None:
    """Применяет конфигурацию логирования."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully with level %s.", LOG_LEVEL)
