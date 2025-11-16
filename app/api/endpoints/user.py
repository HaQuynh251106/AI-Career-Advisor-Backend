
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user, get_user_by_email
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    """
    Đăng ký người dùng mới.
    """
    user = await get_user_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    new_user = await create_user(user_in=user_in)
    
    # Chuyển đổi ID từ PydanticObjectId sang str cho response
    user_dict = new_user.model_dump()
    user_dict["id"] = str(new_user.id) 
    
    return UserRead(**user_dict)

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Lấy thông tin người dùng hiện tại đã đăng nhập.
    """
    user_dict = current_user.model_dump()
    user_dict["id"] = str(current_user.id)
    return UserRead(**user_dict)
