
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Tải biến môi trường từ file .env
load_dotenv()

class Settings(BaseSettings):
    # Cấu hình CSDL MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/aicareerdb")
    
    # Cấu hình bảo mật JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bb5cdbe9232ca95da51aa98c4184c50ee9c7fff100fb975a285422155e4def8e")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Cấu hình AI (Gemini)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyCHoPkD3RU1XVdpsMcjf40ngiuzAfPfEt8")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    class Config:
        case_sensitive = True
        
settings = Settings()
