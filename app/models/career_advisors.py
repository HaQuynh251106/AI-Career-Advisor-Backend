
from beanie import Document, Indexed, Link
from pydantic import Field
from typing import Optional, List
from app.models.user import User

class CareerAdvisor(Document):
    user_id: Link[User]
    specialization: List[str] = Field(default_factory=list)
    bio: Optional[str] = None
    availability: Optional[str] = None # Có thể là cấu trúc JSON phức tạp
    rating: float = Field(default=0.0)

    class Settings:
        name = "career_advisors"
        