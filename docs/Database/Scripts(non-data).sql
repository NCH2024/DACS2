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
-- Table `dacs2`.`NGANH`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`NGANH` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`NGANH` (
  `MaNganh` VARCHAR(5) NOT NULL,
  `TenNganh` VARCHAR(45) NULL,
  PRIMARY KEY (`MaNganh`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`NIENKHOA`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`NIENKHOA` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`NIENKHOA` (
  `MaNienKhoa` INT(3) NOT NULL,
  `TenNienKhoa` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`MaNienKhoa`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`BAC`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`BAC` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`BAC` (
  `MaBac` VARCHAR(5) NOT NULL,
  `TenBac` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MaBac`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`KHOA`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`KHOA` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`KHOA` (
  `MaKhoa` VARCHAR(10) NOT NULL,
  `TenKhoa` VARCHAR(100) NOT NULL,
  `GhiChu` VARCHAR(255) NULL,
  PRIMARY KEY (`MaKhoa`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`GIANGVIEN`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`GIANGVIEN` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`GIANGVIEN` (
  `MaGV` INT(10) NOT NULL,
  `TenGiangVien` NVARCHAR(100) NOT NULL,
  `SDT` INT(11) NULL,
  `MaKhoa` VARCHAR(10) NOT NULL,
  `NamSinh` DATE NULL,
  `GhiChu` VARCHAR(100) NULL,
  PRIMARY KEY (`MaGV`),
  INDEX `fk_gv_khoa_idx` (`MaKhoa` ASC) VISIBLE,
  CONSTRAINT `fk_gv_khoa`
    FOREIGN KEY (`MaKhoa`)
    REFERENCES `dacs2`.`KHOA` (`MaKhoa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`LOP`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`LOP` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`LOP` (
  `MaBac` VARCHAR(5) NOT NULL,
  `MaNienKhoa` INT(3) NOT NULL,
  `MaNganh` VARCHAR(5) NOT NULL,
  `STTLop` VARCHAR(2) NOT NULL,
  `TenLop` NVARCHAR(100) NOT NULL,
  `MaGV` INT(10) NULL,
  `MaKhoa` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`MaBac`, `MaNienKhoa`, `MaNganh`, `STTLop`),
  INDEX `fk_lop_nganh_idx` (`MaNganh` ASC) VISIBLE,
  INDEX `fk_lop_nienkhoa_idx` (`MaNienKhoa` ASC) VISIBLE,
  INDEX `fk_lop_khoa_idx` (`MaKhoa` ASC) VISIBLE,
  INDEX `fk_lop_gv_idx` (`MaGV` ASC) VISIBLE,
  CONSTRAINT `fk_lop_nganh`
    FOREIGN KEY (`MaNganh`)
    REFERENCES `dacs2`.`NGANH` (`MaNganh`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lop_nienkhoa`
    FOREIGN KEY (`MaNienKhoa`)
    REFERENCES `dacs2`.`NIENKHOA` (`MaNienKhoa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lop_bac`
    FOREIGN KEY (`MaBac`)
    REFERENCES `dacs2`.`BAC` (`MaBac`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lop_khoa`
    FOREIGN KEY (`MaKhoa`)
    REFERENCES `dacs2`.`KHOA` (`MaKhoa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lop_gv`
    FOREIGN KEY (`MaGV`)
    REFERENCES `dacs2`.`GIANGVIEN` (`MaGV`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`SINHVIEN`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`SINHVIEN` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`SINHVIEN` (
  `MaSV` INT(10) NOT NULL,
  `MaBac` VARCHAR(5) NOT NULL,
  `MaNienKhoa` INT(3) NOT NULL,
  `MaNganh` VARCHAR(5) NOT NULL,
  `STTLop` VARCHAR(2) NOT NULL,
  `HoTenSV` NVARCHAR(45) NULL,
  `NamSinh` DATE NULL,
  `DiaChi` NVARCHAR(45) NULL,
  `GioiTinh` NVARCHAR(5) NULL,
  `GhiChu` VARCHAR(100) NULL,
  PRIMARY KEY (`MaSV`),
  INDEX `fk_sv_lop_idx` (`MaBac` ASC, `MaNienKhoa` ASC, `MaNganh` ASC, `STTLop` ASC) VISIBLE,
  CONSTRAINT `fk_sv_lop`
    FOREIGN KEY (`MaBac` , `MaNienKhoa` , `MaNganh` , `STTLop`)
    REFERENCES `dacs2`.`LOP` (`MaBac` , `MaNienKhoa` , `MaNganh` , `STTLop`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`HOCPHAN`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`HOCPHAN` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`HOCPHAN` (
  `MaHocPhan` INT(11) NOT NULL,
  `TenHocPhan` VARCHAR(100) NOT NULL,
  `SoTinChi` INT NOT NULL,
  `TongSoTiet` INT NOT NULL,
  PRIMARY KEY (`MaHocPhan`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`HOCKY`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`HOCKY` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`HOCKY` (
  `MaHocKy` VARCHAR(4) NOT NULL,
  `TenHocKy` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MaHocKy`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`LOPHOCPHAN`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`LOPHOCPHAN` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`LOPHOCPHAN` (
  `MaLopHocPhan` VARCHAR(20) NOT NULL,
  `MaHocPhan` INT(11) NOT NULL,
  `MaBac` VARCHAR(5) NOT NULL,
  `MaNienKhoa` INT(3) NOT NULL,
  `MaNganh` VARCHAR(5) NOT NULL,
  `STTLop` VARCHAR(2) NOT NULL,
  `SoBuoi` INT NOT NULL,
  `TietMoiBuoi` INT NOT NULL,
  `MaHocKy` VARCHAR(4) NOT NULL,
  `MaGV` INT(10) NOT NULL,
  PRIMARY KEY (`MaLopHocPhan`),
  INDEX `fk_lophocphan_lop_full_idx` (`MaBac` ASC, `MaNienKhoa` ASC, `MaNganh` ASC, `STTLop` ASC) VISIBLE,
  INDEX `fk_lophocphan_gv_idx` (`MaGV` ASC) VISIBLE,
  INDEX `fk_lophocphan_hocphan_idx` (`MaHocPhan` ASC) VISIBLE,
  INDEX `fk_lophocphan_hocky_idx` (`MaHocKy` ASC) VISIBLE,
  CONSTRAINT `fk_lophocphan_lop_full`
    FOREIGN KEY (`MaBac` , `MaNienKhoa` , `MaNganh` , `STTLop`)
    REFERENCES `dacs2`.`LOP` (`MaBac` , `MaNienKhoa` , `MaNganh` , `STTLop`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lophocphan_gv`
    FOREIGN KEY (`MaGV`)
    REFERENCES `dacs2`.`GIANGVIEN` (`MaGV`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lophocphan_hocphan`
    FOREIGN KEY (`MaHocPhan`)
    REFERENCES `dacs2`.`HOCPHAN` (`MaHocPhan`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lophocphan_hocky`
    FOREIGN KEY (`MaHocKy`)
    REFERENCES `dacs2`.`HOCKY` (`MaHocKy`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`LOAIDIEMDANH`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`LOAIDIEMDANH` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`LOAIDIEMDANH` (
  `MaLoaiDiemDanh` VARCHAR(5) NOT NULL,
  `TenLoaiDiemDanh` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MaLoaiDiemDanh`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`BUOIHOC`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`BUOIHOC` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`BUOIHOC` (
  `MaBuoiHoc` INT NOT NULL AUTO_INCREMENT,
  `MaLopHocPhan` VARCHAR(20) NOT NULL,
  `ThuTuBuoi` INT NOT NULL,
  `NgayHoc` DATE NOT NULL,
  `MaLoaiDiemDanh` VARCHAR(5) NOT NULL,
  `GhiChu` VARCHAR(255) NULL,
  PRIMARY KEY (`MaBuoiHoc`),
  INDEX `fk_buoihoc_lophocphan_idx` (`MaLopHocPhan` ASC) VISIBLE,
  INDEX `fk_buoihoc_loaidiemdanh_idx` (`MaLoaiDiemDanh` ASC) VISIBLE,
  CONSTRAINT `fk_buoihoc_lophocphan`
    FOREIGN KEY (`MaLopHocPhan`)
    REFERENCES `dacs2`.`LOPHOCPHAN` (`MaLopHocPhan`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_buoihoc_loaidiemdanh`
    FOREIGN KEY (`MaLoaiDiemDanh`)
    REFERENCES `dacs2`.`LOAIDIEMDANH` (`MaLoaiDiemDanh`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`TRANGTHAIDIEMDANH`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`TRANGTHAIDIEMDANH` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`TRANGTHAIDIEMDANH` (
  `MaTrangThai` VARCHAR(3) NOT NULL,
  `TenTrangThai` VARCHAR(45) NOT NULL,
  `GhiChu` NVARCHAR(255) NULL,
  PRIMARY KEY (`MaTrangThai`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`DIEMDANHSV`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`DIEMDANHSV` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`DIEMDANHSV` (
  `MaBuoiHoc` INT NOT NULL,
  `MaSV` INT(10) NOT NULL,
  `MaTrangThai` VARCHAR(3) NOT NULL,
  `ThoiGianGhiNhan` DATETIME NOT NULL,
  PRIMARY KEY (`MaBuoiHoc`, `MaSV`),
  INDEX `fk_diemdanhsv_sinhvien_idx` (`MaSV` ASC) VISIBLE,
  INDEX `fk_diemdanhsv_trangthai_idx` (`MaTrangThai` ASC) VISIBLE,
  CONSTRAINT `fk_diemdanhsv_buoihoc`
    FOREIGN KEY (`MaBuoiHoc`)
    REFERENCES `dacs2`.`BUOIHOC` (`MaBuoiHoc`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_diemdanhsv_sinhvien`
    FOREIGN KEY (`MaSV`)
    REFERENCES `dacs2`.`SINHVIEN` (`MaSV`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_diemdanhsv_trangthai`
    FOREIGN KEY (`MaTrangThai`)
    REFERENCES `dacs2`.`TRANGTHAIDIEMDANH` (`MaTrangThai`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dacs2`.`TAIKHOAN`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dacs2`.`TAIKHOAN` ;

CREATE TABLE IF NOT EXISTS `dacs2`.`TAIKHOAN` (
  `TenDangNhap` VARCHAR(20) NOT NULL,
  `MatKhau` NVARCHAR(255) NOT NULL,
  `MaGV` INT(10) NOT NULL,
  `VaiTro` ENUM('admin', 'giangvien') NOT NULL,
  `GhiChu` VARCHAR(255) NULL,
  PRIMARY KEY (`TenDangNhap`),
  INDEX `fk_taikhoan_giangvien_idx` (`MaGV` ASC) VISIBLE,
  CONSTRAINT `fk_taikhoan_giangvien`
    FOREIGN KEY (`MaGV`)
    REFERENCES `dacs2`.`GIANGVIEN` (`MaGV`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
