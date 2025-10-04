from app_analytics.application.use_cases.base import BaseDatabaseUseCase
from app_analytics.infra.repos.tickets import TicketsRepo

class GetTicketsUseCase(BaseDatabaseUseCase):
    @classmethod
    def execute(cls) -> list[str]:
        repo = TicketsRepo()
        repo.get_all_tickets()
        return [ticket.ticket for ticket in repo.get_all_tickets()]
