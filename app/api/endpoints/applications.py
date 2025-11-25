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
    """Nộp đơn ứng tuyển vào một công việc"""
    # 1. Kiểm tra job có tồn tại không
    job = await JobListing.get(data.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Công việc không tồn tại")

    # 2. Kiểm tra xem đã ứng tuyển chưa (tránh spam)
    existing_app = await Application.find_one(
        Application.user_id == current_user.id,
        Application.job_id == data.job_id
    )
    if existing_app:
        raise HTTPException(status_code=400, detail="Bạn đã ứng tuyển công việc này rồi")

    # 3. Tạo đơn ứng tuyển
    new_app = Application(
        user_id=current_user.id,
        job_id=data.job_id,
        cover_letter=data.cover_letter,
        status="pending",
        applied_at=datetime.now()
    )
    await new_app.insert()
    return {"message": "Ứng tuyển thành công!"}

@router.get("/my-applications")
async def get_my_applications(current_user: User = Depends(deps.get_current_user)):
    """Xem danh sách các việc mình đã ứng tuyển"""
    # Có thể cần fetch thêm thông tin Job title để hiển thị (tùy model bạn thiết kế)
    apps = await Application.find(Application.user_id == current_user.id).to_list()
    return apps