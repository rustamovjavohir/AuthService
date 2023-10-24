from fastapi import APIRouter

from app.api.routers import users, authentication, email

router = APIRouter()

router.include_router(users.router, tags=["users"], prefix="/user")
router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(email.router, tags=["email"], prefix="/email")
