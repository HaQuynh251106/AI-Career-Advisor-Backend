from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from app.api import deps 
from app.models.user import User
from app.models.ai_recommendations import AIRecommendation

router = APIRouter()

# --- CẤU HÌNH API KEY ---
MY_API_KEY = "AIzaSyCHoPkD3RU1XVdpsMcjf40ngiuzAfPfEt8" 

try:
    genai.configure(api_key=MY_API_KEY)
    print(f"✅ Đã nạp API Key thành công.")
except Exception as e:
    print(f"❌ Lỗi nạp Key: {e}")

# --- SỬA Ở ĐÂY: Đổi sang gemini-1.5-pro ---
model = genai.GenerativeModel('gemini-2.5-flash')
# ------------------------------------------

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/advice", response_model=ChatResponse)
async def get_advice(
    chat_request: ChatRequest,
    current_user: User = Depends(deps.get_current_user)
):
    try:
        # 1. Gọi AI
        prompt = f"User: {chat_request.message}"
        ai_response = model.generate_content(prompt)
        ai_text = ai_response.text

        # 2. Lưu DB
        try:
            await AIRecommendation(
                user_id=str(current_user.id),
                type="chat_prompt",
                prompt=chat_request.message
            ).insert()
            
            await AIRecommendation(
                user_id=str(current_user.id),
                type="chat_response",
                response=ai_text
            ).insert()
        except Exception as db_e:
            print(f"⚠️ Lỗi lưu DB: {db_e}")

        return {"response": ai_text}

    except Exception as e:
        print(f"❌ Lỗi Gemini: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi AI: {str(e)}")

@router.get("/history")
async def get_chat_history(
    current_user: User = Depends(deps.get_current_user)
):
    history_records = await AIRecommendation.find(
        {"user_id": str(current_user.id)}
    ).sort("+timestamp").to_list()

    formatted_history = []
    for record in history_records:
        if record.type == "chat_prompt" and record.prompt:
            formatted_history.append({"role": "user", "content": record.prompt})
        elif record.type == "chat_response" and record.response:
            formatted_history.append({"role": "ai", "content": record.response})
            
    return formatted_history

# # --- DÁN VÀO CUỐI CÙNG FILE chat.py ---
# print("\n================ KIỂM TRA MODEL GEMINI ================")
# try:
#     print("Đang hỏi Google xem có những model nào...")
#     for m in genai.list_models():
#         # Chỉ in ra các model hỗ trợ chat (generateContent)
#         if 'generateContent' in m.supported_generation_methods:
#             print(f"👉 FOUND MODEL: {m.name}")
# except Exception as e:
#     print(f"❌ Lỗi khi lấy danh sách: {e}")
# print("=======================================================\n")