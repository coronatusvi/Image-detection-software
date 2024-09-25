# app/main.py
from fastapi import FastAPI
from app.routes import router as api_router

app = FastAPI()

# Thêm router vào ứng dụng
app.include_router(api_router)