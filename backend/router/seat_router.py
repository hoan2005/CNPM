from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config import get_db
from ..schemas import SeatMapResponse
from ..controller import SeatController

router = APIRouter(
    prefix="/api/trips",
    tags=["Seats"]
)

@router.get("/{trip_id}/seats", response_model=SeatMapResponse)
def get_trip_seat_map(trip_id: int, db: Session = Depends(get_db)):
    """
    Router tiếp nhận request sơ đồ ghế và ủy quyền cho SeatController
    """
    return SeatController.get_trip_seat_map(db=db, trip_id=trip_id)
