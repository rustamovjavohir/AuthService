from sqlalchemy import Column, String, Boolean, ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship
# from sqlalchemy_utils import ChoiceType
from sqlalchemy_utils.types.choice import ChoiceType
from app.db.models.base import BaseModel
from enum import Enum

from app.utils.choices import UserRoleChoices


class UserRole(BaseModel):
    __tablename__ = "user_roles"

    name = Column(String(250), default=UserRoleChoices.VIEWER)
    # name = Column(ChoiceType(UserRoleChoices, impl=String()), unique=True, default=UserRoleChoices.VIEWER)
    description = Column(String(250), nullable=True)

    user_id = Column(BigInteger, ForeignKey("users.id"))
    users = relationship("User", back_populates="role")

    __table_args__ = (
        UniqueConstraint('name', 'user_id'),
    )


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(250), unique=True)
    first_name = Column(String(250), nullable=True)
    last_name = Column(String(250), nullable=True)
    email = Column(String, nullable=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    role = relationship("UserRole", back_populates="users")
