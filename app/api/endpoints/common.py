from fastapi import APIRouter
from app.models.skills import Skill
from app.models.job_categories import JobCategory

router = APIRouter()

@router.get("/skills")
async def get_all_skills():
    """Lấy danh sách kỹ năng để hiển thị gợi ý"""
    return await Skill.find_all().to_list()

@router.get("/categories")
async def get_job_categories():
    """Lấy danh sách ngành nghề cho dropdown tìm kiếm"""
    return await JobCategory.find_all().to_list()