from beanie import Document, Indexed
from pydantic import Field
from typing import List, Optional, Any
from datetime import datetime

class JobListing(Document):
    # Các trường khớp với ảnh Database của bạn
    job_id: Indexed(str, unique=True)
    title: str
    company: str
    location: str
    employment_type: Optional[str] = None
    
    # QUAN TRỌNG: Trong DB bạn lưu là 'category_code', không phải 'job_category_id'
    category_code: str  
    
    # DB của bạn lưu salary_range là Object, nhưng ta tạm để Any hoặc Dict để tránh lỗi
    salary_range: Optional[Any] = None 
    
    skills_required: List[str] = []
    description: str
    
    posted_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

    class Settings:
        name = "job_listings"