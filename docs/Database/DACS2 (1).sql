-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: dacs2
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bac`
--

DROP TABLE IF EXISTS `bac`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bac` (
  `MaBac` varchar(5) NOT NULL,
  `TenBac` varchar(45) NOT NULL,
  PRIMARY KEY (`MaBac`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `buoihoc`
--

DROP TABLE IF EXISTS `buoihoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buoihoc` (
  `MaBuoiHoc` int NOT NULL AUTO_INCREMENT,
  `MaLopHocPhan` int NOT NULL,
  `Thu` int NOT NULL,
  `NgayHoc` date NOT NULL,
  `MaLoaiDiemDanh` varchar(5) NOT NULL,
  `GhiChu` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`MaBuoiHoc`),
  KEY `fk_buoihoc_loaidiemdanh_idx` (`MaLoaiDiemDanh`),
  KEY `fk_buoihoc_lophocphan_idx` (`MaLopHocPhan`),
  CONSTRAINT `fk_buoihoc_loaidiemdanh` FOREIGN KEY (`MaLoaiDiemDanh`) REFERENCES `loaidiemdanh` (`MaLoaiDiemDanh`),
  CONSTRAINT `fk_buoihoc_lophocphan` FOREIGN KEY (`MaLopHocPhan`) REFERENCES `lophocphan` (`MaLopHocPhan`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dangkyhocthem`
--

DROP TABLE IF EXISTS `dangkyhocthem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dangkyhocthem` (
  `MaDangKy` int NOT NULL AUTO_INCREMENT,
  `MaSV` int NOT NULL,
  `MaLopHocPhan` int NOT NULL,
  `NgayDangKy` date DEFAULT NULL,
  `GhiChu` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`MaDangKy`),
  UNIQUE KEY `MaSV` (`MaSV`,`MaLopHocPhan`),
  KEY `MaLopHocPhan` (`MaLopHocPhan`),
  CONSTRAINT `dangkyhocthem_ibfk_1` FOREIGN KEY (`MaSV`) REFERENCES `sinhvien` (`MaSV`),
  CONSTRAINT `dangkyhocthem_ibfk_2` FOREIGN KEY (`MaLopHocPhan`) REFERENCES `lophocphan` (`MaLopHocPhan`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diemdanhsv`
--

DROP TABLE IF EXISTS `diemdanhsv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diemdanhsv` (
  `MaBuoiHoc` int NOT NULL,
  `MaSV` int NOT NULL,
  `MaTrangThai` varchar(3) NOT NULL,
  `ThoiGianGhiNhan` datetime NOT NULL,
  `GhiChu` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`MaBuoiHoc`,`MaSV`),
  KEY `fk_diemdanhsv_sinhvien_idx` (`MaSV`),
  KEY `fk_diemdanhsv_trangthai_idx` (`MaTrangThai`),
  CONSTRAINT `fk_diemdanhsv_buoihoc` FOREIGN KEY (`MaBuoiHoc`) REFERENCES `buoihoc` (`MaBuoiHoc`),
  CONSTRAINT `fk_diemdanhsv_sinhvien` FOREIGN KEY (`MaSV`) REFERENCES `sinhvien` (`MaSV`),
  CONSTRAINT `fk_diemdanhsv_trangthai` FOREIGN KEY (`MaTrangThai`) REFERENCES `trangthaidiemdanh` (`MaTrangThai`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dulieukhuonmat`
--

DROP TABLE IF EXISTS `dulieukhuonmat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dulieukhuonmat` (
  `MaKhuonMat` int NOT NULL AUTO_INCREMENT,
  `MaSV` int NOT NULL,
  `AnhDaiDien` longblob,
  `FaceEncoding` blob,
  `ThoiGianTao` datetime NOT NULL,
  `GhiChu` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`MaKhuonMat`),
  KEY `fk_dulieukhuonmat_sinhvien_idx` (`MaSV`),
  CONSTRAINT `fk_dulieukhuonmat_sinhvien` FOREIGN KEY (`MaSV`) REFERENCES `sinhvien` (`MaSV`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `giangvien`
--

DROP TABLE IF EXISTS `giangvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giangvien` (
  `MaGV` int NOT NULL,
  `TenGiangVien` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `SDT` int DEFAULT NULL,
  `MaKhoa` varchar(10) DEFAULT NULL,
  `NamSinh` date DEFAULT NULL,
  `GhiChu` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`MaGV`),
  KEY `fk_gv_khoa_idx` (`MaKhoa`),
  CONSTRAINT `fk_gv_khoa` FOREIGN KEY (`MaKhoa`) REFERENCES `khoa` (`MaKhoa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hocky`
--

DROP TABLE IF EXISTS `hocky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hocky` (
  `MaHocKy` varchar(4) NOT NULL,
  `TenHocKy` varchar(45) NOT NULL,
  PRIMARY KEY (`MaHocKy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hocphan`
--

DROP TABLE IF EXISTS `hocphan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hocphan` (
  `MaHocPhan` varchar(30) NOT NULL,
  `TenHocPhan` varchar(100) NOT NULL,
  `SoTinChi` int NOT NULL,
  `TongSoTiet` int NOT NULL,
  PRIMARY KEY (`MaHocPhan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `khoa`
--

DROP TABLE IF EXISTS `khoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khoa` (
  `MaKhoa` varchar(10) NOT NULL,
  `TenKhoa` varchar(100) NOT NULL,
  `GhiChu` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`MaKhoa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `loaidiemdanh`
--

DROP TABLE IF EXISTS `loaidiemdanh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loaidiemdanh` (
  `MaLoaiDiemDanh` varchar(5) NOT NULL,
  `TenLoaiDiemDanh` varchar(45) NOT NULL,
  PRIMARY KEY (`MaLoaiDiemDanh`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lop`
--

DROP TABLE IF EXISTS `lop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lop` (
  `MaBac` varchar(5) NOT NULL,
  `MaNienKhoa` int NOT NULL,
  `MaNganh` varchar(5) NOT NULL,
  `STTLop` varchar(2) NOT NULL,
  `TenLop` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `MaGV` int DEFAULT NULL,
  `MaKhoa` varchar(10) NOT NULL,
  PRIMARY KEY (`MaBac`,`MaNienKhoa`,`MaNganh`,`STTLop`),
  KEY `fk_lop_nganh_idx` (`MaNganh`),
  KEY `fk_lop_nienkhoa_idx` (`MaNienKhoa`),
  KEY `fk_lop_khoa_idx` (`MaKhoa`),
  KEY `fk_lop_gv_idx` (`MaGV`),
  CONSTRAINT `fk_lop_gv` FOREIGN KEY (`MaGV`) REFERENCES `giangvien` (`MaGV`),
  CONSTRAINT `fk_lop_khoa` FOREIGN KEY (`MaKhoa`) REFERENCES `khoa` (`MaKhoa`),
  CONSTRAINT `fk_lop_nganh` FOREIGN KEY (`MaNganh`) REFERENCES `nganh` (`MaNganh`),
  CONSTRAINT `fk_lop_nienkhoa` FOREIGN KEY (`MaNienKhoa`) REFERENCES `nienkhoa` (`MaNienKhoa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lophocphan`
--

DROP TABLE IF EXISTS `lophocphan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lophocphan` (
  `MaLopHocPhan` int NOT NULL AUTO_INCREMENT,
  `MaHocPhan` varchar(30) NOT NULL,
  `MaBac` varchar(5) NOT NULL,
  `MaNienKhoa` int NOT NULL,
  `MaNganh` varchar(5) NOT NULL,
  `STTLop` varchar(2) NOT NULL,
  `SoBuoi` int NOT NULL,
  `TietMoiBuoi` int NOT NULL,
  `MaHocKy` varchar(4) NOT NULL,
  `MaGV` int NOT NULL,
  PRIMARY KEY (`MaLopHocPhan`),
  KEY `fk_lophocphan_lop_full_idx` (`MaBac`,`MaNienKhoa`,`MaNganh`,`STTLop`),
  KEY `fk_lophocphan_gv_idx` (`MaGV`),
  KEY `fk_lophocphan_hocky_idx` (`MaHocKy`),
  KEY `fk_lophocphan_hocphan_idx` (`MaHocPhan`),
  CONSTRAINT `fk_lophocphan_gv` FOREIGN KEY (`MaGV`) REFERENCES `giangvien` (`MaGV`),
  CONSTRAINT `fk_lophocphan_hocky` FOREIGN KEY (`MaHocKy`) REFERENCES `hocky` (`MaHocKy`),
  CONSTRAINT `fk_lophocphan_hocphan` FOREIGN KEY (`MaHocPhan`) REFERENCES `hocphan` (`MaHocPhan`),
  CONSTRAINT `fk_lophocphan_lop_full` FOREIGN KEY (`MaBac`, `MaNienKhoa`, `MaNganh`, `STTLop`) REFERENCES `lop` (`MaBac`, `MaNienKhoa`, `MaNganh`, `STTLop`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nganh`
--

DROP TABLE IF EXISTS `nganh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nganh` (
  `MaNganh` varchar(5) NOT NULL,
  `TenNganh` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`MaNganh`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nienkhoa`
--

DROP TABLE IF EXISTS `nienkhoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nienkhoa` (
  `MaNienKhoa` int NOT NULL,
  `TenNienKhoa` varchar(20) NOT NULL,
  PRIMARY KEY (`MaNienKhoa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sinhvien`
--

DROP TABLE IF EXISTS `sinhvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sinhvien` (
  `MaSV` int NOT NULL,
  `MaBac` varchar(5) NOT NULL,
  `MaNienKhoa` int NOT NULL,
  `MaNganh` varchar(5) NOT NULL,
  `STTLop` varchar(2) NOT NULL,
  `HoTenSV` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `NamSinh` date DEFAULT NULL,
  `DiaChi` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `GioiTinh` varchar(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `GhiChu` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`MaSV`),
  KEY `fk_sv_lop_idx` (`MaBac`,`MaNienKhoa`,`MaNganh`,`STTLop`),
  CONSTRAINT `fk_sv_lop` FOREIGN KEY (`MaBac`, `MaNienKhoa`, `MaNganh`, `STTLop`) REFERENCES `lop` (`MaBac`, `MaNienKhoa`, `MaNganh`, `STTLop`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `taikhoan`
--

DROP TABLE IF EXISTS `taikhoan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `taikhoan` (
  `TenDangNhap` varchar(20) NOT NULL,
  `MatKhau` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `MaGV` int NOT NULL,
  `VaiTro` enum('admin','giangvien') NOT NULL,
  `GhiChu` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`TenDangNhap`),
  KEY `fk_taikhoan_giangvien_idx` (`MaGV`),
  CONSTRAINT `fk_taikhoan_giangvien` FOREIGN KEY (`MaGV`) REFERENCES `giangvien` (`MaGV`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `thongbao`
--

DROP TABLE IF EXISTS `thongbao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thongbao` (
  `thongbao_id` int NOT NULL AUTO_INCREMENT,
  `TieuDeThongBao` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `NgayDang` datetime DEFAULT NULL,
  `NoiDung` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `HinhAnh` longblob,
  PRIMARY KEY (`thongbao_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trangthaidiemdanh`
--

DROP TABLE IF EXISTS `trangthaidiemdanh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trangthaidiemdanh` (
  `MaTrangThai` varchar(3) NOT NULL,
  `TenTrangThai` varchar(45) NOT NULL,
  `GhiChu` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`MaTrangThai`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `view_lichdiemdanh_lop`
--

DROP TABLE IF EXISTS `view_lichdiemdanh_lop`;
/*!50001 DROP VIEW IF EXISTS `view_lichdiemdanh_lop`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_lichdiemdanh_lop` AS SELECT 
 1 AS `TenLop`,
 1 AS `TenHocPhan`,
 1 AS `MaBuoiHoc`,
 1 AS `NgayHoc`,
 1 AS `Thu`,
 1 AS `GhiChu`,
 1 AS `MaLoaiDiemDanh`,
 1 AS `MaLopHocPhan`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_lichphancong`
--

DROP TABLE IF EXISTS `view_lichphancong`;
/*!50001 DROP VIEW IF EXISTS `view_lichphancong`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_lichphancong` AS SELECT 
 1 AS `TenDangNhap`,
 1 AS `TenLop`,
 1 AS `TenHocPhan`,
 1 AS `TenHocKy`,
 1 AS `SoBuoi`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `view_lichdiemdanh_lop`
--

/*!50001 DROP VIEW IF EXISTS `view_lichdiemdanh_lop`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_lichdiemdanh_lop` AS select concat(`lhp`.`MaBac`,`lhp`.`MaNienKhoa`,`lhp`.`MaNganh`,lpad(`lhp`.`STTLop`,2,'0')) AS `TenLop`,`hp`.`TenHocPhan` AS `TenHocPhan`,`bh`.`MaBuoiHoc` AS `MaBuoiHoc`,`bh`.`NgayHoc` AS `NgayHoc`,`bh`.`Thu` AS `Thu`,`bh`.`GhiChu` AS `GhiChu`,`bh`.`MaLoaiDiemDanh` AS `MaLoaiDiemDanh`,`lhp`.`MaLopHocPhan` AS `MaLopHocPhan` from ((`buoihoc` `bh` join `lophocphan` `lhp` on((`bh`.`MaLopHocPhan` = `lhp`.`MaLopHocPhan`))) join `hocphan` `hp` on((`lhp`.`MaHocPhan` = `hp`.`MaHocPhan`))) order by `bh`.`NgayHoc` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_lichphancong`
--

/*!50001 DROP VIEW IF EXISTS `view_lichphancong`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_lichphancong` AS select `tk`.`TenDangNhap` AS `TenDangNhap`,concat(`lhp`.`MaBac`,`lhp`.`MaNienKhoa`,`lhp`.`MaNganh`,`lhp`.`STTLop`) AS `TenLop`,`hp`.`TenHocPhan` AS `TenHocPhan`,`hk`.`TenHocKy` AS `TenHocKy`,`lhp`.`SoBuoi` AS `SoBuoi` from ((((`taikhoan` `tk` join `giangvien` `gv` on((`tk`.`MaGV` = `gv`.`MaGV`))) join `lophocphan` `lhp` on((`lhp`.`MaGV` = `gv`.`MaGV`))) join `hocphan` `hp` on((`lhp`.`MaHocPhan` = `hp`.`MaHocPhan`))) join `hocky` `hk` on((`lhp`.`MaHocKy` = `hk`.`MaHocKy`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-16 16:38:08
