from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..model.railway_models import ChuyenXe, Xe, Ghe, GheChuyenXe
from ..schemas import SeatMapResponse, SeatOut

class SeatController:
    """
    Controller xử lý nghiệp vụ cho sơ đồ ghế:
    - Truy vấn từ bảng ghe_chuyen_xe và ghe theo cấu trúc Railway MySQL
    - Phân tầng ghế Tầng 1 và Tầng 2
    - Đếm số ghế trống và đã đặt thực tế
    """

    @staticmethod
    def get_trip_seat_map(db: Session, trip_id: int) -> SeatMapResponse:
        chuyen = db.query(ChuyenXe).filter(ChuyenXe.id_chuyen == trip_id).first()
        if not chuyen:
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy chuyến xe với ID {trip_id}"
            )

        floor_1 = []
        floor_2 = []
        booked_count = 0
        available_count = 0

        # 1. Thử lấy từ ghe_chuyen_xe trước (nếu có dữ liệu)
        ghe_chuyen_list = []
        try:
            ghe_chuyen_list = (
                db.query(GheChuyenXe, Ghe)
                .join(Ghe, GheChuyenXe.id_ghe == Ghe.id_ghe)
                .filter(GheChuyenXe.id_chuyen == trip_id)
                .order_by(Ghe.tang.asc(), Ghe.so_ghe.asc())
                .all()
            )
        except Exception:
            ghe_chuyen_list = []

        if ghe_chuyen_list:
            for ghe_ct, ghe in ghe_chuyen_list:
                is_booked = ghe_ct.trang_thai in ("DA_DAT", "DA_GIU", "DA_SU_DUNG")
                status_str = "booked" if is_booked else "available"

                seat_dict = {
                    "id": ghe_ct.id_ghe_chuyen,
                    "seat_code": ghe.so_ghe,
                    "seat_type": "vip" if ghe.loai_ghe == "VIP" else "standard",
                    "status": status_str,
                    "floor": ghe.tang,
                    "price": float(chuyen.gia_ve)
                }
                seat_out = SeatOut(**seat_dict)
                if ghe.tang == 1:
                    floor_1.append(seat_out)
                else:
                    floor_2.append(seat_out)

                if is_booked:
                    booked_count += 1
                else:
                    available_count += 1
        else:
            # 2. Truy vấn từ bảng ghe theo id_xe và đối chiếu vé đã đặt trong chi_tiet_ve
            ghes = db.query(Ghe).filter(Ghe.id_xe == chuyen.id_xe).order_by(Ghe.tang.asc(), Ghe.so_ghe.asc()).all()
            booked_seat_ids = set()
            try:
                from sqlalchemy import text
                rows = db.execute(
                    text("SELECT id_ghe FROM chi_tiet_ve WHERE id_chuyen = :cid AND trang_thai = 'DA_DAT'"),
                    {"cid": trip_id}
                ).fetchall()
                booked_seat_ids = set(r[0] for r in rows)
            except Exception:
                booked_seat_ids = set()

            for ghe in ghes:
                is_booked = ghe.id_ghe in booked_seat_ids
                status_str = "booked" if is_booked else "available"

                seat_dict = {
                    "id": ghe.id_ghe,
                    "seat_code": ghe.so_ghe,
                    "seat_type": "vip" if ghe.loai_ghe == "VIP" else "standard",
                    "status": status_str,
                    "floor": ghe.tang,
                    "price": float(chuyen.gia_ve)
                }
                seat_out = SeatOut(**seat_dict)
                if ghe.tang == 1:
                    floor_1.append(seat_out)
                else:
                    floor_2.append(seat_out)

                if is_booked:
                    booked_count += 1
                else:
                    available_count += 1

        total_seats = booked_count + available_count

        return SeatMapResponse(
            trip_id=trip_id,
            bus_type=chuyen.xe.loai_xe,
            base_price=float(chuyen.gia_ve),
            total_seats=total_seats,
            available_seats=available_count,
            booked_seats=booked_count,
            seats=floor_1 + floor_2,
            floor_1=floor_1,
            floor_2=floor_2
        )
