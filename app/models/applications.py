from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional

class Application(Document):
    # --- BỔ SUNG CÁC TRƯỜNG CÒN THIẾU ---
    user_id: Indexed(str)
    job_id: Indexed(str)
    # ------------------------------------
    
    cover_letter: Optional[str] = None
    status: str = "Đang chờ duyệt" # pending, reviewed, accepted, rejected
    applied_at: datetime = Field(default_factory=datetime.now)
    
    # Các thông tin phụ (nếu cần)
    resume_link: Optional[str] = None

    class Settings:
        name = "applications"