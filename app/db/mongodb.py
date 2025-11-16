
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

# Import tất cả các Models (Documents)
from app.models.user import User
from app.models.job_seekers import JobSeeker
from app.models.career_advisors import CareerAdvisor
from app.models.skills import Skill
from app.models.job_categories import JobCategory
from app.models.appointments import Appointment
from app.models.ai_recommendations import AIRecommendation
from app.models.learning_resources import LearningResource
from app.models.job_listings import JobListing
from app.models.applications import Application
from app.models.assessments import Assessment
from app.models.test_results import TestResult

# Khởi tạo kết nối client
try:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    # Lấy database từ URI, hoặc chỉ định tên
    db_name = client.get_default_database().name
    if not db_name:
         # Nếu URI không chỉ định DB (ví dụ: chỉ có localhost:27017)
         db_name = "aicareerdb" 
         
    database = client[db_name]
    print(f"Connecting to MongoDB database: {db_name}")

except Exception as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)


# Danh sách tất cả các Beanie Document (Models) bạn định nghĩa
DOCUMENT_MODELS = [
    User,
    JobSeeker,
    CareerAdvisor,
    Skill,
    JobCategory,
    Appointment,
    AIRecommendation,
    LearningResource,
    JobListing,
    Application,
    Assessment,
    TestResult
]

async def initialize_db():
    """Khởi tạo kết nối Beanie và MongoDB."""
    try:
        await init_beanie(
            database=database,
            document_models=DOCUMENT_MODELS,
        )
    except Exception as e:
        print(f"Error initializing Beanie: {e}")
