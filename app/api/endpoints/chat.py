from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId # <--- Import thêm thư viện này để xử lý ID

from app.api import deps 
from app.models.user import User
from app.models.ai_recommendations import AIRecommendation
from app.models.job_listings import JobListing
from app.models.job_seekers import JobSeeker

router = APIRouter()

# --- CẤU HÌNH API KEY ---
MY_API_KEY = "AIzaSyDHs_J1sQ34UAoQRCVrSQut88AZkYvMspQ" 

try:
    genai.configure(api_key=MY_API_KEY)
except Exception as e:
    print(f"Lỗi Key: {e}")

model = genai.GenerativeModel('gemini-2.5-flash')

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

async def search_relevant_jobs(query_text: str, top_k: int = 3):
    try:
        query_embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=query_text
        )['embedding']
        
        jobs = await JobListing.find(JobListing.vector != None).to_list()
        if not jobs: return []

        job_vectors = [job.vector for job in jobs]
        similarities = cosine_similarity([query_embedding], job_vectors)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.35:
                results.append(jobs[idx])
        return results
    except:
        return []

@router.post("/advice", response_model=ChatResponse)
async def get_advice(
    chat_request: ChatRequest,
    current_user: User = Depends(deps.get_current_user)
):
    try:
        # --- 1. LẤY THÔNG TIN PROFILE (LOGIC BẤT TỬ) ---
        print(f"🔍 DEBUG: Đang tìm hồ sơ cho User ID: {current_user.id}")
        
        user_profile = None
        
        # Cách 1: Tìm theo ObjectId (Chuẩn MongoDB)
        try:
            user_id_obj = ObjectId(current_user.id)
            user_profile = await JobSeeker.find_one({"user_id": user_id_obj})
        except:
            pass # Nếu lỗi convert thì bỏ qua

        # Cách 2: Nếu chưa thấy, tìm theo String (Dự phòng)
        if not user_profile:
            user_profile = await JobSeeker.find_one({"user_id": str(current_user.id)})

        # --- XỬ LÝ KẾT QUẢ TÌM ĐƯỢC ---
        cv_context = ""
        if user_profile:
            print("✅ DEBUG: Đã tìm thấy hồ sơ CV!")
            
            # Lấy kinh nghiệm (xử lý dù là list hay string)
            exp_text = ""
            if isinstance(user_profile.experience, list) and len(user_profile.experience) > 0:
                exp_text = user_profile.experience[0]
            elif isinstance(user_profile.experience, str):
                exp_text = user_profile.experience
            
            cv_context = f"""
            [HỒ SƠ NGƯỜI DÙNG]:
            - Họ tên: {user_profile.full_name}
            - Kinh nghiệm: {exp_text}
            - Mục tiêu: {user_profile.career_goal or 'Chưa rõ'}
            """
        else:
            print("⚠️ DEBUG: Vẫn không tìm thấy hồ sơ.")
            cv_context = "(Người dùng chưa có CV trên hệ thống)"
        # ------------------------------------------------

        # --- 2. RAG SEARCH ---
        search_query = chat_request.message
        if user_profile:
            search_query += f" {cv_context}"

        relevant_jobs = await search_relevant_jobs(search_query)
        
        jobs_context = ""
        if relevant_jobs:
            jobs_context = "\n[CÔNG VIỆC GỢI Ý]:\n"
            for job in relevant_jobs:
                jobs_context += f"- {job.title} tại {job.company} ({job.location}). Lương: {job.salary_range}\n"
        
        # --- 3. TẠO PROMPT ---
        system_instruction = f"""
        Bạn là tư vấn viên tuyển dụng JobFinder.
        User: {current_user.full_name}.
        
        {cv_context}
        
        {jobs_context}
        
        YÊU CẦU:
        - Dựa vào [HỒ SƠ NGƯỜI DÙNG] để tư vấn.
        - Nếu có [CÔNG VIỆC GỢI Ý], hãy giới thiệu chi tiết.
        """
        
        full_prompt = f"{system_instruction}\n\nUser: {chat_request.message}"

        # --- 4. GỌI GEMINI ---
        ai_response = model.generate_content(full_prompt)
        ai_text = ai_response.text

        # --- 5. LƯU LỊCH SỬ (Dùng string ID cho đơn giản) ---
        try:
            await AIRecommendation(user_id=str(current_user.id), type="chat_prompt", prompt=chat_request.message).insert()
            await AIRecommendation(user_id=str(current_user.id), type="chat_response", response=ai_text).insert()
        except: pass

        return {"response": ai_text}

    except Exception as e:
        print(f"❌ Lỗi Chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# API History giữ nguyên
@router.get("/history")
async def get_chat_history(current_user: User = Depends(deps.get_current_user)):
    history_records = await AIRecommendation.find({"user_id": str(current_user.id)}).sort("+timestamp").to_list()
    formatted_history = []
    for record in history_records:
        if record.type == "chat_prompt" and record.prompt:
            formatted_history.append({"role": "user", "content": record.prompt})
        elif record.type == "chat_response" and record.response:
            formatted_history.append({"role": "ai", "content": record.response})
    return formatted_history