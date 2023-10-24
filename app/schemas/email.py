from app.schemas.base import RWSchema


class EmailSchema(RWSchema):
    email: str
    subject: str | None = None
    message: str | None = None


class EmailVerifySchema(RWSchema):
    token: str


class ChangeEmailOut(RWSchema):
    email: str
