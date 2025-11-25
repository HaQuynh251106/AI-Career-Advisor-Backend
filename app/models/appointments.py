
from typing import Optional
from beanie import Document, Link, Indexed
from pydantic import Field
from datetime import datetime
from app.models.job_seekers import JobSeeker
from app.models.career_advisors import CareerAdvisor

class Appointment(Document):
    job_seeker_id: Link[JobSeeker]
    advisor_id: Link[CareerAdvisor]
    start_time: datetime
    end_time: datetime
    status: Indexed(str) = Field(default="pending") # pending, confirmed, completed, cancelled
    notes: Optional[str] = None

    class Settings:
        name = "appointments"
