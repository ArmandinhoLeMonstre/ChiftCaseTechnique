from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Partner(Base):
    __tablename__ = "partners"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    write_date: Mapped[datetime]= mapped_column(DateTime)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    reconciliation_flag: Mapped[bool] = mapped_column(Boolean, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

class SyncState(Base):
    __tablename__ = "sync_state"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(30), unique=True)
    write_date: Mapped[datetime]= mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"