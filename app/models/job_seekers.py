from beanie import Document, Indexed
from pydantic import Field
from typing import List, Optional, Any
from datetime import datetime
# Import kiểu dữ liệu ObjectId đặc biệt của Beanie
from beanie import PydanticObjectId 

class JobSeeker(Document):
    # SỬA: Dùng PydanticObjectId để khớp với MongoDB
    user_id: Indexed(PydanticObjectId)
    
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    career_goal: Optional[str] = None
    
    # Kinh nghiệm là danh sách chuỗi
    experience: List[str] = [] 
    
    skills: List[str] = []
    
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "job_seekers"