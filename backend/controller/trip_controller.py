from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, desc, asc

from ..model.railway_models import TuyenDuong, Xe, ChuyenXe, Ghe, GheChuyenXe
from ..schemas import TripSearchResult, TripDetail, TripSearchResponse

# Tiện ích thời gian & giá
FUTA_LOGO = "https://cdn.futabus.vn/futa-bus/images/logo/logo_futa.svg"
FUTA_PHONE = "1900 6067"
FUTA_RATING = 4.8
AMENITIES_DEFAULT = [
    "Wifi tốc độ cao",
    "Nước suối đóng chai & khăn lạnh",
    "Cổng sạc USB",
    "Điều hòa không khí",
    "Chăn mền, gối"
]
POLICIES_DEFAULT = {
    "cancellation": "Hủy vé trước 24 giờ hoàn 95%, trước 12 giờ hoàn 50%",
    "baggage": "Miễn cước 20kg hành lý gửi và 1 túi xách",
    "children": "Trẻ em dưới 5 tuổi ngồi cùng phụ huynh miễn phí"
}

def format_duration(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0 and mins > 0:
        return f"{hours}h {mins}m"
    elif hours > 0:
        return f"{hours}h"
    return f"{mins}m"


def build_trip_dict(chuyen: ChuyenXe, available_seats: int, total_seats: int) -> dict:
    dep_time = chuyen.thoi_gian_khoi_hanh
    dep_time_str = dep_time.strftime("%H:%M")
    travel_date_str = dep_time.strftime("%Y-%m-%d")
    duration_min = chuyen.thoi_gian_du_kien or (chuyen.xe.so_ghe and 135)
    arr_dt_min = dep_time.hour * 60 + dep_time.minute + (duration_min or 135)
    arr_h, arr_m = divmod(arr_dt_min, 60)
    arr_h = arr_h % 24
    arr_time_str = f"{arr_h:02d}:{arr_m:02d}"

    tuyen = chuyen.tuyen_duong
    xe = chuyen.xe

    # Điểm đón/trả mặc định dựa theo tuyến đường
    pickup_points = [
        {"time": dep_time_str, "location": f"Bến xe Trung tâm {tuyen.diem_di}", "address": f"Quầy vé FUTA, Bến xe TT {tuyen.diem_di}"}
    ]
    dropoff_points = [
        {"time": arr_time_str, "location": f"Văn phòng FUTA {tuyen.diem_den}", "address": f"Văn phòng FUTA, TP. {tuyen.diem_den}"}
    ]

    return {
        "id": chuyen.id_chuyen,
        "operator": {
            "id": 1,
            "name": "Phương Trang (FUTA Bus Lines)",
            "logo_url": FUTA_LOGO,
            "phone": FUTA_PHONE,
            "rating": FUTA_RATING,
        },
        "bus_type": xe.loai_xe,
        "departure_point": tuyen.diem_di,
        "destination_point": tuyen.diem_den,
        "departure_time": dep_time_str,
        "arrival_time": arr_time_str,
        "duration_minutes": duration_min or 135,
        "duration_formatted": format_duration(duration_min or 135),
        "travel_date": travel_date_str,
        "price": float(chuyen.gia_ve),
        "total_seats": total_seats,
        "available_seats": available_seats,
        "rating": FUTA_RATING,
        "review_count": 128,
        "status": "active" if chuyen.trang_thai == "MO_BAN" else "completed",
        "amenities": AMENITIES_DEFAULT,
        "pickup_points": pickup_points,
        "dropoff_points": dropoff_points,
        "policies": POLICIES_DEFAULT,
    }


def count_seats(db: Session, chuyen: ChuyenXe):
    total = (chuyen.xe.so_ghe if chuyen.xe else None) or 34
    booked = 0
    try:
        from sqlalchemy import text
        booked = db.execute(
            text("SELECT COUNT(*) FROM chi_tiet_ve WHERE id_chuyen = :cid AND trang_thai = 'DA_DAT'"),
            {"cid": chuyen.id_chuyen}
        ).scalar() or 0
    except Exception:
        booked = 0
    available = max(0, total - booked)
    return total, available


class TripController:
    """
    Controller xử lý toàn bộ logic nghiệp vụ cho chuyến xe.
    Truy vấn từ MySQL Railway theo cấu trúc bảng của nhóm:
    chuyen_xe <-> tuyen_duong, xe, ghe_chuyen_xe
    """

    @staticmethod
    def search_trips(
        db: Session,
        departure: Optional[str] = None,
        destination: Optional[str] = None,
        travel_date: Optional[str] = None,
        passengers: int = 1,
        bus_types: Optional[List[str]] = None,
        operators: Optional[List[str]] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        time_slot: Optional[str] = None,
        sort_by: Optional[str] = "departure_time",
        sort_order: Optional[str] = "asc"
    ) -> TripSearchResponse:

        # Validate E1: Điểm đi = Điểm đến
        if departure and destination:
            if departure.strip().lower() == destination.strip().lower():
                raise HTTPException(
                    status_code=400,
                    detail="Điểm đi và điểm đến không được trùng nhau"
                )

        # A1: Mặc định ngày hôm nay nếu không chọn ngày
        if not travel_date or not travel_date.strip():
            travel_date = datetime.now().strftime("%Y-%m-%d")

        # Query join chuyen_xe -> tuyen_duong, xe
        query = db.query(ChuyenXe).join(ChuyenXe.tuyen_duong).join(ChuyenXe.xe).filter(
            ChuyenXe.trang_thai == "MO_BAN"
        )

        # Lọc theo điểm đi
        if departure:
            query = query.filter(TuyenDuong.diem_di.ilike(f"%{departure.strip()}%"))
        # Lọc theo điểm đến
        if destination:
            query = query.filter(TuyenDuong.diem_den.ilike(f"%{destination.strip()}%"))

        # Lọc theo ngày khởi hành
        if travel_date:
            date_obj = datetime.strptime(travel_date.strip(), "%Y-%m-%d")
            next_day = date_obj.replace(hour=23, minute=59, second=59)
            query = query.filter(
                ChuyenXe.thoi_gian_khoi_hanh >= date_obj,
                ChuyenXe.thoi_gian_khoi_hanh <= next_day
            )

        # Lọc theo loại xe (bus_type)
        if bus_types:
            flat_bus_types = []
            for bt in bus_types:
                flat_bus_types.extend([item.strip() for item in bt.split(",") if item.strip()])
            if flat_bus_types:
                type_filters = [Xe.loai_xe.ilike(f"%{bt}%") for bt in flat_bus_types]
                query = query.filter(or_(*type_filters))

        # Lọc theo khoảng giá
        if min_price is not None:
            query = query.filter(ChuyenXe.gia_ve >= min_price)
        if max_price is not None:
            query = query.filter(ChuyenXe.gia_ve <= max_price)

        # Lọc theo khung giờ
        if time_slot:
            slot = time_slot.lower()
            if slot == "morning":
                query = query.filter(func.hour(ChuyenXe.thoi_gian_khoi_hanh) < 12)
            elif slot == "afternoon":
                query = query.filter(
                    func.hour(ChuyenXe.thoi_gian_khoi_hanh) >= 12,
                    func.hour(ChuyenXe.thoi_gian_khoi_hanh) < 18
                )
            elif slot == "evening":
                query = query.filter(func.hour(ChuyenXe.thoi_gian_khoi_hanh) >= 18)

        # Sắp xếp
        is_desc = (sort_order.lower() == "desc") if sort_order else False
        if sort_by == "price":
            query = query.order_by(desc(ChuyenXe.gia_ve) if is_desc else asc(ChuyenXe.gia_ve))
        else:
            query = query.order_by(desc(ChuyenXe.thoi_gian_khoi_hanh) if is_desc else asc(ChuyenXe.thoi_gian_khoi_hanh))

        chuyen_list = query.all()

        # Lọc theo số ghế còn trống >= passengers
        results = []
        for chuyen in chuyen_list:
            total, available = count_seats(db, chuyen)
            if available >= passengers:
                results.append(build_trip_dict(chuyen, available, total))

        return TripSearchResponse(total=len(results), trips=results)

    @staticmethod
    def get_trip_detail(db: Session, trip_id: int) -> TripDetail:
        chuyen = db.query(ChuyenXe).filter(ChuyenXe.id_chuyen == trip_id).first()
        if not chuyen:
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy chuyến xe với ID {trip_id}"
            )

        total, available = count_seats(db, chuyen)
        data = build_trip_dict(chuyen, available, total)
        return TripDetail(**data)
