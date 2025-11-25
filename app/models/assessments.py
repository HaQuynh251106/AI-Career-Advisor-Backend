
from beanie import Document, Indexed, Link
from typing import Optional, List, Any

class Assessment(Document):
    title: Indexed(str)
    description: Optional[str] = None
    assessment_type: str # "quiz", "coding_test", "personality"
    questions: List[Any] = [] # Cấu trúc linh hoạt cho các câu hỏi

    class Settings:
        name = "assessments"
