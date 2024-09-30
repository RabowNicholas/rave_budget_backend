from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session


from app.contexts.interest.context import InterestContext
from app.contexts.interest.repo import InterestRepository
from app.database import get_db


interest_router = APIRouter()

interest_router.post("/feature/{name}")


async def post_feature_interest(
    name: str,
    user_id: str = Header(),
    session: Session = Depends(get_db),
) -> None:
    interest_context = InterestContext(InterestRepository(session))
    interest_context.add_feature_interest(user_id, name)
