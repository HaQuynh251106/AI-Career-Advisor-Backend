from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.api import deps
from app.models.learning_resources import LearningResource
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

# --- 1. ĐỊNH NGHĨA DỮ LIỆU GỬI LÊN (SCHEMA) ---
class LearningResourceCreate(BaseModel):
    title: str
    description: str
    type: str  # "video", "article", "course"
    url: str
    difficulty: str # "beginner", "intermediate", "advanced"
    topics: List[str] = [] # Ví dụ: ["Python", "React"]

# --- 2. API LẤY DANH SÁCH (GET) ---
@router.get("/", response_model=List[LearningResource])
async def get_learning_resources(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Lấy danh sách tài liệu học tập
    """
    search_criteria = {}
    
    # Lọc theo chủ đề (VD: Python, React, Interview...)
    if topic and topic != "all":
        # Tìm trong mảng topics
        search_criteria["topics"] = {"$in": [topic]}
        
    # Lọc theo độ khó (beginner, intermediate, advanced)
    if difficulty and difficulty != "all":
        search_criteria["difficulty"] = difficulty

    # Query database
    resources = await LearningResource.find(search_criteria).to_list()
    return resources

# --- 3. API TẠO MỚI (POST) - ĐÃ BỔ SUNG ---
@router.post("/")
async def create_learning_resource(
    data: LearningResourceCreate,
    current_user: User = Depends(deps.get_current_user)
):
    """Tạo mới một tài liệu học tập"""
    # Tạo object từ dữ liệu gửi lên
    resource = LearningResource(**data.dict())
    
    # Lưu vào Database
    await resource.insert()
    
    return {"message": "Thêm tài liệu thành công!", "data": resource}