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
from typing import Dict, Any, Literal

# Khóa bí mật để ký JWT từ biến môi trường
SECRET_KEY = os.getenv("SECRET_KEY", "f92fba826e69b7f89ecb349a2f7b1df92fba826e69b7f89ecb349a2f7b1df")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Ví dụ: 7 ngày

# Tạo context để mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, filters: Dict[Literal['id', 'full_name', 'email', 'id_company'], Any]):
    query = db.query(UserModel)
    
    for feature, value in filters.items():
        if feature == 'id' and isinstance(value, int):
            query = query.filter(UserModel.id == value)  # Kiểm tra id là kiểu integer
        elif feature in ['full_name', 'email', 'id_company']:
            query = query.filter(getattr(UserModel, feature) == value)

    return query.first()
    # Tìm kiếm người dùng theo email
    # user_by_email = get_user(db, {'email': 'example@example.com'})

    # # Tìm kiếm người dùng theo full_name và email
    # user_by_full_name_and_email = get_user(db, {'full_name': 'John Doe', 'email': 'example@example.com'})

    # # Tìm kiếm người dùng theo id và full_name
    # user_by_id_and_full_name = get_user(db, {'id': 1, 'full_name': 'John Doe'})

def get_authenticator(db: Session, user_id: int):
    return db.query(AuthenticatorModel).filter(AuthenticatorModel.id_user == user_id).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, {'email': email})
    if not user:
        return False

    authenticator = get_authenticator(db, user.id)
    if not authenticator or not verify_password(password, authenticator.password_hash):
        return False

    # Cập nhật last_login và refresh_token
    refresh_token = create_refresh_token({"sub": str(user.id)})
    authenticator.refresh_token = refresh_token
    authenticator.last_login = int(datetime.utcnow().timestamp())  # Unix timestamp
    db.commit()  # Lưu thay đổi vào DB

    return user, refresh_token

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("payload", payload)
        user_id: int = payload.get("sub")
        # print("user_id", user_id)
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    db: Session = SessionLocal()
    try:
        authenticator = get_authenticator(db, user_id)  # Lấy thông tin xác thực
        if not authenticator:
            raise credentials_exception
        
        user = get_user(db,  {'id': authenticator.id_user})  # Lấy thông tin người dùng từ bảng users
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close() 
        
