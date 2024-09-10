from fastapi import FastAPI
from routes import router as auth_router

app = FastAPI()

# Đăng ký các route
app.include_router(auth_router)

# Chạy ứng dụng
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)