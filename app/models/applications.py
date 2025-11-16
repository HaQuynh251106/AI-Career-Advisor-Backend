
from beanie import Document, Link, Indexed
from pydantic import Field
from datetime import datetime
from app.models.job_listings import JobListing
from app.models.job_seekers import JobSeeker

class Application(Document):
    job_listing_id: Link[JobListing]
    job_seeker_id: Link[JobSeeker]
    status: Indexed(str) = Field(default="applied") # applied, reviewed, rejected, accepted
    applied_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "applications"
