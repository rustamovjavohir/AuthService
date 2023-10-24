from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from app.api.dependencies.db import get_service
from app.core.config import SECRET_KEY, ALGORITHM, JWT_TOKEN_PREFIX
from sqlalchemy.orm import Session
from app.db.domain.users import UserInDB, Role
from app.db.models.users import User, UserRole
from app.schemas.users import UserInCreate, UserUpdate, TokenData, ChangePasswordIn, ChangePasswordOut, Token
from app.services import security
from app.services.base import BaseService
from app.services.security import get_password_hash, oauth2_scheme
from app.utils import constants as const
from app.utils.choices import UserRoleChoices


class UsersService(BaseService):

    def active_users(self):
        return self.db.query(User).filter(User.is_active is True)

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def list_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_active_user_by_id(self, user_id: int):
        return self.active_users().filter(User.id == user_id).first()

    def create_user(self, user: UserInCreate):
        user.password = get_password_hash(user.password)
        db_user = User(
            **user.dict(),
        )
        self.db.add(db_user)
        self.db.commit()
        return db_user

    def update_user(self, user_id: int, user: UserUpdate):
        db_user = self.get_user_by_id(user_id=user_id)
        for var, value in vars(user).items():
            if value:
                setattr(db_user, var, value)
        self.db.commit()
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id=user_id)
        db_user.is_active = False
        self.db.commit()
        return db_user

    def check_password(self, user: User, password: str) -> bool:
        return security.verify_password(password, user.password)

    def create_access_token(self, user: User, expires_delta: timedelta | None = None):
        """
        Create access token for user
        :param user:
        :param expires_delta:
        :return:
        """
        data = TokenData(id=user.id, username=user.username)
        return security.create_access_token(data=data.model_dump(), expires_delta=expires_delta)

    def get_user_by_token(self, token: str):
        """
        Get user by token
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
            payload.pop('exp')
            token_data = TokenData(**payload)
            if token_data.id is None:
                return None
        except JWTError:
            return None
        user = self.get_user_by_id(user_id=token_data.id)
        if user is None:
            return None
        return user

    def check_role(self, user_id: int):
        role_exists = self.db.query(UserRole).filter(UserRole.user_id == user_id).first()
        return role_exists

    def get_user_or_raise_error(self, db_user):
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=const.USER_NOT_FOUND
            )
        return db_user

    def create_role(self, user_id, role: Role):
        db_user = self.get_user_by_id(user_id=user_id)
        self.get_user_or_raise_error(db_user)
        if self.check_role(user_id=user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=const.ROLE_EXISTS
            )
        db_role = UserRole(**role.model_dump(), user_id=db_user.id)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def change_password(self, user_id: int, password: ChangePasswordIn):
        db_user = self.get_user_by_id(user_id=user_id)
        self.get_user_or_raise_error(db_user)
        if password.new_password != password.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=const.PASSWORD_NOT_MATCH
            )

        if not self.check_password(db_user, password.current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=const.INCORRECT_PASSWORD
            )
        db_user.password = get_password_hash(password.new_password)
        self.db.commit()
        self.db.refresh(db_user)

        # return self.create_access_token(db_user)
        return ChangePasswordOut(
            token=Token(
                access_token=self.create_access_token(db_user),
                token_type=JWT_TOKEN_PREFIX
            )
        )

    def check_user_attrs(self, user_id, **kwargs):
        user = self.get_user_by_id(user_id=user_id)
        self.get_user_or_raise_error(user)
        for key, value in kwargs.items():
            if getattr(user, key) != value:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=const.USER_INFORMATION_DOES_NOT_MATCH
                )
        return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           user_service: UsersService = Depends(get_service(UsersService))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        payload.pop('exp')
        token_data = TokenData(**payload)
        if token_data.id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.get_user_by_id(user_id=token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
