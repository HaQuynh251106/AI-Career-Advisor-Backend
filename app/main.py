
from fastapi import FastAPI
from app.api.api import api_router
from app.db.mongodb import initialize_db
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="AI Career Advisor Backend",
    description="API cho hệ thống Tư vấn Nghề nghiệp AI sử dụng FastAPI và MongoDB.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000",  # React development server
        "http://localhost:5173",  # Vite development server
        "http://127.0.0.1:5173",  # Vite development server
        # Thêm các domain khác nếu cần
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Cho phép tất cả headers
)

# Sự kiện khởi động: Kết nối CSDL
@app.on_event("startup")
async def startup_event():
    """Chạy khi ứng dụng khởi động."""
    print("Starting up... Connecting to MongoDB.")
    await initialize_db()
    print("Database initialized successfully.")

# Thêm router chính vào ứng dụng
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "AI Career Advisor API is running! Truy cập /api/v1/docs để xem tài liệu."}

# Để chạy ứng dụng (từ thư mục gốc):
# uvicorn app.main:app --reload
