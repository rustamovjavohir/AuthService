from app.db.domain.base import DateTimeMixin, IdMixin
from app.schemas.base import RWSchema
from pydantic import EmailStr
from app.db.domain.users import User, Role


class UserInCreate(RWSchema):
    username: str
    first_name: str
    last_name: str | None = None
    email: EmailStr
    password: str


class UserUpdate(RWSchema):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserInLogin(RWSchema):
    username: str
    password: str


class UserOutLogin(RWSchema):
    token: str


class UserInUpdate(RWSchema):
    username: str
    email: EmailStr
    password: str


class UserResponse(User, DateTimeMixin, IdMixin):
    role: list[Role] | None = None


class UserList(RWSchema):
    users: list[User]


class TokenData(RWSchema):
    id: int
    username: str


class Token(RWSchema):
    access_token: str
    token_type: str


class ChangePasswordIn(RWSchema):
    current_password: str
    new_password: str
    confirm_password: str


class ChangePasswordOut(RWSchema):
    token: Token
