from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional

class AIRecommendation(Document):
    # Dùng string cho đơn giản, tránh lỗi PydanticObjectId
    user_id: Indexed(str)
    
    type: str 
    prompt: Optional[str] = None
    response: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "ai_recommendations"