from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime as DateTimeC


class InterestFeature(Base):
    __tablename__: str = "interest_feature"

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
    user_id: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
