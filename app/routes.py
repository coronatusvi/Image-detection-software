# routes.py
from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from pydantic import BaseModel
from app.controllers.auth_controller import ( ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, get_current_user, get_user)
from sqlalchemy.orm import Session
from app.connection.connection import SessionLocal
from app.models.models import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# Route để đăng nhập và tạo token
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(login_request: LoginRequest):
    db: Session = SessionLocal()  # Khởi tạo phiên làm việc
    try:
        user, refresh_token = authenticate_user(db, login_request.email, login_request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    finally:
        db.close()  # Đóng session để tránh rò rỉ tài nguyên

@router.post("/refresh-token")
async def refresh_access_token(
    refresh_token: str = Depends(oauth2_scheme)  # Lấy refresh token từ header
):
    print("refresh_token", refresh_token)
    db: Session = Depends(SessionLocal),  # Lấy session từ DB
    try:
        # Decode refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # Lấy thông tin người dùng từ DB
        user = get_user(db, {'id': user_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Tạo access token mới
        access_token = create_access_token(data={"sub": str(user.id)})

        db.commit()
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    finally:
        db.close()  # Đóng session để tránh rò rỉ tài nguyên

# Route để lấy thông tin người dùng hiện tại
@router.get("/users/me")
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
