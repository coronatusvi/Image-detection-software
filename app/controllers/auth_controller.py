# app/controllers/auth_controller.py
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.connection.connection import SessionLocal
from app.models.models import UserModel, AuthenticatorModel  # Import các mô hình

# Khóa bí mật để ký JWT từ biến môi trường
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Tạo context để mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_authenticator(db: Session, user_id: int):
    return db.query(AuthenticatorModel).filter(AuthenticatorModel.id_user == user_id).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False

    authenticator = get_authenticator(db, user.id)  # Lấy thông tin xác thực
    if not authenticator or not verify_password(password, authenticator.password_hash):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db: Session = SessionLocal()
    try:
        authenticator = get_authenticator(db, user_id)  # Lấy thông tin xác thực
        if not authenticator:
            raise credentials_exception

        user = get_user(db, authenticator.id_user)  # Lấy thông tin người dùng từ bảng users
        if user is None:
            raise credentials_exception
    finally:
        db.close()  # Đóng session để tránh rò rỉ tài nguyên
    return user
