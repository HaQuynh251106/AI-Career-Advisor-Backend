from beanie import Document, Indexed
from pydantic import Field
from typing import List, Optional, Any
from datetime import datetime

class JobListing(Document):
    job_id: Indexed(str, unique=True)
    title: str
    company: str
    location: str
    employment_type: Optional[str] = None
    category_code: str  
    salary_range: Optional[Any] = None 
    skills_required: List[str] = []
    description: str
    
    # --- THÊM TRƯỜNG NÀY (Để chứa vector) ---
    vector: Optional[List[float]] = None
    # ---------------------------------------
    
    posted_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

    class Settings:
        name = "job_listings"