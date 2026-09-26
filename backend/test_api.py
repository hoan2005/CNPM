import sys
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def run_tests():
    print("--- 1. Kiểm tra GET / (Health check) ---")
    res = client.get("/")
    assert res.status_code == 200, f"Lỗi GET /: {res.status_code}"
    print("GET / OK:", res.json()["message"])

    print("\n--- 2. Kiểm tra Ngoại lệ E1: Điểm đi == Điểm đến (Báo lỗi 400) ---")
    res_e1 = client.get("/api/trips/search?departure=Đà Nẵng&destination=Đà Nẵng")
    assert res_e1.status_code == 400, f"Phải trả về 400 khi điểm đi == điểm đến, nhưng nhận {res_e1.status_code}"
    assert "Điểm đi và điểm đến không được trùng nhau" in res_e1.json()["detail"]
    print("Validate E1 (Điểm đi = Điểm đến) OK:", res_e1.json()["detail"])

    print("\n--- 3. Kiểm tra Luồng thay thế A1: Không chọn ngày -> Tự lấy ngày hôm nay ---")
    res_a1 = client.get("/api/trips/search?departure=Đà Nẵng&destination=Huế")
    assert res_a1.status_code == 200
    print(f"Tìm kiếm mặc định: Tìm thấy {res_a1.json()['total']} chuyến xe")

    print("\n--- 4. Kiểm tra Ngoại lệ E2: Tuyến không có chuyến xe nào ---")
    res_e2 = client.get("/api/trips/search?departure=Cà Mau&destination=Lạng Sơn")
    assert res_e2.status_code == 200
    assert res_e2.json()["total"] == 0
    assert len(res_e2.json()["trips"]) == 0
    print("Xử lý E2 (Không tìm thấy chuyến xe) OK: total = 0")

    print("\n--- 5. Kiểm tra các bộ lọc search trong Controller ---")
    # Lọc theo loại xe
    res_type = client.get("/api/trips/search?departure=Đà Nẵng&destination=Huế&bus_type=Limousine")
    assert res_type.status_code == 200
    print(f"Lọc loại xe Limousine: {res_type.json()['total']} chuyến")

    # Lọc theo nhà xe
    res_op = client.get("/api/trips/search?departure=Đà Nẵng&destination=Huế&operator=Phương Trang")
    assert res_op.status_code == 200
    print(f"Lọc nhà xe Phương Trang: {res_op.json()['total']} chuyến")

    # Lọc theo khoảng giá
    res_price = client.get("/api/trips/search?departure=Đà Nẵng&destination=Huế&min_price=150000")
    assert res_price.status_code == 200
    print(f"Lọc giá >= 150.000đ: {res_price.json()['total']} chuyến")

    # Sắp xếp giá tăng dần
    res_sort = client.get("/api/trips/search?departure=Đà Nẵng&destination=Huế&sort_by=price&sort_order=asc")
    assert res_sort.status_code == 200
    prices = [t["price"] for t in res_sort.json()["trips"]]
    assert prices == sorted(prices), "Sắp xếp giá không đúng thứ tự asc!"
    print(f"Sắp xếp giá tăng dần OK: {prices[:4]}...")

    print("\n--- 6. Kiểm tra GET /api/trips/{trip_id} (Chi tiết chuyến xe) ---")
    first_trip = res_a1.json()["trips"][0]
    res_detail = client.get(f"/api/trips/{first_trip['id']}")
    assert res_detail.status_code == 200, f"Lỗi lấy chi tiết: {res_detail.status_code}"
    detail = res_detail.json()
    print(f"Chi tiết chuyến ID {first_trip['id']}: Nhà xe {detail['operator']['name']}, {len(detail['pickup_points'])} điểm đón")

    print("\n--- 7. Kiểm tra GET /api/trips/{trip_id}/seats (Sơ đồ ghế) ---")
    res_seats = client.get(f"/api/trips/{first_trip['id']}/seats")
    assert res_seats.status_code == 200, f"Lỗi lấy ghế: {res_seats.status_code}"
    seat_map = res_seats.json()
    print(f"Sơ đồ ghế: Tổng {seat_map['total_seats']}, Trống {seat_map['available_seats']}, Đã đặt {seat_map['booked_seats']}")
    print(f"Tầng 1: {len(seat_map['floor_1'])} ghế, Tầng 2: {len(seat_map['floor_2'])} ghế")

    print("\n--- 8. Kiểm tra 404 khi không tìm thấy chuyến ---")
    res_404 = client.get("/api/trips/999999")
    assert res_404.status_code == 404
    print("404 Error handling OK!")

    print("\n========================================================")
    print(" TẤT CẢ TEST CASES (MVC + USE CASE FLOWS) THÀNH CÔNG 100%! ")
    print("========================================================")

if __name__ == "__main__":
    run_tests()
