
from beanie import Document, Link, Indexed
from typing import List, Optional
from app.models.job_categories import JobCategory
from app.models.skills import Skill

class JobListing(Document):
    title: str
    company_name: str
    description: str
    requirements: str
    location: str
    category: Link[JobCategory]
    required_skills: List[Link[Skill]] = []
    is_active: bool = True

    class Settings:
        name = "job_listings"
