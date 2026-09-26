from typing import List, Optional
from pydantic import BaseModel

# Thông tin từng ghế
class SeatOut(BaseModel):
    id: int
    seat_code: str
    seat_type: str        # 'standard' hoặc 'vip'
    status: str           # 'available' hoặc 'booked'
    floor: int            # 1 hoặc 2
    price: Optional[float] = None

    class Config:
        from_attributes = True


# Response sơ đồ ghế (Phục vụ Trang 2: Sơ đồ ghế 2D)
class SeatMapResponse(BaseModel):
    trip_id: int
    bus_type: str
    base_price: float
    total_seats: int
    available_seats: int
    booked_seats: int
    seats: List[SeatOut]
    floor_1: List[SeatOut] = []
    floor_2: List[SeatOut] = []
