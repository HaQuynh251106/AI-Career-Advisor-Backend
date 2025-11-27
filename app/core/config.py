from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

class Settings(BaseSettings):
    # --- THÊM DÒNG NÀY ĐỂ SỬA LỖI ---
    API_V1_STR: str = "/api/v1"

    # Cấu hình CSDL MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/ai-career-advisor")
    
    # Cấu hình bảo mật JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bb5cdbe9232ca95da51aa98c4184c50ee9c7fff100fb975a285422155e4def8e")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    
    # Cấu hình AI (Gemini)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyDHs_J1sQ34UAoQRCVrSQut88AZkYvMspQ")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    class Config:
        case_sensitive = True
        
settings = Settings()