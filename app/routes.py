# routes.py
from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from app.controllers.auth_controller import ( authenticate_user, create_access_token, get_current_user)
from sqlalchemy.orm import Session
from app.connection.connection import SessionLocal
from app.controllers.auth_controller import (
    authenticate_user,
    create_access_token,
    get_current_user
)

router = APIRouter()

# Route để đăng nhập và tạo token
@router.post("/login")
async def login(email: str, password: str):
    db: Session = SessionLocal()  # Khởi tạo phiên làm việc
    try:
        user = authenticate_user(db, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.id})  # Giả sử user có thuộc tính id
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()  # Đóng session để tránh rò rỉ tài nguyên

# Route để lấy thông tin người dùng hiện tại
@router.get("/users/me")
async def read_users_me(current_user: authenticate_user = Depends(get_current_user)):
    return current_user
