from enum import Enum


class UserRoleChoices(str, Enum):
    VIEWER = "viewer"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
