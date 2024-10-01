# app/auth/models.py
from sqlalchemy import Column, Integer, String
from app.connection.connection import Base

class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    id_company = Column(Integer)

class AuthenticatorModel(Base):
    __tablename__ = 'authenticator'
    
    id_user = Column(Integer, primary_key=True)  # Khoá chính
    password_hash = Column(String, nullable=False)  
    refresh_token = Column(String, nullable=False)  
    last_login = Column(Integer, nullable=False, default=0) 