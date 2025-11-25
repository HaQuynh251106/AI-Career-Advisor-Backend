from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from app.models.user import User
from app.core.config import settings 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub") # Token này đang chứa EMAIL
        
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
            
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    # --- SỬA ĐOẠN NÀY ---
    # Cũ (Sai): user = await User.get(token_data) -> Lỗi vì token_data là email
    
    # Mới (Đúng): Tìm user có trường email trùng với token_data
    user = await User.find_one(User.email == token_data)
    # --------------------
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user