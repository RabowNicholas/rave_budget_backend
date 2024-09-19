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


class UsersGetUserResponse(BaseModel):
    id: str
    onboarded: bool


@user_router.get("/{phone}")
async def get_user(
    phone: str, session: Session = Depends(get_db)
) -> UsersGetUserResponse:
    try:
        user_context = UserContext(UserRepository(session))
        user: User | None = user_context.user_exists_by_phone(phone=phone)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UsersGetUserResponse(
            id=user.id,
            onboarded=user.name is not None,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class UsersPutOnboardUserRequest(BaseModel):
    phone: str
    name: str


class UsersPutOnboardUserResponse(BaseModel):
    pass


@user_router.put("/onboard")
async def onboard_user(
    req: UsersPutOnboardUserRequest, session: Session = Depends(get_db)
) -> UsersPutOnboardUserResponse:
    try:
        user_context = UserContext(UserRepository(session))
        user: User | None = user_context.user_exists_by_phone(phone=req.phone)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_context.onboard_user(user=user, name=req.name)
        return UsersPutOnboardUserResponse()

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
