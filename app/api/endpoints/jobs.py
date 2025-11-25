from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.job_listings import JobListing

router = APIRouter()

@router.get("/", response_model=List[JobListing])
async def search_jobs(
    q: Optional[str] = None,
    category: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 20
):
    """
    Tìm kiếm việc làm khớp với cấu trúc Database thực tế
    """
    search_criteria = {}
    
    # 1. Xử lý bộ lọc NGÀNH NGHỀ
    if category and category != "all":
        # Frontend gửi 'it', DB lưu 'IT' -> Cần .upper()
        # DB dùng field 'category_code'
        search_criteria["category_code"] = category.upper()

    # 2. Xử lý bộ lọc ĐỊA ĐIỂM
    if location:
        # Tìm gần đúng địa điểm (regex)
        search_criteria["location"] = {"$regex": location, "$options": "i"}

    # 3. Tạo Query
    query = JobListing.find(search_criteria)
    
    # 4. Xử lý tìm kiếm TỪ KHÓA (Title hoặc Company)
    if q:
        query = query.find({"$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"company": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}}
        ]})
        
    # Chỉ lấy các job đang active
    query = query.find({"is_active": True})

    results = await query.limit(limit).to_list()
    return results