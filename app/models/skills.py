
from beanie import Document, Link
from typing import Optional

class Skill(Document):
    name: Indexed(str, unique=True)
    description: Optional[str] = None

    class Settings:
        name = "skills"
