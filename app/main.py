from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.api.api import api_router
from app.core.config import settings

# --- IMPORT CÁC MODEL BEANIE (DATABASE) ---
from app.models.user import User
from app.models.ai_recommendations import AIRecommendation
from app.models.job_listings import JobListing
from app.models.job_seekers import JobSeeker
from app.models.applications import Application
from app.models.skills import Skill
from app.models.job_categories import JobCategory
from app.models.learning_resources import LearningResource
from app.models.assessments import Assessment
from app.models.test_results import TestResult
# (Lưu ý: Không import advisors ở đây vì advisors là API endpoint, không phải Model Database)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... Connecting to MongoDB.")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    
    await init_beanie(
        database=client.get_database(),
        document_models=[
            User,
            AIRecommendation,
            JobListing,
            JobSeeker,
            Application,
            Skill,
            JobCategory,
            LearningResource,
            Assessment,
            TestResult           
        ],
    )
    print("Database initialized successfully with all models.")
    
    yield
    
    print("Shutting down...")

app = FastAPI(
    title="AI Career Advisor Backend",
    description="API cho hệ thống Tư vấn Nghề nghiệp AI.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# --- QUAN TRỌNG: Dòng này gom tất cả API từ file api.py ---
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "AI Career Advisor API is running!"}