# routes.py
from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from pydantic import BaseModel
from app.controllers.auth_controller import ( authenticate_user, create_access_token, get_current_user)
from sqlalchemy.orm import Session
from app.connection.connection import SessionLocal
from app.models.models import UserModel

router = APIRouter()

# Route để đăng nhập và tạo token
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(login_request: LoginRequest):
    db: Session = SessionLocal()  # Khởi tạo phiên làm việc
    try:
        user = authenticate_user(db, login_request.email, login_request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": str(user.id)})  # Giả sử user có thuộc tính id
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()  # Đóng session để tránh rò rỉ tài nguyên

# Route để lấy thông tin người dùng hiện tại
@router.get("/users/me")
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    print("current_user", current_user.id)
    return current_user
