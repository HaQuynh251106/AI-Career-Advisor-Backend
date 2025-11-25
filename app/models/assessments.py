from beanie import Document
from pydantic import Field
from typing import List, Optional
from datetime import datetime

class Assessment(Document):
    title: str
    description: str
    type: str = "skill_assessment" 
    
    questions: List[dict] = [] 
    difficulty: str = "beginner"
    
    # --- SỬA ĐOẠN NÀY ---
    # Thêm Optional để chấp nhận trường hợp DB lưu là null
    score: Optional[int] = None
    max_score: Optional[int] = 100 
    result: Optional[str] = None 
    # --------------------
    
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "assessments"