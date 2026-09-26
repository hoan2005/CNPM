import json
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..config import Base

class Trip(Base):
    """
    Bảng lưu thông tin từng chuyến xe khách
    """
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    
    bus_type = Column(String(100), nullable=False)        # VD: 'Limousine 9 chỗ', 'Giường nằm 34 phòng'
    departure_point = Column(String(150), nullable=False) # VD: 'Đà Nẵng' hoặc 'Bến xe TT Đà Nẵng'
    destination_point = Column(String(150), nullable=False) # VD: 'Huế' hoặc 'Bến xe Phía Nam Huế'
    
    departure_time = Column(String(10), nullable=False)   # Giờ khởi hành: '08:00'
    arrival_time = Column(String(10), nullable=False)     # Giờ đến nơi: '10:30'
    duration_minutes = Column(Integer, nullable=False)    # Thời gian chạy (phút)
    travel_date = Column(String(10), nullable=False, index=True) # Ngày chạy định dạng 'YYYY-MM-DD'
    
    price = Column(Float, nullable=False)                 # Giá vé gốc (VNĐ)
    total_seats = Column(Integer, nullable=False)         # Tổng số ghế
    available_seats = Column(Integer, nullable=False)     # Số ghế còn trống
    rating = Column(Float, default=4.5)                   # Điểm đánh giá (1-5)
    review_count = Column(Integer, default=0)             # Số lượt đánh giá
    status = Column(String(50), default="active")         # Trạng thái: 'active', 'completed', 'cancelled'

    # Các thông tin mở rộng phục vụ trang chi tiết chuyến xe (lưu dưới dạng JSON text)
    pickup_points_json = Column(Text, nullable=True)      # Danh sách điểm đón kèm giờ
    dropoff_points_json = Column(Text, nullable=True)     # Danh sách điểm trả kèm giờ
    amenities_json = Column(Text, nullable=True)          # Danh sách tiện ích (wifi, nước, sạc...)
    policies_json = Column(Text, nullable=True)           # Chính sách hoàn hủy, hành lý

    # Quan hệ
    operator = relationship("Operator", back_populates="trips")
    seats = relationship("Seat", back_populates="trip", cascade="all, delete-orphan")

    # Helper properties để tự động giải mã JSON
    @property
    def pickup_points(self):
        if self.pickup_points_json:
            try:
                return json.loads(self.pickup_points_json)
            except Exception:
                return []
        return []

    @property
    def dropoff_points(self):
        if self.dropoff_points_json:
            try:
                return json.loads(self.dropoff_points_json)
            except Exception:
                return []
        return []

    @property
    def amenities(self):
        if self.amenities_json:
            try:
                return json.loads(self.amenities_json)
            except Exception:
                return []
        return []

    @property
    def policies(self):
        if self.policies_json:
            try:
                return json.loads(self.policies_json)
            except Exception:
                return {}
        return {}
