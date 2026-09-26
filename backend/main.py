import sys
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import engine, Base, SessionLocal
from .model import ChuyenXe
from .seed_railway import seed_railway_data
from .router import trip_router, seat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Sự kiện vòng đời ứng dụng:
    Đảm bảo các bảng tồn tại trên Cloud MySQL và kiểm tra dữ liệu.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        trip_count = db.query(ChuyenXe).count()
        if trip_count == 0:
            print("[Database] Chưa có chuyến xe. Đang tự động khởi tạo dữ liệu mẫu lên Cloud...")
            seed_railway_data()
            print("[Database] Đã khởi tạo dữ liệu thành công!")
        else:
            print(f"[Database] Đã sẵn sàng với {trip_count} chuyến xe trong hệ thống.")
    except Exception as e:
        print(f"[Database] Lỗi kiểm tra CSDL: {e}")
    finally:
        db.close()
    
    yield


# Khởi tạo ứng dụng FastAPI theo mô hình phân tầng của nhóm (CS434)
app = FastAPI(
    title="Hệ thống Đặt vé xe khách API (CS434)",
    description="Backend API phục vụ module Tìm kiếm chuyến xe, Chi tiết chuyến xe & Sơ đồ ghế (Chuẩn kiến trúc Router - Controller - Model - Schemas)",
    version="1.1.0",
    lifespan=lifespan
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn các routers vào ứng dụng
app.include_router(trip_router)
app.include_router(seat_router)

@app.get("/", tags=["Health Check"])
def root():
    """
    Endpoint kiểm tra trạng thái hoạt động của backend API
    """
    return {
        "status": "online",
        "message": "Hệ thống API Đặt vé xe khách (CS434) đang chạy ổn định theo cấu trúc Router - Controller!",
        "module": "Tìm kiếm chuyến xe & Sơ đồ ghế",
        "swagger_docs": "/docs",
        "endpoints": {
            "search_trips": "/api/trips/search?departure=Đà Nẵng&destination=Huế",
            "trip_detail": "/api/trips/1",
            "seat_map": "/api/trips/1/seats"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

