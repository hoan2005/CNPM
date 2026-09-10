from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CNPM - Hệ thống quản lý bán vé xe"
)

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "FastAPI đang chạy!"
    }


@app.get("/api/test")
def test():
    return {
        "message": "API hoạt động bình thường"
    }