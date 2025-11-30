from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Tiền tố API
    API_V1_STR: str = "/api/v1"

    # Các biến này sẽ tự động đọc từ file .env nếu trùng tên
    MONGO_URI: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # AI Config
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    class Config:
        # Chỉ định file chứa biến môi trường
        env_file = ".env"
        case_sensitive = True

settings = Settings()