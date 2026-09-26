from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..config import Base

class Seat(Base):
    """
    Bảng lưu thông tin từng ghế ngồi/giường nằm của chuyến xe
    """
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    
    seat_code = Column(String(10), nullable=False)        # VD: 'A1', 'A2', 'B1'...
    seat_type = Column(String(20), default="standard")    # 'standard' hoặc 'vip'
    status = Column(String(20), default="available")      # 'available' hoặc 'booked'
    floor = Column(Integer, default=1)                    # Tầng 1 hoặc Tầng 2
    price = Column(Float, nullable=True)                  # Giá riêng cho ghế (nếu có)

    # Quan hệ với chuyến xe
    trip = relationship("Trip", back_populates="seats")
