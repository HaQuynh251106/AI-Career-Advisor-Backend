
from beanie import Document, Link, Indexed
from pydantic import Field
from datetime import datetime
from app.models.user import User
from app.models.assessments import Assessment
from typing import Any, Dict

class TestResult(Document):
    user_id: Link[User]
    assessment_id: Link[Assessment]
    score: float
    results_details: Dict[str, Any] = Field(default_factory=dict)
    completed_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "test_results"
