from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.contexts.user.context import UserContext
from app.contexts.user.models import User
from app.contexts.user.repo import UserRepository
from app.database import get_db


user_router = APIRouter()


class UsersPostUserResponse(BaseModel):
    id: str


@user_router.post("/{phone}")
async def post_user(
    phone: str, session: Session = Depends(get_db)
) -> UsersPostUserResponse:
    try:
        user_context = UserContext(UserRepository(session))
        user: User | None = user_context.user_exists_by_phone(phone=phone)
        if not user:
            user = user_context.create_user(phone=phone)
        return UsersPostUserResponse(id=user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
