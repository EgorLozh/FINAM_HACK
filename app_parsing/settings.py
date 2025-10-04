from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # REDIS
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    TELEGRAM_API_ID: int = 0
    TELEGRAM_API_HASH: str = ""
    TELEGRAM_TOKEN: str = ""

    TELEGRAM_CHANNELS: list[str] = ["@naurys_home"]

    INTERNAL_API_TOKEN: str = ""

    @property
    def celery_broker_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @property
    def celery_result_backend(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"


settings = Settings()
