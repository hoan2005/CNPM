# Frontend
- có 2 giao diện người dùng và quản lý
+ **giao diện người dùng** : đăng ký, đăng nhập , tìm vé, đặt vé , thanh toán ...
+ **giao diện quản lý** : quản lý xe, quản lý vé , quản lý nhân viên , quản lý người dùng ...
- *lưu ý* : 
+ mỗi thành tự hoàn thành chức năng của mình đã phân công( dựa vào thông báo trên trello)
+ nên triễn khau code theo kiểu có 1 file index chung gọi đến phần main của từng giao diện nhỏ bên trong
# Backend
- **config.py**:nơi code các cấu trúc chung của dự án
- **schemas**:nơi  chứa code Pydantic request/response
- **router**: nơi nới nhận và xử lý các request
- **model**: nơi chưa các bảng dữ liệu tương ững với mysql
- **controller**: nơi xử lý các nghiệp vụ
# cách khởi động web
bước 1 : chạy file "main.py" ở backend nhấn vào đường hiệ thị ra ở teminal
bước 2 : bấm vào file frontend index  chọn live server

# quy tắc chung
- beckend chỉ trả về dữ liệu khi gọi API
- việc điều hướng API là do frontend quyết định
- bên trong mỗi file frontend contend của từng phần luôn có phần gọi đến backend để lấy dữ liệu
