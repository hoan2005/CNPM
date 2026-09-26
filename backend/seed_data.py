import sys
import json
from datetime import datetime, timedelta

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from .config import engine, Base, SessionLocal
from .model import Operator, Trip, Seat


def seed_database():
    """
    Hàm tạo dữ liệu mẫu cho hệ thống đặt vé xe
    """
    # 1. Tạo lại bảng trong CSDL
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("Đang nạp dữ liệu nhà xe (Operators)...")
        # 2. Tạo danh sách 1 nhà xe duy nhất
        operators_data = [
            {
                "name": "Phương Trang (FUTA Bus Lines)",
                "logo_url": "https://cdn.futabus.vn/futa-bus/images/logo/logo_futa.svg",
                "phone": "1900 6067",
                "rating": 4.8
            }
        ]

        operators = []
        for op in operators_data:
            operator_obj = Operator(**op)
            db.add(operator_obj)
            operators.append(operator_obj)
        db.commit()

        # Refresh để lấy id
        for op in operators:
            db.refresh(op)

        # Lấy ngày hiện tại và các ngày tiếp theo để người dùng test ngày nào cũng có dữ liệu
        today = datetime.now()
        dates = [
            (today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(4)
        ]
        # Thêm ngày cố định phòng khi test ngày cụ thể
        if "2026-09-10" not in dates:
            dates.append("2026-09-10")

        print(f"Tạo chuyến xe cho các ngày: {dates}...")

        # Dữ liệu mẫu các chuyến xe tuyến Đà Nẵng ⇄ Huế (Toàn bộ thuộc Nhà xe Phương Trang)
        trip_templates = [
            {
                "operator_idx": 0, # Phương Trang
                "bus_type": "Giường nằm 34 phòng",
                "dep_point": "Đà Nẵng",
                "dest_point": "Huế",
                "dep_time": "07:00",
                "arr_time": "09:15",
                "duration": 135,
                "price": 140000,
                "rating": 4.8,
                "review_count": 128,
                "seat_type_gen": "sleeper_34",
                "pickup": [
                    {"time": "06:40", "location": "Bến xe Trung tâm Đà Nẵng", "address": "185 Tôn Đức Thắng, Hòa Minh, Liên Chiểu"},
                    {"time": "07:00", "location": "Văn phòng 28 Nguyễn Tri Phương", "address": "28 Nguyễn Tri Phương, Thanh Khê"}
                ],
                "dropoff": [
                    {"time": "09:00", "location": "Bến xe Phía Nam Huế", "address": "97 An Dương Vương, TP. Huế"},
                    {"time": "09:15", "location": "Văn phòng FUTA Huế", "address": "12 Đội Cung, Phường Phú Hội, TP. Huế"}
                ]
            },
            {
                "operator_idx": 0, # Phương Trang
                "bus_type": "Limousine 9 chỗ VIP",
                "dep_point": "Đà Nẵng",
                "dest_point": "Huế",
                "dep_time": "08:30",
                "arr_time": "10:30",
                "duration": 120,
                "price": 190000,
                "rating": 4.9,
                "review_count": 94,
                "seat_type_gen": "limo_9",
                "pickup": [
                    {"time": "08:15", "location": "Sân bay Quốc tế Đà Nẵng", "address": "Cột số 5, Ga Quốc nội"},
                    {"time": "08:30", "location": "Văn phòng FUTA Đà Nẵng", "address": "Số 01 Nguyễn Hữu Thọ, Hải Châu"}
                ],
                "dropoff": [
                    {"time": "10:15", "location": "Vincom Plaza Huế", "address": "50A Hùng Vương, Phú Nhuận, TP. Huế"},
                    {"time": "10:30", "location": "Văn phòng FUTA Huế", "address": "12 Đội Cung, Phường Phú Hội, TP. Huế"}
                ]
            },
            {
                "operator_idx": 0, # Phương Trang
                "bus_type": "Giường nằm 40 chỗ",
                "dep_point": "Đà Nẵng",
                "dest_point": "Huế",
                "dep_time": "10:00",
                "arr_time": "12:30",
                "duration": 150,
                "price": 120000,
                "rating": 4.7,
                "review_count": 67,
                "seat_type_gen": "sleeper_40",
                "pickup": [
                    {"time": "09:30", "location": "Bến xe Trung tâm Đà Nẵng", "address": "Quầy vé FUTA số 14, Bến xe TT Đà Nẵng"}
                ],
                "dropoff": [
                    {"time": "12:30", "location": "Bến xe Phía Bắc Huế", "address": "132 Lý Thái Tổ, An Hòa, TP. Huế"}
                ]
            },
            {
                "operator_idx": 0, # Phương Trang
                "bus_type": "Giường nằm 34 phòng",
                "dep_point": "Đà Nẵng",
                "dest_point": "Huế",
                "dep_time": "13:30",
                "arr_time": "15:45",
                "duration": 135,
                "price": 140000,
                "rating": 4.8,
                "review_count": 112,
                "seat_type_gen": "sleeper_34",
                "pickup": [
                    {"time": "13:10", "location": "Bến xe Trung tâm Đà Nẵng", "address": "185 Tôn Đức Thắng, Liên Chiểu"},
                    {"time": "13:30", "location": "Văn phòng FUTA Nam Trân", "address": "Nam Trân, Hòa Minh, Liên Chiểu"}
                ],
                "dropoff": [
                    {"time": "15:30", "location": "Bến xe Phía Nam Huế", "address": "97 An Dương Vương, TP. Huế"},
                    {"time": "15:45", "location": "Văn phòng FUTA Hùng Vương", "address": "Hùng Vương, TP. Huế"}
                ]
            },
            {
                "operator_idx": 0, # Phương Trang
                "bus_type": "Limousine 9 chỗ VIP",
                "dep_point": "Đà Nẵng",
                "dest_point": "Huế",
                "dep_time": "15:00",
                "arr_time": "17:00",
                "duration": 120,
                "price": 190000,
                "rating": 4.9,
                "review_count": 83,
                "seat_type_gen": "limo_9",
                "pickup": [
                    {"time": "14:45", "location": "Văn phòng FUTA Hải Châu", "address": "36 Bạch Đằng, Hải Châu"},
                    {"time": "15:00", "location": "Văn phòng FUTA Nguyễn Hữu Thọ", "address": "Số 01 Nguyễn Hữu Thọ, Hải Châu"}
                ],
                "dropoff": [
                    {"time": "16:45", "location": "Bến xe Phía Nam Huế", "address": "97 An Dương Vương, TP. Huế"},
                    {"time": "17:00", "location": "Văn phòng FUTA Huế", "address": "12 Đội Cung, Phường Phú Hội, TP. Huế"}
                ]
            },
            {
                "operator_idx": 0, # Phương Trang
                "bus_type": "Giường nằm 34 phòng",
                "dep_point": "Đà Nẵng",
                "dest_point": "Huế",
                "dep_time": "17:30",
                "arr_time": "19:50",
                "duration": 140,
                "price": 135000,
                "rating": 4.8,
                "review_count": 95,
                "seat_type_gen": "sleeper_34",
                "pickup": [
                    {"time": "17:15", "location": "Văn phòng FUTA Đà Nẵng", "address": "65 đường 3 Tháng 2, Hải Châu"}
                ],
                "dropoff": [
                    {"time": "19:50", "location": "Văn phòng FUTA Huế", "address": "12 Đội Cung, Phú Hội, TP. Huế"}
                ]
            },
            {
                "operator_idx": 0, # Phương Trang
                "bus_type": "Giường nằm 34 phòng",
                "dep_point": "Huế",
                "dest_point": "Đà Nẵng",
                "dep_time": "08:00",
                "arr_time": "10:15",
                "duration": 135,
                "price": 140000,
                "rating": 4.8,
                "review_count": 105,
                "seat_type_gen": "sleeper_34",
                "pickup": [
                    {"time": "07:45", "location": "Bến xe Phía Nam Huế", "address": "97 An Dương Vương, TP. Huế"}
                ],
                "dropoff": [
                    {"time": "10:15", "location": "Bến xe Trung tâm Đà Nẵng", "address": "185 Tôn Đức Thắng, Liên Chiểu"}
                ]
            },
            {
                "operator_idx": 0, # Phương Trang
                "bus_type": "Limousine 9 chỗ VIP",
                "dep_point": "Huế",
                "dest_point": "Đà Nẵng",
                "dep_time": "14:00",
                "arr_time": "16:00",
                "duration": 120,
                "price": 190000,
                "rating": 4.9,
                "review_count": 76,
                "seat_type_gen": "limo_9",
                "pickup": [
                    {"time": "13:45", "location": "Văn phòng FUTA Huế", "address": "12 Đội Cung, Phường Phú Hội, TP. Huế"}
                ],
                "dropoff": [
                    {"time": "16:00", "location": "Bến xe Trung tâm Đà Nẵng", "address": "185 Tôn Đức Thắng, Liên Chiểu"}
                ]
            }
        ]

        amenities_default = [
            "Wifi tốc độ cao",
            "Nước suối đóng chai & khăn lạnh",
            "Cổng sạc điện thoại USB",
            "Chăn đắp vệ sinh riêng",
            "Điều hòa khử khuẩn"
        ]

        policies_default = {
            "cancellation": "Hủy vé trước 24 giờ hoàn 95%, trước 12 giờ hoàn 50%, sau 12 giờ không hoàn vé.",
            "baggage": "Mỗi hành khách được miễn cước 20kg hành lý gửi kèm và 1 túi xách tay dưới 5kg.",
            "children": "Trẻ em dưới 5 tuổi hoặc cao dưới 100cm ngồi chung ghế với người lớn được miễn phí vé.",
            "pickup_dropoff": "Có hỗ trợ đón trả khách tận nơi tại các điểm hẹn trước trong nội thành."
        }

        created_trips_count = 0
        created_seats_count = 0

        # Duyệt qua các ngày để tạo chuyến
        for date_str in dates:
            for tmpl in trip_templates:
                operator = operators[tmpl["operator_idx"]]

                # Tạo chuyến xe
                trip = Trip(
                    operator_id=operator.id,
                    bus_type=tmpl["bus_type"],
                    departure_point=tmpl["dep_point"],
                    destination_point=tmpl["dest_point"],
                    departure_time=tmpl["dep_time"],
                    arrival_time=tmpl["arr_time"],
                    duration_minutes=tmpl["duration"],
                    travel_date=date_str,
                    price=tmpl["price"],
                    total_seats=0, # sẽ cập nhật sau khi sinh ghế
                    available_seats=0,
                    rating=tmpl["rating"],
                    review_count=tmpl["review_count"],
                    status="active",
                    pickup_points_json=json.dumps(tmpl["pickup"], ensure_ascii=False),
                    dropoff_points_json=json.dumps(tmpl["dropoff"], ensure_ascii=False),
                    amenities_json=json.dumps(amenities_default, ensure_ascii=False),
                    policies_json=json.dumps(policies_default, ensure_ascii=False),
                )
                db.add(trip)
                db.commit()
                db.refresh(trip)

                # Sinh danh sách ghế mẫu tùy theo loại xe
                seats_list = []
                gen_type = tmpl["seat_type_gen"]

                if gen_type == "limo_9":
                    # Limousine 9 chỗ (1 tầng)
                    # 2 ghế đầu tài xế, 4 ghế VIP giữa, 3 ghế cuối
                    codes = ["A1", "A2", "B1", "B2", "B3", "B4", "C1", "C2", "C3"]
                    for idx, code in enumerate(codes):
                        is_vip = code.startswith("B")
                        # Giả lập một vài ghế đã được đặt trước
                        is_booked = (idx in [1, 4])
                        seats_list.append(Seat(
                            trip_id=trip.id,
                            seat_code=code,
                            seat_type="vip" if is_vip else "standard",
                            status="booked" if is_booked else "available",
                            floor=1,
                            price=trip.price + (30000 if is_vip else 0)
                        ))

                elif gen_type == "sleeper_34":
                    # Giường nằm 34 phòng (Tầng 1: A01..A17; Tầng 2: B01..B17)
                    for i in range(1, 18):
                        code_t1 = f"A{i:02d}"
                        # Giả lập một vài giường tầng 1 đã đặt
                        booked_t1 = (i in [2, 5, 8, 12])
                        seats_list.append(Seat(
                            trip_id=trip.id,
                            seat_code=code_t1,
                            seat_type="vip" if i <= 6 else "standard",
                            status="booked" if booked_t1 else "available",
                            floor=1,
                            price=trip.price
                        ))

                        code_t2 = f"B{i:02d}"
                        booked_t2 = (i in [3, 7, 10])
                        seats_list.append(Seat(
                            trip_id=trip.id,
                            seat_code=code_t2,
                            seat_type="standard",
                            status="booked" if booked_t2 else "available",
                            floor=2,
                            price=trip.price
                        ))

                else: # sleeper_40
                    # Giường nằm 40 chỗ (Tầng 1: A1..A20; Tầng 2: B1..B20)
                    for i in range(1, 21):
                        code_t1 = f"A{i:02d}"
                        booked_t1 = (i in [1, 4, 7, 11, 15])
                        seats_list.append(Seat(
                            trip_id=trip.id,
                            seat_code=code_t1,
                            seat_type="standard",
                            status="booked" if booked_t1 else "available",
                            floor=1,
                            price=trip.price
                        ))

                        code_t2 = f"B{i:02d}"
                        booked_t2 = (i in [2, 6, 9, 14])
                        seats_list.append(Seat(
                            trip_id=trip.id,
                            seat_code=code_t2,
                            seat_type="standard",
                            status="booked" if booked_t2 else "available",
                            floor=2,
                            price=trip.price
                        ))

                # Lưu toàn bộ ghế
                db.bulk_save_objects(seats_list)
                db.commit()

                # Cập nhật lại số ghế thực tế trong Trip
                total_seats = len(seats_list)
                available_seats = sum(1 for s in seats_list if s.status == "available")
                trip.total_seats = total_seats
                trip.available_seats = available_seats
                db.commit()

                created_trips_count += 1
                created_seats_count += len(seats_list)

        print(f"Khởi tạo thành công {len(operators)} nhà xe, {created_trips_count} chuyến xe và {created_seats_count} ghế!")

    except Exception as e:
        db.rollback()
        print(f"Lỗi trong quá trình nạp dữ liệu: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
