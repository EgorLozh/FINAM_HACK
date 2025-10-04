from app_analytics.application.use_cases.base import BaseDatabaseUseCase
from app_analytics.infra.repos.market_data import MarketDataRepository



class PostMarketDataUseCase(BaseDatabaseUseCase):
    @classmethod
    async def execute(cls, market_data: list) -> None:
        # Логика добавления рыночных данных в базу данных
        repo = MarketDataRepository()
        data = [data.to_dict() for data in market_data]
        await repo.add_market_data(data)
