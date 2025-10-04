import chromadb

from app_analytics.core.config import settings

class VectorDatabase:
    def __init__(self, chroma_host: str, chroma_port: int) -> None:
        self.client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
        )

    def get_client(self) -> chromadb.HttpClient:
        return self.client


_vector_database: VectorDatabase | None = None


def get_vector_database() -> VectorDatabase:
    if _vector_database is None:
        _init_vector_database()
    return _vector_database  # type: ignore


def _init_vector_database() -> None:
    global _vector_database
    _vector_database = VectorDatabase(chroma_host=settings.CHROMA_HOST, chroma_port=settings.CHROMA_PORT)

