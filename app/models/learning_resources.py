from beanie import Document, Indexed
from pydantic import Field
from typing import List, Optional
from datetime import datetime

class LearningResource(Document):
    title: Indexed(str)
    description: str
    
    # --- SỬA Ở ĐÂY: Đổi resource_type thành type ---
    type: str  # "video", "article", "course"
    # -----------------------------------------------
    
    url: str
    difficulty: str # "beginner", "intermediate", "advanced"
    topics: List[str] = []
    
    # Các trường phụ
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "learning_resources"