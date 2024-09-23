from fastapi import APIRouter, Header
from pydantic import BaseModel

from app.contexts.user.models import User


budget_router = APIRouter()


class BudgetPostBudgetRequest(BaseModel):
    pass


@budget_router.post("")
async def post_budget(
    req: BudgetPostBudgetRequest,
    user_id: str = Header(),
):
    print(user_id)
