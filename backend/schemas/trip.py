from typing import List, Optional, Dict, Any
from pydantic import BaseModel

# Thông tin rút gọn của nhà xe
class OperatorOut(BaseModel):
    id: int
    name: str
    logo_url: Optional[str] = None
    phone: Optional[str] = None
    rating: float

    class Config:
        from_attributes = True


# Kết quả 1 chuyến xe khi tìm kiếm (Phục vụ Trang 1: Tìm kiếm & Lọc)
class TripSearchResult(BaseModel):
    id: int
    operator: OperatorOut
    bus_type: str
    departure_point: str
    destination_point: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    duration_formatted: str
    travel_date: str
    price: float
    total_seats: int
    available_seats: int
    rating: float
    review_count: int
    status: str
    amenities: List[str] = []

    class Config:
        from_attributes = True


# Response danh sách tìm kiếm
class TripSearchResponse(BaseModel):
    total: int
    trips: List[TripSearchResult]


# Thông tin điểm đón / trả khách
class PointInfo(BaseModel):
    time: str
    location: str
    address: Optional[str] = None


# Chi tiết chuyến xe (Phục vụ Trang 2: Chi tiết chuyến xe)
class TripDetail(TripSearchResult):
    pickup_points: List[PointInfo] = []
    dropoff_points: List[PointInfo] = []
    policies: Dict[str, Any] = {}
