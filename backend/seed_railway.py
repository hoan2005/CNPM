import sys
from datetime import datetime, timedelta
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.config import SessionLocal
from backend.model import TuyenDuong, Xe, ChuyenXe, Ghe, GheChuyenXe

def seed_railway_data():
    db = SessionLocal()
    try:
        print("[Railway Seed] Đang kiểm tra dữ liệu hiện tại...")
        existing_tuyen = db.query(TuyenDuong).count()
        if existing_tuyen > 0:
            print(f"[Railway Seed] Đã có {existing_tuyen} tuyến đường trong DB. Bỏ qua nạp lại.")
            return

        print("[Railway Seed] Đang nạp Tuyến đường...")
        tuyen_list = [
            TuyenDuong(diem_di="Đà Nẵng", diem_den="Huế", khoang_cach=100.0, thoi_gian_du_kien=135, trang_thai="HOAT_DONG"),
            TuyenDuong(diem_di="Huế", diem_den="Đà Nẵng", khoang_cach=100.0, thoi_gian_du_kien=135, trang_thai="HOAT_DONG"),
            TuyenDuong(diem_di="Đà Nẵng", diem_den="Hà Nội", khoang_cach=760.0, thoi_gian_du_kien=840, trang_thai="HOAT_DONG"),
            TuyenDuong(diem_di="Đà Nẵng", diem_den="Hồ Chí Minh", khoang_cach=960.0, thoi_gian_du_kien=1020, trang_thai="HOAT_DONG"),
            TuyenDuong(diem_di="Đà Nẵng", diem_den="Nha Trang", khoang_cach=530.0, thoi_gian_du_kien=600, trang_thai="HOAT_DONG")
        ]
        db.add_all(tuyen_list)
        db.commit()
        for t in tuyen_list:
            db.refresh(t)

        print("[Railway Seed] Đang nạp danh sách Xe Phương Trang (FUTA Bus Lines)...")
        xe_list = [
            Xe(bien_so="43B-012.34", loai_xe="Giường nằm 34 phòng", hang_xe="Phương Trang (FUTA Bus Lines)", so_ghe=34, nam_san_xuat=2023, trang_thai="HOAT_DONG"),
            Xe(bien_so="43B-056.78", loai_xe="Limousine 9 chỗ VIP", hang_xe="Phương Trang (FUTA Bus Lines)", so_ghe=9, nam_san_xuat=2024, trang_thai="HOAT_DONG"),
            Xe(bien_so="43B-099.99", loai_xe="Giường nằm 40 chỗ", hang_xe="Phương Trang (FUTA Bus Lines)", so_ghe=40, nam_san_xuat=2022, trang_thai="HOAT_DONG"),
            Xe(bien_so="75B-011.22", loai_xe="Giường nằm 34 phòng", hang_xe="Phương Trang (FUTA Bus Lines)", so_ghe=34, nam_san_xuat=2023, trang_thai="HOAT_DONG")
        ]
        db.add_all(xe_list)
        db.commit()
        for x in xe_list:
            db.refresh(x)

        print("[Railway Seed] Đang tạo sơ đồ Ghế cho từng xe...")
        # 1. Xe Giường nằm 34 phòng: Tầng 1 (A01 - A17), Tầng 2 (B01 - B17)
        for xe in [xe_list[0], xe_list[3]]:
            ghes = []
            for i in range(1, 18):
                ghes.append(Ghe(id_xe=xe.id_xe, so_ghe=f"A{i:02d}", tang=1, loai_ghe="VIP" if i <= 6 else "THUONG"))
            for i in range(1, 18):
                ghes.append(Ghe(id_xe=xe.id_xe, so_ghe=f"B{i:02d}", tang=2, loai_ghe="VIP" if i <= 6 else "THUONG"))
            db.add_all(ghes)

        # 2. Xe Limousine 9 chỗ VIP: Tầng 1 (L01 - L09)
        ghes_limo = [Ghe(id_xe=xe_list[1].id_xe, so_ghe=f"L0{i}", tang=1, loai_ghe="VIP") for i in range(1, 10)]
        db.add_all(ghes_limo)

        # 3. Xe Giường nằm 40 chỗ: Tầng 1 (A01 - A20), Tầng 2 (B01 - B20)
        ghes_40 = []
        for i in range(1, 21):
            ghes_40.append(Ghe(id_xe=xe_list[2].id_xe, so_ghe=f"A{i:02d}", tang=1, loai_ghe="THUONG"))
        for i in range(1, 21):
            ghes_40.append(Ghe(id_xe=xe_list[2].id_xe, so_ghe=f"B{i:02d}", tang=2, loai_ghe="THUONG"))
        db.add_all(ghes_40)

        db.commit()

        print("[Railway Seed] Đang tạo Chuyến xe và Trạng thái ghế...")
        today = datetime.now()
        hours_trips = [
            ("07:00", 0, 140000), # 7h sáng, xe 34 phòng
            ("08:30", 1, 190000), # 8h30 sáng, xe limo 9 chỗ
            ("10:00", 2, 120000), # 10h sáng, xe 40 chỗ
            ("13:30", 0, 140000), # 13h30 chiều, xe 34 phòng
            ("15:00", 1, 190000), # 15h chiều, xe limo 9 chỗ
            ("17:30", 3, 140000), # 17h30 chiều, xe 34 phòng
        ]

        tuyen_dn_hue = tuyen_list[0]
        for day_offset in range(5):
            curr_date = today + timedelta(days=day_offset)
            date_str = curr_date.strftime("%Y-%m-%d")

            for dep_time, xe_idx, price in hours_trips:
                dep_dt = datetime.strptime(f"{date_str} {dep_time}", "%Y-%m-%d %H:%M")
                xe = xe_list[xe_idx]

                chuyen = ChuyenXe(
                    id_tuyen=tuyen_dn_hue.id_tuyen,
                    id_xe=xe.id_xe,
                    thoi_gian_khoi_hanh=dep_dt,
                    thoi_gian_du_kien=135,
                    gia_ve=price,
                    trang_thai="MO_BAN"
                )
                db.add(chuyen)
                db.flush() # Lấy id_chuyen

                # Lấy danh sách ghế của xe này
                ghes_of_xe = db.query(Ghe).filter(Ghe.id_xe == xe.id_xe).all()
                ghe_chuyen_list = []
                # Giả lập một số ghế đã đặt để giao diện trực quan
                for idx, g in enumerate(ghes_of_xe):
                    status = "DA_DAT" if idx in [2, 5, 8, 12] else "TRONG"
                    ghe_chuyen_list.append(GheChuyenXe(
                        id_chuyen=chuyen.id_chuyen,
                        id_ghe=g.id_ghe,
                        trang_thai=status
                    ))
                db.add_all(ghe_chuyen_list)

        db.commit()
        print("[Railway Seed] HOÀN TẤT NẠP DỮ LIỆU LÊN CLOUD RAILWAY THÀNH CÔNG!")
    except Exception as e:
        db.rollback()
        print(f"[Railway Seed Error] {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_railway_data()
