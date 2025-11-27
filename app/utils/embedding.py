import google.generativeai as genai
from app.core.config import settings

# Cấu hình API Key (Lấy từ Config)
genai.configure(api_key=settings.GEMINI_API_KEY)

def get_embedding(text: str) -> list[float]:
    """
    Chuyển đổi văn bản thành Vector sử dụng Google Gemini Embedding
    """
    try:
        # Dùng model chuyên để tạo embedding
        result = genai.embed_content(
            model="models/text-embedding-004", # Hoặc "models/embedding-001"
            content=text,
            task_type="retrieval_document",
            title="Embedding of job description"
        )
        return result['embedding']
    except Exception as e:
        print(f"Lỗi tạo vector: {e}")
        return []