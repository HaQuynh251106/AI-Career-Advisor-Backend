
from fastapi import APIRouter
from app.api.endpoints import auth, user, chat

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Career Advisor"])

# (Bạn sẽ thêm các router khác cho job_listings, appointments... ở đây)
