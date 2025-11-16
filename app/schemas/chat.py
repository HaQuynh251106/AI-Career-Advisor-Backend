
from pydantic import BaseModel
from typing import List, Dict, Any

class ChatMessage(BaseModel):
    """Định nghĩa cấu trúc một tin nhắn trong lịch sử."""
    role: str # "user" hoặc "model"
    parts: List[Dict[str, Any]]

class ChatMessageRequest(BaseModel):
    # Lịch sử chat được gửi lên từ client để duy trì ngữ cảnh
    history: List[ChatMessage] = [] 
    message: str # Tin nhắn mới nhất

class ChatMessageResponse(BaseModel):
    user_id: str
    response: str
    # Trả về toàn bộ lịch sử đã cập nhật
    history: List[ChatMessage]
