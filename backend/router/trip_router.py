from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..config import get_db
from ..schemas import TripSearchResponse, TripDetail
from ..controller import TripController

router = APIRouter(
    prefix="/api/trips",
    tags=["Trips"]
)

@router.get("/search", response_model=TripSearchResponse)
def search_trips(
    departure: Optional[str] = Query(None, description="Điểm đi (VD: Đà Nẵng)"),
    destination: Optional[str] = Query(None, description="Điểm đến (VD: Huế)"),
    travel_date: Optional[str] = Query(None, description="Ngày khởi hành (YYYY-MM-DD)"),
    passengers: int = Query(1, ge=1, description="Số lượng hành khách"),
    bus_types: Optional[List[str]] = Query(None, alias="bus_type", description="Lọc theo loại xe"),
    operators: Optional[List[str]] = Query(None, alias="operator", description="Lọc theo nhà xe"),
    min_price: Optional[float] = Query(None, description="Giá vé tối thiểu"),
    max_price: Optional[float] = Query(None, description="Giá vé tối đa"),
    time_slot: Optional[str] = Query(None, description="Khung giờ: morning, afternoon, evening"),
    sort_by: Optional[str] = Query("departure_time", description="Sắp xếp theo: departure_time, price, rating, duration"),
    sort_order: Optional[str] = Query("asc", description="Thứ tự: asc, desc"),
    db: Session = Depends(get_db)
):
    """
    Router tiếp nhận HTTP request tìm kiếm và ủy quyền xử lý nghiệp vụ cho TripController
    """
    return TripController.search_trips(
        db=db,
        departure=departure,
        destination=destination,
        travel_date=travel_date,
        passengers=passengers,
        bus_types=bus_types,
        operators=operators,
        min_price=min_price,
        max_price=max_price,
        time_slot=time_slot,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/{trip_id}", response_model=TripDetail)
def get_trip_detail(trip_id: int, db: Session = Depends(get_db)):
    """
    Router tiếp nhận request chi tiết chuyến xe và ủy quyền cho TripController
    """
    return TripController.get_trip_detail(db=db, trip_id=trip_id)
