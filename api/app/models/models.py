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

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    odoo_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    write_date: Mapped[datetime]= mapped_column(DateTime)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    reconciliation_flag: Mapped[bool] = mapped_column(Boolean, nullable=True)

    def __repr__(self) -> str:
        return (
            f"Partner(id={self.id}, "
            f"odoo_id={self.odoo_id}, "
            f"name='{self.name}', "
            f"active={self.active}, "
            f"reconciliation_flag={self.reconciliation_flag})"
        )

class SyncState(Base):
    __tablename__ = "sync_state"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(30), unique=True)
    write_date: Mapped[datetime]= mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"SyncState(id={self.id}, "
            f"model='{self.model}', "
            f"write_date={self.write_date})"
        )