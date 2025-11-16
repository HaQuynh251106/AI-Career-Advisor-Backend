
from beanie import Document, Link
from pydantic import Field, HttpUrl
from typing import Optional, List
from app.models.user import User

class JobSeeker(Document):
    user_id: Link[User]
    cv_url: Optional[HttpUrl] = None
    experience: List[str] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)
    career_goals: Optional[str] = None

    class Settings:
        name = "job_seekers"
