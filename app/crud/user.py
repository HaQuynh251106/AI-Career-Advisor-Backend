
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user_by_email(email: str) -> Optional[User]:
    """Tìm người dùng bằng email."""
    return await User.find_one(User.email == email)

async def create_user(user_in: UserCreate) -> User:
    """Tạo người dùng mới."""
    # Hash mật khẩu
    hashed_password = get_password_hash(user_in.password)
    
    # Tạo đối tượng User model
    user_obj = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
        role=user_in.role
    )
    
    # Lưu vào DB
    await user_obj.insert()
    return user_obj

# (Bạn sẽ thêm các hàm CRUD khác ở đây, ví dụ: get_user, update_user,...)
