from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api import deps
from app.models.applications import Application
from app.models.job_listings import JobListing
from app.models.user import User
from datetime import datetime

router = APIRouter()

class ApplyRequest(BaseModel):
    job_id: str
    cover_letter: str = ""

@router.post("/apply")
async def apply_job(
    data: ApplyRequest,
    current_user: User = Depends(deps.get_current_user)
):
    # 1. Kiểm tra job có tồn tại không
    job = await JobListing.get(data.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Công việc không tồn tại")

    # 2. Kiểm tra xem đã nộp chưa (Dùng Dictionary Query cho an toàn)
    existing_app = await Application.find_one({
        "user_id": str(current_user.id),
        "job_id": data.job_id
    })
    
    if existing_app:
        raise HTTPException(status_code=400, detail="Bạn đã ứng tuyển công việc này rồi")

    # 3. Tạo đơn ứng tuyển mới
    try:
        new_app = Application(
            user_id=str(current_user.id),
            job_id=data.job_id,
            cover_letter=data.cover_letter,
            status="Đang chờ duyệt",
            applied_at=datetime.now()
        )
        await new_app.insert()
    except Exception as e:
        print(f"Lỗi DB: {e}")
        raise HTTPException(status_code=500, detail="Lỗi lưu đơn ứng tuyển")
        
    return {"message": "Ứng tuyển thành công!"}

@router.get("/my-applications")
async def get_my_applications(
    current_user: User = Depends(deps.get_current_user)
):
    # Tìm các đơn của user này (Dùng Dictionary Query)
    apps = await Application.find({
        "user_id": str(current_user.id)
    }).sort("-applied_at").to_list()
    
    # Map thêm thông tin Job Title
    result = []
    for app in apps:
        # Lấy thông tin job
        job = await JobListing.get(app.job_id)
        
        app_dict = app.dict()
        # Chuyển id thành string để frontend dễ dùng
        if "_id" in app_dict:
            app_dict["_id"] = str(app_dict["_id"])
            
        if job:
            app_dict["job_title"] = job.title
            app_dict["company"] = job.company
            app_dict["location"] = job.location
        else:
            app_dict["job_title"] = "Công việc không còn tồn tại"
            app_dict["company"] = "N/A"
            
        result.append(app_dict)
        
    return result