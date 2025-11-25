from fastapi import APIRouter
from typing import List
from app.models.advisors import Advisor  # Import model vừa tạo ở Bước 1

router = APIRouter()

# API này sẽ trả về danh sách các Advisor lấy trực tiếp từ MongoDB
@router.get("/", response_model=List[Advisor])
async def get_advisors():
    # Lệnh tìm tất cả bản ghi trong collection 'advisors'
    advisors_list = await Advisor.find_all().to_list()
    return advisors_list