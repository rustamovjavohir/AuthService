from fastapi import APIRouter

from app.api.routers import users, authentication

router = APIRouter()

router.include_router(users.router, tags=["users"], prefix="/user")
router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
