from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.api.api import api_router
from app.core.config import settings

# --- IMPORT TẤT CẢ CÁC MODEL CỦA BẠN VÀO ĐÂY ---
# Nếu thiếu model nào, Beanie sẽ báo lỗi "CollectionWasNotInitialized"
from app.models.user import User
from app.models.ai_recommendations import AIRecommendation
from app.models.job_listings import JobListing
from app.models.job_seekers import JobSeeker
from app.models.applications import Application
from app.models.skills import Skill
from app.models.job_categories import JobCategory
# -----------------------------------------------

# Hàm khởi động và tắt Database (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Khởi động: Kết nối MongoDB
    print("Starting up... Connecting to MongoDB.")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    
    # 2. Khởi tạo Beanie với danh sách Models
    await init_beanie(
        database=client.get_database(), # Tự lấy tên DB từ MONGO_URI
        document_models=[
            User,
            AIRecommendation, # <-- Cái này quan trọng để sửa lỗi của bạn
            JobListing,
            JobSeeker,
            Application,
            Skill,
            JobCategory
        ],
    )
    print("Database initialized successfully with all models.")
    
    yield
    
    # 3. Tắt: Đóng kết nối (nếu cần)
    print("Shutting down...")

# Khởi tạo ứng dụng FastAPI với lifespan
app = FastAPI(
    title="AI Career Advisor Backend",
    description="API cho hệ thống Tư vấn Nghề nghiệp AI sử dụng FastAPI và MongoDB.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan # Gắn hàm lifespan vào đây
)

# Cấu hình CORS
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

# Thêm router chính
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "AI Career Advisor API is running! Truy cập /docs để xem tài liệu."}