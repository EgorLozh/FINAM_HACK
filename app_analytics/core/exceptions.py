from dataclasses import dataclass
from http import HTTPStatus


@dataclass(eq=False)
class BaseError(Exception):
    """Базовый класс для всех ошибок в приложении."""

    @property
    def message(self) -> str:
        return "Exception"

    def __str__(self) -> str:
        return self.message


@dataclass(eq=False)
class APIError(BaseError):
    """Базовый класс для ошибок API."""

    @property
    def message(self) -> str:
        return "API Error"

    @property
    def status_code(self) -> HTTPStatus:
        return HTTPStatus.INTERNAL_SERVER_ERROR
