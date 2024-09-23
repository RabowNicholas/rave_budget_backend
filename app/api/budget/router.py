from datetime import datetime
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.contexts.budget.context import (
    BudgetContext,
    BudgetData,
    BudgetDataEnum,
    BudgetLimitData,
    BudgetOverviewData,
)
from app.contexts.budget.repository import BudgetRepository
from app.database import get_db

budget_router = APIRouter()


class BudgetLimitRequest(BaseModel):
    category: str
    amount: float


class BudgetPostBudgetRequest(BaseModel):
    overview: BudgetOverviewData
    limits: list[BudgetLimitRequest]


class BudgetPostBudgetResponse(BaseModel):
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
        overview = BudgetOverviewData(
            name=req.overview.name,
            date=datetime.fromisoformat(req.overview.date),
            location=req.overview.location,
        )

        limits = [
            BudgetLimitData(
                category=BudgetDataEnum[l.category],
                amount=l.amount,
            )
            for l in req.limits
        ]

        return BudgetData(overview=overview, limits=limits)
    except Exception as e:
        raise ValueError("Error parsing budget request data") from e
