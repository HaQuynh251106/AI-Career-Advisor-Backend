from typing import List, Optional
from beanie import Document
from pydantic import BaseModel

class Advisor(Document):
    name: str
    title: str          # Ví dụ: Senior Fullstack Developer
    skills: List[str]   # Ví dụ: ["ReactJS", "Python"]
    avatar: Optional[str] = None
    bio: Optional[str] = None
    rating: Optional[float] = 5.0
    
    class Settings:
        name = "advisors"  # Tên collection trong MongoDB