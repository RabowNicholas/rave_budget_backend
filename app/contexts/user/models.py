from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime as DateTimeC
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__: str = "user"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        unique=True,
        default=lambda: str(uuid4()),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTimeC,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTimeC, default=None)
    phone: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    name: Mapped[Optional[str]] = mapped_column(String)
