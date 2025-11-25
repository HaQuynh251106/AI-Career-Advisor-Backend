
from fastapi import APIRouter
from app.api.endpoints import auth, user, chat
from app.api.endpoints import jobs, job_seekers, applications, common

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Career Advisor"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs Listing"])
api_router.include_router(job_seekers.router, prefix="/job-seekers", tags=["Job Seekers Profile"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(common.router, prefix="/common", tags=["Common Data"])

# (Bạn sẽ thêm các router khác cho job_listings, appointments... ở đây)
