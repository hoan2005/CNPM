from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..config import Base

class Operator(Base):
    """
    Bảng lưu thông tin các nhà xe (Phương Trang, Hải Vân, Hoàng Long...)
    """
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    logo_url = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    rating = Column(Float, default=4.5)

    # Quan hệ 1 - N với chuyến xe
    trips = relationship("Trip", back_populates="operator", cascade="all, delete-orphan")
