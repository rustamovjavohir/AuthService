from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, List, Annotated

from fastapi.responses import JSONResponse, RedirectResponse, Response

from app.api.dependencies.db import get_db, get_service
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN_PREFIX
from app.db.domain.users import UserInDB, User, Role
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.schemas.users import UserResponse, UserList, UserInCreate, UserUpdate, UserInLogin, UserOutLogin, Token, \
    ChangePasswordOut, ChangePasswordIn
from app.services.security import oauth2_scheme
from app.services.users import UsersService, get_current_user, get_current_active_user
from app.utils import constants as const

router = APIRouter()


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    name="auth:login"
)
async def login(
        user: UserInLogin,
        user_service: UsersService = Depends(get_service(UsersService))
):
    user_db = user_service.get_user_by_username(user.username)
    if not user_db or not user_service.check_password(user_db, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=const.INCORRECT_LOGIN_INPUT
        )
    if not user_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=const.USER_NOT_FOUND
        )
    access_token = user_service.create_access_token(user_db)
    return Token(access_token=access_token, token_type=JWT_TOKEN_PREFIX)


@router.post(
    "/token",
    deprecated=True,
    response_model=Token
)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UsersService = Depends(get_service(UsersService))
):
    user_db = user_service.get_user_by_username(form_data.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(user_db, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": JWT_TOKEN_PREFIX}


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    name="users:get-current-user"
)
async def profile(
        current_user: User = Depends(get_current_active_user)
):
    return current_user


@router.post(
    "/role/{user_id}/create",
    response_model=Role,
)
async def create_role(
        user_id: int,
        role: Role,
        user_service: UsersService = Depends(get_service(UsersService))
):
    result = user_service.create_role(user_id, role)
    return result


@router.put(
    "/role/change_password",
    response_model=ChangePasswordOut,
)
async def change_password(
        password: Annotated[ChangePasswordIn, Body(...)],
        user_service: UsersService = Depends(get_service(UsersService)),
        current_user: User = Depends(get_current_active_user)
):
    return user_service.change_password(current_user.id, password)
