
from beanie import Document, Link, Indexed
from pydantic import HttpUrl
from typing import List, Optional
from app.models.skills import Skill

class LearningResource(Document):
    title: str
    url: HttpUrl
    description: Optional[str] = None
    resource_type: str # "course", "article", "video"
    related_skills: List[Link[Skill]] = []

    class Settings:
        name = "learning_resources"
