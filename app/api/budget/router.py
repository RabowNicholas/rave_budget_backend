from datetime import datetime
from fastapi import APIRouter, Depends, Header
from fastapi_camelcase import CamelModel
from sqlalchemy.orm import Session
from app.api.budget.exceptions import NotAuthorizedException
from app.contexts.budget.context import (
    BudgetContext,
    BudgetData,
    BudgetDataEnum,
    BudgetLimitData,
    BudgetOverviewData,
)
from app.contexts.budget.models import Budget
from app.contexts.budget.repository import BudgetRepository
from app.database import get_db

budget_router = APIRouter()


class BudgetOverviewRequest(CamelModel):
    name: str
    date: datetime
    location: str


class BudgetLimitRequest(CamelModel):
    category: str
    amount: float


class BudgetPostBudgetRequest(CamelModel):
    overview: BudgetOverviewRequest
    limits: list[BudgetLimitRequest]


class BudgetPostBudgetResponse(CamelModel):
    message: str
    budget_id: str


@budget_router.post("", response_model=BudgetPostBudgetResponse)
async def post_budget(
    req: BudgetPostBudgetRequest,
    user_id: str = Header(),
    session: Session = Depends(get_db),
) -> BudgetPostBudgetResponse:
    budget_context = BudgetContext(BudgetRepository(session))

    budget_data = _parse_post_budget_request(req)

    budget = budget_context.create_budget(
        user_id=user_id,
        data=budget_data,
    )

    return BudgetPostBudgetResponse(
        message="Budget created successfully", budget_id=budget.id
    )


def _parse_post_budget_request(req: BudgetPostBudgetRequest) -> BudgetData:
    try:
        overview = BudgetOverviewData()
        overview.name = req.overview.name
        overview.date = req.overview.date
        overview.location = req.overview.location

        limits = []
        for l in req.limits:
            limit = BudgetLimitData()
            limit.category = BudgetDataEnum(l.category).value
            limit.amount = l.amount
            limits.append(limit)

        budget_data = BudgetData()
        budget_data.overview = overview
        budget_data.limits = limits
        return budget_data
    except Exception as e:
        raise ValueError("Error parsing budget request data") from e


class BudgetCategoryBreakdownResponse(CamelModel):
    category: str
    budgeted_amount: float
    expense_amount: float


class BudgetGetBudgetResponse(CamelModel):
    id: str
    name: str
    date: datetime
    location: str
    total_budget: float
    total_spent: float
    remaining_balance: float
    category_breakdown: list[BudgetCategoryBreakdownResponse]


def _pack_get_budget_response(b: Budget) -> BudgetGetBudgetResponse:
    category_expense_map = {}

    for expense in b.expenses:
        if expense.category in category_expense_map:
            category_expense_map[expense.category] += expense.amount
        else:
            category_expense_map[expense.category] = expense.amount

    budget_breakdown: list[BudgetCategoryBreakdownResponse] = []
    total_unexpected_expenses = 0

    for l in b.limits:
        spent_amount = category_expense_map.pop(l.category, 0)

        breakdown = BudgetCategoryBreakdownResponse(
            category=l.category,
            budgeted_amount=l.amount,
            expense_amount=spent_amount,
        )
        budget_breakdown.append(breakdown)

    for spent_amount in category_expense_map.items():
        total_unexpected_expenses += spent_amount

    if total_unexpected_expenses > 0:
        breakdown = BudgetCategoryBreakdownResponse(
            category="Unexpected",
            budgeted_amount=0,
            expense_amount=total_unexpected_expenses,
        )
        budget_breakdown.append(breakdown)

    return BudgetGetBudgetResponse(
        id=b.id,
        name=b.name,
        date=b.date,
        location=b.location,
        total_budget=b.total_budget,
        total_spent=b.total_expense,
        remaining_balance=b.total_budget - b.total_expense,
        category_breakdown=budget_breakdown,
    )


@budget_router.get("/{budget_id}")
async def get_budget(
    budget_id: str,
    user_id: str = Header(),
    session: Session = Depends(get_db),
) -> BudgetGetBudgetResponse:
    budget_context = BudgetContext(BudgetRepository(session))
    budget = budget_context.get_budget(budget_id)
    if budget.user_id != user_id:
        raise NotAuthorizedException("user not authorized to access budget")
    response = _pack_get_budget_response(budget)
    return response


class BudgetPostExpenseRequest(CamelModel):
    amount: float
    category: str


@budget_router.post("/{budget_id}/expense")
async def post_expense(
    budget_id: str,
    req: BudgetPostExpenseRequest,
    user_id: str = Header(),
    session: Session = Depends(get_db),
) -> None:
    budget_context = BudgetContext(BudgetRepository(session))
    budget = budget_context.get_budget(budget_id)
    if budget.user_id != user_id:
        raise NotAuthorizedException("user not authorize to access budget")
    budget_context.add_expense(budget_id, req.amount, req.category)
