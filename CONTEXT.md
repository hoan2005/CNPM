# TÀI LIỆU CONTEXT DỰ ÁN - ĐỒ ÁN CS434
**Hệ thống Đặt vé xe khách trực tuyến**  
**Module phụ trách:** Tìm kiếm chuyến xe, Chi tiết chuyến xe & Sơ đồ ghế

---

## 1. Tổng quan kiến trúc & Phân công nhiệm vụ

- **Môn học:** Công cụ & Phương pháp Thiết kế - Quản lý phần mềm (CS434)
- **Kiến trúc:** Phân tầng nghiêm ngặt Tách biệt Client - Server:
  - **Backend:** FastAPI + SQLAlchemy theo chuẩn **Router - Controller - Model - Schemas**. Đã cấu hình và kết nối trực tiếp đến CSDL **Cloud MySQL (Railway: `zephyr.proxy.rlwy.net:49810/railway`)**, kèm cơ chế fallback an toàn sang SQLite local (`bus_booking.db`) khi offline.
  - **Frontend:** HTML + Tailwind CSS (thiết kế TransLink), giao tiếp backend qua Fetch API module hóa.
- **Quy tắc làm việc nhóm:**
  1. **Backend:** Chỉ trả về dữ liệu thuần định dạng JSON khi gọi API.
  2. **Router:** Chỉ tiếp nhận HTTP request, parse tham số và chuyển tiếp cho Controller.
  3. **Controller:** Chịu trách nhiệm toàn bộ logic nghiệp vụ (validate ngoại lệ E1, E2, luồng thay thế A1, lọc, sắp xếp, format dữ liệu).
  4. **Frontend:** Điều khiển hiển thị, bắt lỗi người dùng, chuyển trang qua URL query string.
  5. **CORS:** Đã mở `allow_origins=["*"]`, cho phép Live Server (port 5500) hoặc mở file trực tiếp kết nối tới Backend (port 8000).

---

## 2. Cấu trúc thư mục chuẩn hiện tại

```text
d:\ccqltk\
├── backend/
│   ├── main.py                  # Entrypoint FastAPI, CORS, gắn router, auto-seed
│   ├── config.py                # Cấu hình CSDL MySQL (SQLAlchemy + PyMySQL, fallback SQLite, get_db)
│   ├── model/                   # Các bảng dữ liệu (SQLAlchemy Models)
│   │   ├── __init__.py
│   │   ├── railway_models.py    # Bảng chuẩn CSDL nhóm: tuyen_duong, xe, chuyen_xe, ghe, ghe_chuyen_xe
│   │   ├── operator.py          # Bảng operators (nhà xe)
│   │   ├── trip.py              # Bảng trips (chuyến xe)
│   │   └── seat.py              # Bảng seats (sơ đồ ghế)
│   ├── schemas/                 # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── trip.py              # TripSearchResult, TripDetail, TripSearchResponse
│   │   └── seat.py              # SeatOut, SeatMapResponse
│   ├── controller/              # Xử lý toàn bộ logic nghiệp vụ theo Use Case
│   │   ├── __init__.py
│   │   ├── trip_controller.py   # Tìm kiếm, validate E1, A1, bộ lọc, sắp xếp, chi tiết
│   │   └── seat_controller.py   # Sơ đồ ghế phân tầng 1 và tầng 2
│   ├── router/                  # Tiếp nhận HTTP requests và gọi Controller
│   │   ├── __init__.py
│   │   ├── trip_router.py       # Endpoints /api/trips
│   │   └── seat_router.py       # Endpoints /api/trips/{trip_id}/seats
│   ├── seed_railway.py          # Script nạp dữ liệu mẫu lên Cloud MySQL
│   ├── seed_data.py             # Script nạp dữ liệu mẫu SQLite fallback
│   └── test_api.py              # Script kiểm thử tự động toàn bộ API & các ca Use Case
├── frontend/
│   ├── giaodiennguoidung/
│   │   └── timkiemchuyenxe/     # Module phụ trách chính: Tìm kiếm chuyến xe & Sơ đồ ghế
│   │       ├── index.html       # Giao diện Tìm kiếm & Lọc chuyến xe (TransLink)
│   │       ├── trip-detail.html # Giao diện Chi tiết chuyến xe & Sơ đồ ghế 2D (TransLink)
│   │       └── js/
│   │           ├── api.js       # Service gọi API tập trung
│   │           ├── search.js    # Logic tìm kiếm, lọc, dropdown chọn địa điểm, E1/E2, điều hướng
│   │           └── detail.js    # Logic hiển thị chi tiết chuyến, chuyển tầng, chọn ghế & tính tiền
│   ├── giaodienquanly/          # Module quản lý của nhà xe (do thành viên nhóm phụ trách)
│   └── giaodienthanhtoan/       # Module thanh toán & tra cứu vé (do thành viên nhóm phụ trách)
├── bus_booking.db               # SQLite database đã nạp sẵn dữ liệu mẫu
├── requirements.txt             # Thư viện: fastapi, uvicorn, sqlalchemy, pydantic, httpx, pymysql, cryptography
├── requiment.md                 # Ghi chú quy ước kiến trúc nhóm
└── CONTEXT.md                   # Tài liệu context dự án (file này)
```

---

## 3. Đặc tả Nghiệp vụ Use Case & Activity Diagram

### 3.1. Use Case 1: Tìm kiếm chuyến xe
- **Actor:** Khách vãng lai, Khách hàng
- **Mô tả:** Cho phép người dùng tìm các chuyến xe phù hợp dựa trên điểm đi, điểm đến và ngày khởi hành.
- **Luồng sự kiện chính:**
  1. Người dùng bấm/focus vào ô **Điểm đi** hoặc **Điểm đến** → Hiện dropdown danh sách tỉnh thành (66 tỉnh/thành, nhóm "Phổ biến" và danh sách đầy đủ).
  2. Người dùng có thể gõ để lọc nhanh (autocomplete không phân biệt dấu), hoặc bấm vào tên địa điểm để chọn.
  3. Người dùng có thể bấm nút **"Đổi chiều"** để hoán đổi Điểm đi ↔ Điểm đến.
  4. Người dùng chọn ngày khởi hành và số hành khách, rồi bấm nút **"Tìm kiếm"**.
  5. Controller kiểm tra tính hợp lệ dữ liệu.
  6. Truy vấn CSDL và trả về danh sách kết quả cho Frontend hiển thị.
- **Luồng thay thế (A1):** Nếu không nhập ngày đi, hệ thống tự động gán ngày hiện tại (`YYYY-MM-DD`).
- **Luồng ngoại lệ (E1):** Điểm đi == Điểm đến $\rightarrow$ Controller trả về mã lỗi HTTP 400 kèm thông báo: *"Điểm đi và điểm đến không được trùng nhau"*. Frontend hiển thị banner cảnh báo lỗi màu đỏ.
- **Luồng ngoại lệ (E2):** Tuyến không có chuyến xe $\rightarrow$ Trả về danh sách rỗng (`total: 0`), Frontend hiển thị giao diện Empty State *"Không tìm thấy chuyến xe"*.

### 3.2. Use Case 2: Lọc chuyến xe
- **Actor:** Khách vãng lai, Khách hàng
- **Mô tả:** Thu hẹp danh sách chuyến xe theo các tiêu chí bổ sung (khung giờ, loại xe, khoảng giá, nhà xe) và sắp xếp.
- **Luồng sự kiện chính:**
  1. Người dùng chọn tiêu chí lọc:
     - Khung giờ: Sáng sớm (0-6h), Buổi sáng (6-12h), Buổi chiều (12-18h), Buổi tối (18-24h).
     - Loại xe: Limousine, Giường nằm, Ghế ngồi.
     - Mức giá tối đa: Thanh trượt (slider 100k - 500k).
     - Nhà xe: Phương Trang, Hải Vân, Hoàng Long.
     - Sắp xếp: Giờ khởi hành (sớm/muộn), Giá vé (thấp/cao), Đánh giá.
  2. Frontend tự động áp dụng bộ lọc và cập nhật kết quả tức thì.
- **Luồng thay thế (A1):** Nhấn **"Xóa lọc"** $\rightarrow$ Hệ thống reset toàn bộ checkbox/slider và hiển thị lại danh sách gốc.
- **Luồng ngoại lệ (E1):** Không có chuyến xe nào thỏa điều kiện lọc $\rightarrow$ Hiển thị Empty State kèm nút *"Xem tất cả chuyến xe"*.

### 3.3. Use Case 3: Xem thông tin chuyến xe & Sơ đồ ghế
- **Actor:** Khách vãng lai, Khách hàng
- **Mô tả:** Xem chi tiết một chuyến xe (nhà xe, loại xe, giờ đi/đến, điểm đón/trả, tiện ích, chính sách) và sơ đồ ghế 2D để chọn chỗ.
- **Luồng sự kiện chính:**
  1. Người dùng bấm **"Chọn chuyến"** tại thẻ chuyến xe trên trang tìm kiếm $\rightarrow$ Điều hướng sang `trip-detail.html?trip_id=...`.
  2. Hệ thống gọi API chi tiết chuyến xe và API sơ đồ ghế.
  3. Hiển thị timeline điểm đón/trả, tiện ích, chính sách nhà xe.
  4. Hiển thị sơ đồ ghế 2D trực quan phân theo Tầng 1 và Tầng 2.
  5. Người dùng click chọn ghế trống $\rightarrow$ Ghế đổi màu sang đang chọn, bảng tóm tắt giá vé tự động cập nhật số lượng ghế và tổng tiền tạm tính.
- **Luồng ngoại lệ (E1):** Chuyến xe đã hết chỗ hoặc bị hủy $\rightarrow$ Hiển thị banner cảnh báo và nút gợi ý *"Tìm chuyến khác"*.

---

## 4. Đặc tả API Endpoints

Địa chỉ gốc Backend: `http://127.0.0.1:8000`  
Swagger UI tương tác: `http://127.0.0.1:8000/docs`

### 4.1. `GET /api/trips/search` - Tìm kiếm & Lọc chuyến xe
- **Query Parameters:**
  - `departure` (string): Điểm đi (VD: "Đà Nẵng")
  - `destination` (string): Điểm đến (VD: "Huế")
  - `travel_date` (string): Ngày đi (`YYYY-MM-DD`, mặc định: ngày hiện tại)
  - `passengers` (int): Số hành khách (mặc định: 1)
  - `bus_type` (array/string): Lọc loại xe (`Limousine`, `Giường nằm`, `Ghế ngồi`)
  - `operator` (array/string): Lọc nhà xe (`Phương Trang`, `Hải Vân`, `Hoàng Long`)
  - `min_price` (float), `max_price` (float): Lọc khoảng giá
  - `time_slot` (string): `morning` (00:00-12:00), `afternoon` (12:00-18:00), `evening` (18:00-24:00)
  - `sort_by` (string): `departure_time`, `price`, `rating`, `duration`
  - `sort_order` (string): `asc` (tăng dần), `desc` (giảm dần)
- **Response thành công (HTTP 200):**
  ```json
  {
    "total": 6,
    "trips": [
      {
        "id": 1,
        "operator": {
          "id": 1,
          "name": "Phương Trang (FUTA Bus Lines)",
          "logo_url": "https://cdn.futabus.vn/futa-bus/images/logo/logo_futa.svg",
          "phone": "1900 6067",
          "rating": 4.8
        },
        "bus_type": "Giường nằm 34 phòng",
        "departure_point": "Đà Nẵng",
        "destination_point": "Huế",
        "departure_time": "07:00",
        "arrival_time": "09:15",
        "duration_minutes": 135,
        "duration_formatted": "2h 15m",
        "travel_date": "2026-09-10",
        "price": 140000.0,
        "total_seats": 34,
        "available_seats": 27,
        "rating": 4.8,
        "review_count": 128,
        "status": "active",
        "amenities": ["Wifi tốc độ cao", "Nước suối đóng chai", "Cổng sạc USB"]
      }
    ]
  }
  ```
- **Response lỗi E1 (HTTP 400):**
  ```json
  {
    "detail": "Điểm đi và điểm đến không được trùng nhau"
  }
  ```

### 4.2. `GET /api/trips/{trip_id}` - Chi tiết chuyến xe
- **Path Parameter:** `trip_id` (int)
- **Response (HTTP 200):**
  ```json
  {
    "id": 1,
    "operator": {
      "id": 1,
      "name": "Phương Trang (FUTA Bus Lines)",
      "phone": "1900 6067",
      "rating": 4.8
    },
    "bus_type": "Giường nằm 34 phòng",
    "departure_point": "Đà Nẵng",
    "destination_point": "Huế",
    "departure_time": "07:00",
    "arrival_time": "09:15",
    "duration_formatted": "2h 15m",
    "price": 140000.0,
    "available_seats": 27,
    "pickup_points": [
      {"time": "06:40", "location": "Bến xe Trung tâm Đà Nẵng", "address": "185 Tôn Đức Thắng, Liên Chiểu"}
    ],
    "dropoff_points": [
      {"time": "09:15", "location": "Văn phòng Huế", "address": "12 Đội Cung, TP. Huế"}
    ],
    "amenities": ["Wifi tốc độ cao", "Nước suối đóng chai", "Cổng sạc USB"],
    "policies": {
      "cancellation": "Hủy vé trước 24 giờ hoàn 95%, trước 12 giờ hoàn 50%",
      "baggage": "Miễn cước 20kg hành lý gửi và 1 túi xách",
      "children": "Trẻ em dưới 5 tuổi ngồi cùng phụ huynh miễn phí"
    }
  }
  ```

### 4.3. `GET /api/trips/{trip_id}/seats` - Sơ đồ ghế 2D
- **Path Parameter:** `trip_id` (int)
- **Response (HTTP 200):**
  ```json
  {
    "trip_id": 1,
    "bus_type": "Giường nằm 34 phòng",
    "base_price": 140000.0,
    "total_seats": 34,
    "available_seats": 27,
    "booked_seats": 7,
    "floor_1": [
      {"id": 1, "seat_code": "A01", "seat_type": "vip", "status": "available", "floor": 1, "price": 140000.0},
      {"id": 2, "seat_code": "A02", "seat_type": "vip", "status": "booked", "floor": 1, "price": 140000.0}
    ],
    "floor_2": [
      {"id": 18, "seat_code": "B01", "seat_type": "standard", "status": "available", "floor": 2, "price": 140000.0}
    ]
  }
  ```

---

## 5. Hướng dẫn Vận hành & Khởi động

### 5.1. Khởi động Backend API (Port 8000)
```powershell
.\venv\Scripts\uvicorn.exe backend.main:app --host 127.0.0.1 --port 8000 --reload
# Hoặc nếu đã kích hoạt venv:
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5.2. Khởi động Frontend (Port 5500)
Mở terminal riêng chạy:
```powershell
.\venv\Scripts\python.exe -m http.server 5500
```
Hoặc dùng extension **Live Server** trên VS Code mở file `frontend/giaodiennguoidung/timkiemchuyenxe/index.html`.
Truy cập: **`http://127.0.0.1:5500/frontend/giaodiennguoidung/timkiemchuyenxe/index.html`**

### 5.3. Chạy kiểm thử tự động toàn bộ ca kiểm thử (100% Passed)
```powershell
.\venv\Scripts\python.exe -m backend.test_api
```
Script sẽ tự động kiểm tra:
- Health check `GET /`
- Ngoại lệ E1: Trùng điểm đi & đến $\rightarrow$ Báo lỗi 400
- Luồng A1: Không nhập ngày $\rightarrow$ Tự động gán ngày hôm nay
- Ngoại lệ E2: Tuyến không có chuyến $\rightarrow$ Trả về total = 0
- Các bộ lọc (loại xe, nhà xe, khoảng giá, sắp xếp)
- Chi tiết chuyến xe & sơ đồ ghế phân tầng 1/tầng 2
- Xử lý lỗi 404 khi ID không tồn tại
