from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from ..config import Base

class TuyenDuong(Base):
    __tablename__ = "tuyen_duong"

    id_tuyen = Column(Integer, primary_key=True, index=True, autoincrement=True)
    diem_di = Column(String(100), nullable=False)
    diem_den = Column(String(100), nullable=False)
    khoang_cach = Column(Numeric(10, 2), nullable=True)
    thoi_gian_du_kien = Column(Integer, nullable=True) # phút
    trang_thai = Column(Enum("HOAT_DONG", "NGUNG_HOAT_DONG"), default="HOAT_DONG")

    chuyen_xe = relationship("ChuyenXe", back_populates="tuyen_duong")


class Xe(Base):
    __tablename__ = "xe"

    id_xe = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bien_so = Column(String(20), unique=True, nullable=False)
    loai_xe = Column(String(50), nullable=False) # VD: Giường nằm 34 phòng, Limousine 9 chỗ VIP
    hang_xe = Column(String(50), default="Phương Trang (FUTA Bus Lines)")
    so_ghe = Column(Integer, nullable=False)
    nam_san_xuat = Column(Integer, nullable=True)
    trang_thai = Column(Enum("HOAT_DONG", "BAO_TRI", "NGUNG_HOAT_DONG"), default="HOAT_DONG")

    ghe_list = relationship("Ghe", back_populates="xe")
    chuyen_xe = relationship("ChuyenXe", back_populates="xe")


class ChuyenXe(Base):
    __tablename__ = "chuyen_xe"

    id_chuyen = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_tuyen = Column(Integer, ForeignKey("tuyen_duong.id_tuyen"), nullable=False)
    id_xe = Column(Integer, ForeignKey("xe.id_xe"), nullable=False)
    thoi_gian_khoi_hanh = Column(DateTime, nullable=False)
    thoi_gian_du_kien = Column(Integer, nullable=True)
    gia_ve = Column(Numeric(12, 2), nullable=False)
    trang_thai = Column(Enum("MO_BAN", "DA_DAY", "DA_KHOI_HANH", "HOAN_THANH", "HUY"), default="MO_BAN")

    tuyen_duong = relationship("TuyenDuong", back_populates="chuyen_xe")
    xe = relationship("Xe", back_populates="chuyen_xe")
    ghe_chuyen_xe = relationship("GheChuyenXe", back_populates="chuyen_xe")


class Ghe(Base):
    __tablename__ = "ghe"

    id_ghe = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_xe = Column(Integer, ForeignKey("xe.id_xe"), nullable=False)
    so_ghe = Column(String(10), nullable=False) # A01, A02, B01...
    tang = Column(Integer, default=1)
    loai_ghe = Column(Enum("THUONG", "VIP"), default="THUONG")

    xe = relationship("Xe", back_populates="ghe_list")
    ghe_chuyen_xe = relationship("GheChuyenXe", back_populates="ghe")


class GheChuyenXe(Base):
    __tablename__ = "ghe_chuyen_xe"

    id_ghe_chuyen = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_chuyen = Column(Integer, ForeignKey("chuyen_xe.id_chuyen"), nullable=False)
    id_ghe = Column(Integer, ForeignKey("ghe.id_ghe"), nullable=False)
    trang_thai = Column(Enum("TRONG", "DA_GIU", "DA_DAT", "DA_SU_DUNG"), default="TRONG")

    chuyen_xe = relationship("ChuyenXe", back_populates="ghe_chuyen_xe")
    ghe = relationship("Ghe", back_populates="ghe_chuyen_xe")
