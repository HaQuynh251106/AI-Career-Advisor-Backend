from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api import deps 
from app.models.job_seekers import JobSeeker
from app.models.user import User

router = APIRouter()

# Schema dữ liệu nhận từ Frontend (khớp với form bên React)
class JobSeekerUpdate(BaseModel):
    full_name: str
    phone: str
    address: str
    career_goal: str
    # Có thể thêm skills, experience nếu frontend gửi lên

@router.get("/me")
async def get_current_job_seeker_profile(
    current_user: User = Depends(deps.get_current_user)
):
    """
    Lấy thông tin hồ sơ chi tiết của user đang đăng nhập
    """
    # Tìm JobSeeker liên kết với user_id này
    profile = await JobSeeker.find_one(JobSeeker.user_id == current_user.id)
    
    if not profile:
        # Nếu chưa có hồ sơ thì trả về rỗng hoặc tạo mới tùy logic
        return {} 
        
    return profile

@router.put("/me")
async def update_job_seeker_profile(
    profile_data: JobSeekerUpdate,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Cập nhật hoặc Tạo mới hồ sơ CV
    """
    # 1. Tìm hồ sơ cũ
    profile = await JobSeeker.find_one(JobSeeker.user_id == current_user.id)
    
    if profile:
        # 2. Nếu đã có -> Update
        # Update từng trường dữ liệu gửi lên
        profile.full_name = profile_data.full_name
        profile.phone = profile_data.phone
        profile.address = profile_data.address
        profile.career_goal = profile_data.career_goal
        
        await profile.save()
        return {"message": "Cập nhật hồ sơ thành công", "data": profile}
    else:
        # 3. Nếu chưa có -> Tạo mới (Create)
        new_profile = JobSeeker(
            user_id=current_user.id,
            **profile_data.dict() # Bung dữ liệu từ schema ra
        )
        await new_profile.insert()
        return {"message": "Tạo hồ sơ mới thành công", "data": new_profile}