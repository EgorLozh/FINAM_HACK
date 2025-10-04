from chromadb import config, Client
from app_analytics.core.config import settings



class VectorDatabaseManager:
    def __init__(self):
        pass
        # self.client = Client(
        #     config.Settings(
        #         persist_directory="./.chroma/persistent" if settings.CHROMA_IS_PERSISTENT else None,
        #         anonymized_telemetry=False,
        #         host=settings.CHROMA_HOST,
        #         port=settings.CHROMA_PORT,
        #     )
        # ) Хуйня какая-то с хромой, пока закомментил, settings берет из pydantic и ругается на неизвестные поля

    def get_client(self) -> Client:
        return self.client