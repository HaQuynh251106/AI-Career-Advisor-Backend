
from beanie import Document, Indexed
from typing import Optional

class JobCategory(Document):
    name: Indexed(str, unique=True)
    description: Optional[str] = None

    class Settings:
        name = "job_categories"
