from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from fastapi.responses import JSONResponse, RedirectResponse, Response

from app.schemas.email import ChangeEmailOut
from app.services.users import UsersService
from app.api.dependencies.db import get_service
from app.services.users import get_current_user

router = APIRouter()


@router.put(
    "/input",
    response_model=ChangeEmailOut,
    name="auth:input-email"
)
async def input_email(
        email: EmailStr,
        current_user=Depends(get_current_user),
        user_service: UsersService = Depends(get_service(UsersService))
):
    current_user.email = email
    # user_service.check_user_attrs(current_user.id, **{"email": email})
    user_service.update_user(current_user.id, current_user)
    return ChangeEmailOut(email=email)


@router.get(
    "/verify",
    response_model=str,
    name="auth:verify"
)
async def verify(
        token: str,
        user_service=Depends(get_service(UsersService)),
):

    return {"token": token}
