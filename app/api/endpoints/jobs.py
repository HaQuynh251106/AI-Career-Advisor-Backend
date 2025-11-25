from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.api import deps 
from app.models.job_listings import JobListing # Import model của bạn
from app.models.user import User
from pydantic import BaseModel


router = APIRouter()

# Schema dữ liệu tạo việc làm (DTO)
class JobCreate(BaseModel):
    title: str
    description: str
    company: str
    location: str
    salary: str
    job_category_id: str
    required_skills: List[str] = []

@router.get("/", response_model=List[JobListing])
async def search_jobs(
    q: Optional[str] = None,
    category: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 20
):
    """API Tìm kiếm việc làm công khai (Public)"""
    search_criteria = {}
    
    if category and category != "all":
        search_criteria["job_category_id"] = category
    if location:
        search_criteria["location"] = location

    query = JobListing.find(search_criteria)
    
    if q:
        # Tìm kiếm regex không phân biệt hoa thường
        query = query.find({"title": {"$regex": q, "$options": "i"}})
        
    return await query.limit(limit).to_list()

@router.get("/{job_id}", response_model=JobListing)
async def get_job_detail(job_id: str):
    """Xem chi tiết một công việc"""
    job = await JobListing.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy công việc")
    return job

@router.post("/", response_model=JobListing)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(deps.get_current_user)
):
    """Đăng việc làm mới (Cần quyền Admin/Recruiter)"""
    # Logic kiểm tra quyền admin ở đây nếu cần
    new_job = JobListing(**job_data.dict(), posted_by=current_user.id)
    await new_job.insert()
    return new_job