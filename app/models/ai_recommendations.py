from beanie import Document
from pydantic import Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from datetime import datetime
from typing import Optional, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.str_schema()

class AIRecommendation(Document):
    user_id: PyObjectId = Field(description="Reference to User document")
    timestamp: datetime = Field(default_factory=datetime.now)
    # Loại tương tác: "chat_prompt", "chat_response", "job_suggestion", "skill_gap"
    type: str = Field(default="chat_prompt")
    
    # Dùng cho chat
    prompt: Optional[str] = None
    response: Optional[str] = None
    
    class Settings:
        name = "ai_recommendations"
        indexes = [
            [("user_id", 1), ("timestamp", 1)],  # Compound index
            [("type", 1)]  # Single field index
        ]