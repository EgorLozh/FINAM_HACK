from app_analytics.application.use_cases.base import BaseDatabaseUseCase
from app_analytics.infra.repos.tickets import TicketsRepo

class GetTicketsUseCase(BaseDatabaseUseCase):
    @classmethod
    def execute(cls) -> list[tuple]:
        repo = TicketsRepo()
        repo.get_all_tickets()
        return [(ticket.ticket, ticket.country) for ticket in repo.get_all_tickets()]
