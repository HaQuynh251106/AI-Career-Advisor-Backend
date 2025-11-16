
import httpx
import json
from typing import List, Dict, Any, Tuple
from app.core.config import settings

class AIAdvisorService:
    def __init__(self, model_name: str = settings.GEMINI_MODEL):
        self.model_name = model_name
        # API URL sử dụng GEMINI_API_KEY
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        self.system_instruction = (
            "Bạn là một Trợ lý Tư vấn Nghề nghiệp AI (AI Career Advisor) chuyên nghiệp, thân thiện "
            "và tận tâm. Nhiệm vụ của bạn là: 1) Phân tích kỹ năng, kinh nghiệm của người dùng. "
            "2) Đưa ra các lời khuyên về con đường sự nghiệp, kỹ năng cần học. "
            "3) Giới thiệu các cố vấn phù hợp từ hệ thống (nếu cần). "
            "4) Luôn trả lời ngắn gọn, trực tiếp và hữu ích. "
            "5) Luôn trả lời bằng Tiếng Việt."
        )

    async def get_advice(self, history: List[Dict[str, Any]], new_message: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Gửi tin nhắn mới đến AI và nhận câu trả lời.
        Sử dụng httpx để gọi API bất đồng bộ.
        """
        
        # Thêm tin nhắn mới của người dùng vào lịch sử
        current_contents = history + [{
            "role": "user", 
            "parts": [{"text": new_message}]
        }]

        payload = {
            "contents": current_contents,
            "systemInstruction": {
                "parts": [{"text": self.system_instruction}]
            },
            # Kích hoạt Google Search để grounding (cung cấp thông tin thời gian thực)
            "tools": [{"google_search": {}}]
        }
        
        headers = {'Content-Type': 'application/json'}

        try:
            # Kiểm tra xem API Key đã được cung cấp chưa
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY chưa được cấu hình. Vui lòng kiểm tra file .env.")

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.api_url, headers=headers, data=json.dumps(payload))
                
                # Kiểm tra lỗi HTTP (ví dụ: 400 Bad Request, 401 Unauthorized, 403 Forbidden)
                response.raise_for_status() 
                
                api_response = response.json()
                
                # Xử lý response (kiểm tra block/lỗi từ Gemini)
                if not api_response.get("candidates"):
                     # Trường hợp bị block do safety settings hoặc lỗi khác
                    finish_reason = api_response.get("promptFeedback", {}).get("blockReason", "Unknown")
                    error_text = f"Xin lỗi, câu trả lời bị chặn. Lý do: {finish_reason}"
                    print(f"Gemini API Error: {error_text}")
                    return error_text, current_contents

                candidate = api_response.get("candidates", [{}])[0]
                ai_response_part = candidate.get("content", {}).get("parts", [{}])[0]
                ai_response_text = ai_response_part.get("text", "Xin lỗi, tôi không thể trả lời lúc này.")

                # Thêm câu trả lời của AI vào lịch sử
                updated_history = current_contents + [{
                    "role": "model",
                    "parts": [ai_response_part]
                }]
                
                return ai_response_text, updated_history

        except httpx.HTTPStatusError as e:
            error_detail = "Unknown API Error"
            try:
                error_detail = e.response.json().get("error", {}).get("message", "Unknown API Error")
            except json.JSONDecodeError:
                error_detail = e.response.text

            print(f"Lỗi HTTP khi gọi Gemini API: {e.response.status_code} - Chi tiết: {error_detail}")
            return f"Xin lỗi, đã có lỗi xảy ra khi gọi API AI (Code: {e.response.status_code}). Vui lòng kiểm tra lại GEMINI_API_KEY.", current_contents
        except httpx.RequestError as e:
            print(f"Lỗi kết nối khi gọi Gemini API: {e}")
            return "Xin lỗi, không thể kết nối đến máy chủ AI.", current_contents
        except ValueError as e:
            print(f"Lỗi cấu hình: {e}")
            return "Lỗi cấu hình: Vui lòng cung cấp GEMINI_API_KEY hợp lệ trong file .env.", current_contents
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            return "Xin lỗi, một lỗi không mong muốn đã xảy ra.", current_contents

# Khởi tạo một instance của service
ai_advisor_service = AIAdvisorService()
