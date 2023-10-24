from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any, List, Annotated

from fastapi.responses import JSONResponse, RedirectResponse, Response

from app.api.dependencies.db import get_db, get_service
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN_PREFIX
from app.db.domain.users import UserInDB, User
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.schemas.users import UserResponse, UserList, UserInCreate, UserUpdate, UserInLogin, UserOutLogin, Token
from app.services.security import oauth2_scheme
from app.services.users import UsersService, get_current_user, get_current_active_user
from app.utils import constants as const

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    name="auth:register"
)
async def register(
        user: UserInCreate,
        user_service: UsersService = Depends(get_service(UsersService))
):
    if user_service.get_user_by_username(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=const.USERNAME_TAKEN)
    user = user_service.create_user(user)
    return user


@router.get(
    "/list",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    name="users:list-users"
)
async def get_users(
        skip: int = 0,
        limit: int = 100,
        user_service: UsersService = Depends(get_service(UsersService))
):
    users = user_service.list_users(skip, limit)
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    name="users:get-user-by-id"
)
async def get_user_retrieve(
        user_id: int,
        user_service: UsersService = Depends(get_service(UsersService)),
):
    user_db = user_service.get_user_by_id(user_id=user_id)
    user_service.get_user_or_raise_error(user_db)
    return user_db


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    name="users:update-user"
)
async def update_user(
        user_id: int,
        user: UserUpdate,
        user_service: UsersService = Depends(get_service(UsersService)),
):
    user_db = user_service.get_user_by_id(user_id=user_id)
    user_service.get_user_or_raise_error(user_db)
    if user_service.get_user_by_username(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=const.USERNAME_TAKEN)
    user_db = user_service.update_user(user_id=user_id, user=user)
    return user_db


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    name="users:delete-user"
)
async def delete_user(
        user_id: int,
        user_service: UsersService = Depends(get_service(UsersService)),
) -> Response:
    user_db = user_service.get_user_by_id(user_id=user_id)
    user_service.get_user_or_raise_error(user_db)
    user_service.delete_user(user_id=user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': const.USER_SUCCESSFULLY_DELETED})
