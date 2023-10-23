from pydantic import EmailStr
from app.db.domain.base import RWModel, DateTimeMixin
from app.services import security
from app.utils.choices import UserRoleChoices


class Role(RWModel):
    name: UserRoleChoices = UserRoleChoices.VIEWER
    description: str | None = None


class User(RWModel):
    username: str
    first_name: str
    last_name: str | None = None
    email: EmailStr
    is_active: bool = True


class UserInDB(User):
    password: str
    is_active: bool = True

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.password = security.get_password_hash(password)
