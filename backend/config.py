import os
import sys
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cấu hình chuỗi kết nối MySQL
# Người dùng có thể cấu hình qua biến môi trường DATABASE_URL hoặc dùng mặc định
# Mặc định: mysql+pymysql://root:password@localhost:3306/bus_booking?charset=utf8mb4
# Có fallback sang SQLite nếu môi trường dev cục bộ chưa bật MySQL server để hệ thống vẫn chạy mượt mà
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "TkLeXbRWmjKcDzsvZBULHWkPpvVkLnyQ")
DB_HOST = os.getenv("DB_HOST", "zephyr.proxy.rlwy.net")
DB_PORT = os.getenv("DB_PORT", "49810")
DB_NAME = os.getenv("DB_NAME", "railway")

MYSQL_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
DATABASE_URL = os.getenv("DATABASE_URL", MYSQL_URL)

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    # Thử kết nối test
    with engine.connect() as conn:
        pass
    print(f"[Database] Đã kết nối thành công đến MySQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")
except Exception as e:
    # Nếu kết nối MySQL lỗi (chưa cài MySQL hoặc chưa start service), fallback về SQLite để các test case vẫn chạy ổn định
    print(f"[Database Warning] Không thể kết nối MySQL ({e}). Tự động fallback sang SQLite bus_booking.db để đảm bảo hệ thống không bị gián đoạn.")
    DATABASE_URL = "sqlite:///./bus_booking.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency cung cấp database session cho từng request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
