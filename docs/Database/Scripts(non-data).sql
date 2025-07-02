-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema dacs2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dacs2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dacs2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `dacs2` ;

-- -----------------------------------------------------
-- Table `dacs2`.`bac`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`bac` (
  `MaBac` VARCHAR(5) NOT NULL,
  `TenBac` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MaBac`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`loaidiemdanh`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`loaidiemdanh` (
  `MaLoaiDiemDanh` VARCHAR(5) NOT NULL,
  `TenLoaiDiemDanh` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MaLoaiDiemDanh`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`khoa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`khoa` (
  `MaKhoa` VARCHAR(10) NOT NULL,
  `TenKhoa` VARCHAR(100) NOT NULL,
  `GhiChu` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`MaKhoa`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`giangvien`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`giangvien` (
  `MaGV` INT NOT NULL,
  `TenGiangVien` VARCHAR(100) CHARACTER SET 'utf8mb3' NOT NULL,
  `SDT` INT NULL DEFAULT NULL,
  `MaKhoa` VARCHAR(10) NULL DEFAULT NULL,
  `NamSinh` DATE NULL DEFAULT NULL,
  `GhiChu` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`MaGV`),
  INDEX `fk_gv_khoa_idx` (`MaKhoa` ASC) VISIBLE,
  CONSTRAINT `fk_gv_khoa`
    FOREIGN KEY (`MaKhoa`)
    REFERENCES `dacs2`.`khoa` (`MaKhoa`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`hocky`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`hocky` (
  `MaHocKy` VARCHAR(4) NOT NULL,
  `TenHocKy` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MaHocKy`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`hocphan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`hocphan` (
  `MaHocPhan` VARCHAR(30) NOT NULL,
  `TenHocPhan` VARCHAR(100) NOT NULL,
  `SoTinChi` INT NOT NULL,
  `TongSoTiet` INT NOT NULL,
  PRIMARY KEY (`MaHocPhan`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`nganh`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`nganh` (
  `MaNganh` VARCHAR(5) NOT NULL,
  `TenNganh` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`MaNganh`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`nienkhoa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`nienkhoa` (
  `MaNienKhoa` INT NOT NULL,
  `TenNienKhoa` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`MaNienKhoa`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`lop`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`lop` (
  `MaBac` VARCHAR(5) NOT NULL,
  `MaNienKhoa` INT NOT NULL,
  `MaNganh` VARCHAR(5) NOT NULL,
  `STTLop` VARCHAR(2) NOT NULL,
  `TenLop` VARCHAR(100) CHARACTER SET 'utf8mb3' NOT NULL,
  `MaGV` INT NULL DEFAULT NULL,
  `MaKhoa` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`MaBac`, `MaNienKhoa`, `MaNganh`, `STTLop`),
  INDEX `fk_lop_nganh_idx` (`MaNganh` ASC) VISIBLE,
  INDEX `fk_lop_nienkhoa_idx` (`MaNienKhoa` ASC) VISIBLE,
  INDEX `fk_lop_khoa_idx` (`MaKhoa` ASC) VISIBLE,
  INDEX `fk_lop_gv_idx` (`MaGV` ASC) VISIBLE,
  CONSTRAINT `fk_lop_gv`
    FOREIGN KEY (`MaGV`)
    REFERENCES `dacs2`.`giangvien` (`MaGV`),
  CONSTRAINT `fk_lop_khoa`
    FOREIGN KEY (`MaKhoa`)
    REFERENCES `dacs2`.`khoa` (`MaKhoa`),
  CONSTRAINT `fk_lop_nganh`
    FOREIGN KEY (`MaNganh`)
    REFERENCES `dacs2`.`nganh` (`MaNganh`),
  CONSTRAINT `fk_lop_nienkhoa`
    FOREIGN KEY (`MaNienKhoa`)
    REFERENCES `dacs2`.`nienkhoa` (`MaNienKhoa`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`lophocphan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`lophocphan` (
  `MaLopHocPhan` VARCHAR(20) NOT NULL,
  `MaHocPhan` VARCHAR(30) NOT NULL,
  `MaBac` VARCHAR(5) NOT NULL,
  `MaNienKhoa` INT NOT NULL,
  `MaNganh` VARCHAR(5) NOT NULL,
  `STTLop` VARCHAR(2) NOT NULL,
  `SoBuoi` INT NOT NULL,
  `TietMoiBuoi` INT NOT NULL,
  `MaHocKy` VARCHAR(4) NOT NULL,
  `MaGV` INT NOT NULL,
  PRIMARY KEY (`MaLopHocPhan`),
  INDEX `fk_lophocphan_lop_full_idx` (`MaBac` ASC, `MaNienKhoa` ASC, `MaNganh` ASC, `STTLop` ASC) VISIBLE,
  INDEX `fk_lophocphan_gv_idx` (`MaGV` ASC) VISIBLE,
  INDEX `fk_lophocphan_hocky_idx` (`MaHocKy` ASC) VISIBLE,
  INDEX `fk_lophocphan_hocphan_idx` (`MaHocPhan` ASC) VISIBLE,
  CONSTRAINT `fk_lophocphan_gv`
    FOREIGN KEY (`MaGV`)
    REFERENCES `dacs2`.`giangvien` (`MaGV`),
  CONSTRAINT `fk_lophocphan_hocky`
    FOREIGN KEY (`MaHocKy`)
    REFERENCES `dacs2`.`hocky` (`MaHocKy`),
  CONSTRAINT `fk_lophocphan_hocphan`
    FOREIGN KEY (`MaHocPhan`)
    REFERENCES `dacs2`.`hocphan` (`MaHocPhan`),
  CONSTRAINT `fk_lophocphan_lop_full`
    FOREIGN KEY (`MaBac` , `MaNienKhoa` , `MaNganh` , `STTLop`)
    REFERENCES `dacs2`.`lop` (`MaBac` , `MaNienKhoa` , `MaNganh` , `STTLop`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`buoihoc`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`buoihoc` (
  `MaBuoiHoc` INT NOT NULL AUTO_INCREMENT,
  `MaLopHocPhan` VARCHAR(20) NOT NULL,
  `ThuTuBuoi` INT NOT NULL,
  `NgayHoc` DATE NOT NULL,
  `MaLoaiDiemDanh` VARCHAR(5) NOT NULL,
  `GhiChu` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`MaBuoiHoc`),
  INDEX `fk_buoihoc_lophocphan_idx` (`MaLopHocPhan` ASC) VISIBLE,
  INDEX `fk_buoihoc_loaidiemdanh_idx` (`MaLoaiDiemDanh` ASC) VISIBLE,
  CONSTRAINT `fk_buoihoc_loaidiemdanh`
    FOREIGN KEY (`MaLoaiDiemDanh`)
    REFERENCES `dacs2`.`loaidiemdanh` (`MaLoaiDiemDanh`),
  CONSTRAINT `fk_buoihoc_lophocphan`
    FOREIGN KEY (`MaLopHocPhan`)
    REFERENCES `dacs2`.`lophocphan` (`MaLopHocPhan`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`sinhvien`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`sinhvien` (
  `MaSV` INT NOT NULL,
  `MaBac` VARCHAR(5) NOT NULL,
  `MaNienKhoa` INT NOT NULL,
  `MaNganh` VARCHAR(5) NOT NULL,
  `STTLop` VARCHAR(2) NOT NULL,
  `HoTenSV` VARCHAR(45) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `NamSinh` DATE NULL DEFAULT NULL,
  `DiaChi` VARCHAR(45) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `GioiTinh` VARCHAR(5) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `GhiChu` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`MaSV`),
  INDEX `fk_sv_lop_idx` (`MaBac` ASC, `MaNienKhoa` ASC, `MaNganh` ASC, `STTLop` ASC) VISIBLE,
  CONSTRAINT `fk_sv_lop`
    FOREIGN KEY (`MaBac` , `MaNienKhoa` , `MaNganh` , `STTLop`)
    REFERENCES `dacs2`.`lop` (`MaBac` , `MaNienKhoa` , `MaNganh` , `STTLop`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`trangthaidiemdanh`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`trangthaidiemdanh` (
  `MaTrangThai` VARCHAR(3) NOT NULL,
  `TenTrangThai` VARCHAR(45) NOT NULL,
  `GhiChu` VARCHAR(255) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  PRIMARY KEY (`MaTrangThai`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`diemdanhsv`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`diemdanhsv` (
  `MaBuoiHoc` INT NOT NULL,
  `MaSV` INT NOT NULL,
  `MaTrangThai` VARCHAR(3) NOT NULL,
  `ThoiGianGhiNhan` DATETIME NOT NULL,
  PRIMARY KEY (`MaBuoiHoc`, `MaSV`),
  INDEX `fk_diemdanhsv_sinhvien_idx` (`MaSV` ASC) VISIBLE,
  INDEX `fk_diemdanhsv_trangthai_idx` (`MaTrangThai` ASC) VISIBLE,
  CONSTRAINT `fk_diemdanhsv_buoihoc`
    FOREIGN KEY (`MaBuoiHoc`)
    REFERENCES `dacs2`.`buoihoc` (`MaBuoiHoc`),
  CONSTRAINT `fk_diemdanhsv_sinhvien`
    FOREIGN KEY (`MaSV`)
    REFERENCES `dacs2`.`sinhvien` (`MaSV`),
  CONSTRAINT `fk_diemdanhsv_trangthai`
    FOREIGN KEY (`MaTrangThai`)
    REFERENCES `dacs2`.`trangthaidiemdanh` (`MaTrangThai`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dacs2`.`taikhoan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dacs2`.`taikhoan` (
  `TenDangNhap` VARCHAR(20) NOT NULL,
  `MatKhau` VARCHAR(255) CHARACTER SET 'utf8mb3' NOT NULL,
  `MaGV` INT NOT NULL,
  `VaiTro` ENUM('admin', 'giangvien') NOT NULL,
  `GhiChu` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`TenDangNhap`),
  INDEX `fk_taikhoan_giangvien_idx` (`MaGV` ASC) VISIBLE,
  CONSTRAINT `fk_taikhoan_giangvien`
    FOREIGN KEY (`MaGV`)
    REFERENCES `dacs2`.`giangvien` (`MaGV`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
