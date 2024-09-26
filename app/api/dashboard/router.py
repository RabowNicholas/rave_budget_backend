from datetime import datetime
from fastapi import APIRouter, Depends, Header
from fastapi_camelcase import CamelModel
from sqlalchemy.orm import Session

from app.contexts.budget.context import BudgetContext
from app.contexts.budget.models import Budget
from app.contexts.budget.repository import BudgetRepository
from app.database import get_db


dashboard_router = APIRouter()


class BudgetCategoryBreakdownResponse(CamelModel):
    category: str
    budgeted_amount: float
    expense_amount: float


class BudgetOverviewResponse(CamelModel):
    id: str
    name: str
    date: datetime
    location: str
    total_budget: float
    total_spent: float
    remaining_balance: float
    category_breakdown: list[BudgetCategoryBreakdownResponse]


class DashboardGetResponse(CamelModel):
    budgets: list[BudgetOverviewResponse]


@dashboard_router.get("", response_model=DashboardGetResponse)
async def get_dashboard(
    user_id: str = Header(),
    session: Session = Depends(get_db),
) -> DashboardGetResponse:

    budgets: list[BudgetOverviewResponse] = []
    budget_context = BudgetContext(BudgetRepository(session))
    budgets = budget_context.get_budgets_for_user(user_id)

    budgets_response = _pack_response(budgets=budgets)

    return DashboardGetResponse(budgets=budgets_response)


def _pack_response(budgets: list[Budget]) -> list[BudgetOverviewResponse]:
    budgets_response: list[BudgetOverviewResponse] = []

    for b in budgets:
        budget_breakdown: list[BudgetCategoryBreakdownResponse] = []
        for l in b.limits:
            # TODO: add spent amount when expenses are in
            breakdown = BudgetCategoryBreakdownResponse(
                category=l.category,
                budgeted_amount=l.amount,
                expense_amount=0,
            )
            budget_breakdown.append(breakdown)

        budget_response = BudgetOverviewResponse(
            id=b.id,
            name=b.name,
            date=b.date,
            location=b.location,
            total_budget=b.total_budget,
            total_spent=0,
            remaining_balance=b.total_budget - 0,
            category_breakdown=budget_breakdown,
        )

        budgets_response.append(budget_response)

    return budgets_response
