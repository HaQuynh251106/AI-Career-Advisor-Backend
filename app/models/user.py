
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional

class User(Document):
    full_name: Optional[str] = None
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    role: Indexed(str) = Field(default="job_seeker") # job_seeker, career_advisor, admin
    is_active: bool = Field(default=True)
    
    class Settings:
        name = "users"
