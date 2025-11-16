
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatMessage
from app.services.ai_advisor import ai_advisor_service
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.ai_recommendations import AIRecommendation
from beanie.operators import In
from typing import List

router = APIRouter()

@router.post("/advice", response_model=ChatMessageResponse)
async def get_ai_advice(
    chat_request: ChatMessageRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Endpoint nhận tin nhắn từ người dùng và trả về phản hồi từ AI Career Advisor.
    """
    
    # 1. Gọi AI Service để nhận câu trả lời
    ai_response_text, updated_history_dict = await ai_advisor_service.get_advice(
        history=[msg.model_dump() for msg in chat_request.history], # Chuyển schema sang dict
        new_message=chat_request.message
    )
    
    # 2. Lưu lịch sử chat (tin nhắn user và tin nhắn AI) vào CSDL
    try:
        # Lấy tin nhắn người dùng cuối cùng
        user_prompt = chat_request.message
        
        # Lưu prompt
        user_prompt_record = AIRecommendation(
            user_id=current_user,
            type="chat_prompt",
            prompt=user_prompt
        )
        await user_prompt_record.insert()
        
        # Lưu response
        ai_response_record = AIRecommendation(
            user_id=current_user,
            type="chat_response",
            response=ai_response_text
        )
        await ai_response_record.insert()
        
    except Exception as e:
        # Log lỗi nếu không lưu được vào DB, nhưng vẫn trả về kết quả AI
        print(f"Error saving chat history to DB: {e}")

    # Chuyển đổi lại updated_history (list of dict) sang list of ChatMessage schema
    history_schema = [ChatMessage(**msg) for msg in updated_history_dict]

    return ChatMessageResponse(
        user_id=str(current_user.id),
        response=ai_response_text,
        history=history_schema
    )

@router.get("/history", response_model=List[ChatMessage])
async def get_chat_history(
    current_user: User = Depends(get_current_active_user)
):
    """
    Tải lịch sử chat của người dùng (chỉ tải prompt và response).
    """
    history_records = await AIRecommendation.find(
        AIRecommendation.user_id.id == current_user.id, # Lọc theo user_id
        In(AIRecommendation.type, ["chat_prompt", "chat_response"]) # Chỉ lấy 2 loại
    ).sort("timestamp").to_list() # Sắp xếp theo thời gian

    history_chat_format = []
    for record in history_records:
        if record.type == "chat_prompt" and record.prompt:
            history_chat_format.append(
                ChatMessage(role="user", parts=[{"text": record.prompt}])
            )
        elif record.type == "chat_response" and record.response:
             history_chat_format.append(
                ChatMessage(role="model", parts=[{"text": record.response}])
            )
            
    return history_chat_format
