from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, DateTime, Text, Integer, Float, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app_analytics.infra.database import Base

class Ticket(Base):
    __tablename__ = "tickets"
    company: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    ticket: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
