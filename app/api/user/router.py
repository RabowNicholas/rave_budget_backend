from fastapi import APIRouter, Depends, HTTPException
from fastapi_camelcase import CamelModel
from sqlalchemy.orm import Session

from app.contexts.user.context import UserContext, UserUpdateData
from app.contexts.user.models import User
from app.contexts.user.repo import UserRepository
from app.database import get_db


user_router = APIRouter()


class UsersPostUserResponse(CamelModel):
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
        raise HTTPException(status_code=500, detail=str(e)) from e


class UsersGetUserResponse(CamelModel):
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
        raise HTTPException(status_code=500, detail=str(e)) from e


class UsersGetUserByIdResponse(CamelModel):
    id: str
    name: str
    phone: str


@user_router.get("/id/{user_id}")
async def get_user_by_id(
    user_id: str, session: Session = Depends(get_db)
) -> UsersGetUserByIdResponse:
    try:
        user_context = UserContext(UserRepository(session))
        user: User = user_context.get_user_by_id(user_id=user_id)
        return UsersGetUserByIdResponse(
            id=user.id,
            name=user.name,
            phone=user.phone,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


class UpdateUserNameRequest(CamelModel):
    name: str


class UsersUpdateUserResponse(CamelModel):
    id: str
    name: str


@user_router.put("/id/{user_id}", response_model=UsersUpdateUserResponse)
async def update_user_name(
    user_id: str,
    req: UpdateUserNameRequest,
    session: Session = Depends(get_db),
) -> UsersUpdateUserResponse:
    try:
        user_context = UserContext(UserRepository(session))
        update_data = UserUpdateData()
        update_data.name = req.name
        user: User = user_context.update_user(
            user_id=user_id,
            update_data=update_data,
        )

        return UsersUpdateUserResponse(
            id=user.id,
            name=user.name,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


class UsersPutOnboardUserRequest(CamelModel):
    phone: str
    name: str


class UsersPutOnboardUserResponse(CamelModel):
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
        raise HTTPException(status_code=500, detail=str(e)) from e
