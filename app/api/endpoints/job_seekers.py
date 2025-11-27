from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import pypdf
import io
import google.generativeai as genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.api import deps
from app.models.job_seekers import JobSeeker
from app.models.user import User
from app.models.job_listings import JobListing
from app.core.config import settings

router = APIRouter()

# Cấu hình Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Lỗi đọc PDF: {e}")
        return ""

@router.post("/upload-cv")
async def upload_cv_and_find_jobs(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Upload CV -> Phân tích -> TÌM VIỆC + LƯU VÀO PROFILE
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

    content = await file.read()
    cv_text = extract_text_from_pdf(content)
    
    if not cv_text or len(cv_text) < 50:
        raise HTTPException(status_code=400, detail="CV quá ngắn hoặc lỗi file")

    try:
        # 1. Tóm tắt CV bằng AI
        model = genai.GenerativeModel('gemini-2.5-flash')
        summary_prompt = f"Hãy tóm tắt kỹ năng, kinh nghiệm và mong muốn từ CV này thành 1 đoạn văn ngắn khoảng 200 chữ: \n\n {cv_text[:4000]}"
        summary_res = model.generate_content(summary_prompt)
        summary_text = summary_res.text

        # 2. RAG Search (Tìm việc phù hợp)
        cv_embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=summary_text
        )['embedding']

        jobs = await JobListing.find(JobListing.vector != None).to_list()
        matched_jobs = []
        
        if jobs:
            job_vectors = [job.vector for job in jobs]
            similarities = cosine_similarity([cv_embedding], job_vectors)[0]
            top_indices = similarities.argsort()[-5:][::-1]
            
            for idx in top_indices:
                if similarities[idx] > 0.35:
                    matched_jobs.append(jobs[idx])

        # --- 3. QUAN TRỌNG: LƯU VÀO DATABASE (PROFILE) ---
        # Tìm profile của user
        profile = await JobSeeker.find_one({"user_id": str(current_user.id)})
        
        if not profile:
            # Nếu chưa có thì tạo mới
            profile = JobSeeker(
            user_id=str(current_user.id),
            full_name=current_user.full_name or "User",
            # SỬA: Bọc vào ngoặc vuông để thành List
            experience=[summary_text] 
            )
            await profile.insert()
        else:
            # Nếu có rồi thì cập nhật
            # SỬA: Bọc vào ngoặc vuông
            profile.experience = [summary_text]
            await profile.save()
        # ------------------------------------------------

        return {
            "message": "Đã phân tích và LƯU CV vào hồ sơ thành công!",
            "summary": summary_text,
            "jobs": matched_jobs
        }

    except Exception as e:
        print(f"Lỗi: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")

# ... (Giữ nguyên các hàm get/update khác ở dưới nếu có)
@router.get("/me")
async def get_my_profile(current_user: User = Depends(deps.get_current_user)):
    profile = await JobSeeker.find_one({"user_id": str(current_user.id)})
    return profile or {}

@router.put("/me")
async def update_my_profile(data: dict, current_user: User = Depends(deps.get_current_user)):
    # Code update cũ của bạn...
    pass