from typing import TYPE_CHECKING, List
from datetime import datetime
from app_analytics.infra.database import get_database
from app_analytics.infra.models import Ticket


class TicketsRepo:
    def __init__(self):
        self.db_manager = get_database()


    def add_ticket(self, ticket: str, company: str) -> Ticket:
        """Добавить новый тикет."""
        new_ticket = Ticket(
            ticket=ticket,
            company=company
        )
        self.db_manager.add(new_ticket)
        self.db_manager.commit()
        self.db_manager.refresh(new_ticket)
        return new_ticket

    def get_all_tickets(self) -> List[Ticket]:
        """Получить все тикеты."""
        tickets = self.db_manager.query(Ticket).all()
        return tickets
