from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import DateTime as DateTimeC, Float, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property


from app.database import Base


class Budget(Base):
    __tablename__: str = "budget"

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
    date: Mapped[datetime] = mapped_column(DateTimeC)
    location: Mapped[str] = mapped_column(String)

    limits: Mapped[list["BudgetLimit"]] = relationship(
        "BudgetLimit", back_populates="budget"
    )
    expenses: Mapped[list["BudgetExpense"]] = relationship(
        "BudgetExpense", back_populates="budget"
    )

    @hybrid_property
    def total_budget(self) -> float:
        return sum(limit.amount for limit in self.limits)

    @hybrid_property
    def total_expense(self) -> float:
        return sum(e.amount for e in self.expenses)


class BudgetLimit(Base):
    __tablename__: str = "budget_limit"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        unique=True,
        default=lambda: str(uuid4()),
    )
    budget_id: Mapped[str] = mapped_column(String, ForeignKey("budget.id"))
    category: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)

    budget: Mapped["Budget"] = relationship("Budget", back_populates="limits")


class BudgetExpense(Base):
    __tablename__: str = "budget_expense"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, unique=True, default=lambda: str(uuid4())
    )
    budget_id: Mapped[str] = mapped_column(String, ForeignKey("budget.id"))
    category: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)

    budget: Mapped["Budget"] = relationship("Budget", back_populates="expenses")
