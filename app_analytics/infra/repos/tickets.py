from typing import List
from sqlalchemy.future import select
from app_analytics.infra.models import Ticket
from app_analytics.infra.database import get_database

class TicketsRepo:
    def __init__(self):
        self.db_manager = get_database()

    async def add_ticket(self, ticket: str, company: str, country: str) -> Ticket:
        """Добавить новый тикет."""
        new_ticket = Ticket(ticket=ticket, company=company, country=country)
        async with self.db_manager.get_session() as session:
            session.add(new_ticket)
            # commit и refresh выполняются автоматически через get_session()
            await session.flush()  # чтобы new_ticket.id стал доступен
            await session.refresh(new_ticket)
        return new_ticket

    async def get_all_tickets(self) -> List[Ticket]:
        """Получить все тикеты."""
        async with self.db_manager.get_session() as session:
            result = await session.execute(select(Ticket))
            tickets = result.scalars().all()
        return tickets
