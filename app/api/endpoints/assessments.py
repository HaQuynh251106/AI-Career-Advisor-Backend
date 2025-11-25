from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from datetime import datetime

# Import Model (Đảm bảo bạn đã có 2 file model này trong folder models)
from app.models.assessments import Assessment
from app.models.test_results import TestResult

router = APIRouter()

# --- Schemas ---
class AssessmentCreate(BaseModel):
    title: str
    description: str
    questions: List[dict] # List các câu hỏi: [{"question": "...", "options": [], "correct": 0}]
    difficulty: str # beginner, intermediate, advanced

class SubmitTest(BaseModel):
    assessment_id: str
    score: int # Tạm thời cho Frontend tự chấm điểm rồi gửi lên (hoặc gửi đáp án lên để BE chấm)

# --- API 1: Tạo bài test mới (Dùng cho Admin/Swagger nhập liệu) ---
@router.post("/", response_model=Assessment)
async def create_assessment(
    data: AssessmentCreate,
    current_user: User = Depends(deps.get_current_user)
):
    assessment = Assessment(**data.dict())
    await assessment.insert()
    return assessment

# --- API 2: Lấy danh sách bài test ---
@router.get("/", response_model=List[Assessment])
async def get_assessments(
    current_user: User = Depends(deps.get_current_user)
):
    return await Assessment.find_all().to_list()

# --- API 3: Nộp bài & Lưu kết quả ---
@router.post("/submit")
async def submit_assessment(
    data: SubmitTest,
    current_user: User = Depends(deps.get_current_user)
):
    # 1. Kiểm tra bài test có tồn tại không
    assessment = await Assessment.get(data.assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Bài test không tồn tại")

    # 2. Lưu kết quả
    result = TestResult(
        user_id=str(current_user.id),
        assessment_id=data.assessment_id,
        score=data.score,
        completed_at=datetime.now()
    )
    await result.insert()
    
    return {"message": "Nộp bài thành công!", "score": data.score}

# --- API 4: Lấy lịch sử thi của User ---
@router.get("/history")
async def get_test_history(
    current_user: User = Depends(deps.get_current_user)
):
    results = await TestResult.find({"user_id": str(current_user.id)}).to_list()
    # Map thêm tên bài test cho đẹp
    history = []
    for res in results:
        test = await Assessment.get(res.assessment_id)
        history.append({
            "test_title": test.title if test else "Bài test đã xóa",
            "score": res.score,
            "date": res.completed_at
        })
    return history