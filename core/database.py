'''
FILE NAME: core/database.py
CODE BY: Nguyễn Chánh Hiệp 
DATE: 22/06/2025
DESCRIPTION:
        + Đây là file chứa các hàm tương tác với cơ sở dữ liệu
        + Định nghĩa các hàm lấy dữ liệu, lưu trữ dữ liệu
        + Các hàm này sẽ được sử dụng để hỗ trợ cho các model và controller
VERSION: 1.0.0
'''
from socket import timeout
import mysql.connector
from core.utils import *
from PIL import Image
from datetime import datetime, timedelta
import io
import pickle
import numpy as np
from mysql.connector import Error

DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'database': 'dacs2'
        }

def connect_db():
    """
    Kết nối đến cơ sở dữ liệu MySQL.
    Trả về một kết nối vào cơ sở dữ liệu.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
# ĐOẠN KẾT NỐI DƯỚI ĐÂY ĐANG THỬ NGHIỆM CHO CLOUD DATABASE AIVEN (Do vẫn còn lỗi nên chưa áp dụng thực tế)
# DB_CONFIG = {
#     'host': 'mysql-bd31deb-chanhhiep-04d9.k.aivencloud.com',
#     'user': 'avnadmin',
#     'password': 'AVNS_fYJ141qHPpEqOQlsKk1',
#     'database': 'da2',
#     'port': 25447,
#     'ssl_disabled': False
# }

# def connect_db():
#     try:
#         connection = mysql.connector.connect(**DB_CONFIG)
#         if connection.is_connected():
#             return connection
#     except Error as err:
#         print(f"Database connection error: {err}")
#         return None


    
def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT TenDangNhap, MatKhau, VaiTro FROM taikhoan WHERE TenDangNhap = %s", (username,))
    result = cursor.fetchone()

    if not result:
        return False

    user_id, bcrypt_password, role = result
        
    print(f"user_id: {user_id}, role: {role}")

    if check_password(password, bcrypt_password):
        return user_id, role
    else:
        return False

def get_username(tendangnhap):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT gv.TenGiangVien FROM taikhoan tk JOIN giangvien gv ON tk.MaGV = gv.MaGV WHERE tk.TenDangNhap = %s;", (tendangnhap,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else :
        return False


def get_info_lecturer(tendangnhap):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT gv.MaGV, gv.TenGiangVien, gv.SDT, gv.MaKhoa, gv.NamSinh, gv.GhiChu FROM taikhoan tk JOIN giangvien gv ON tk.MaGV = gv.MaGV WHERE tk.TenDangNhap = %s;", (tendangnhap,))
    result = cursor.fetchone()
    
    MaGV, TenGiangVien, SDT, MaKhoa, NamSinh, GhiChu = result
    if result:
        return MaGV, TenGiangVien, SDT, MaKhoa, NamSinh, GhiChu
    else:
        return False
    

def get_thongbao():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT thongbao_id, TieuDeThongBao, NoiDung, NgayDang, HinhAnh FROM thongbao order by NgayDang DESC")
    results = []

    for row in cursor.fetchall():
        thongbao_id, title, content, ngay_dang, image_blob = row
        # Chuyển ảnh blob thành PIL Image
        if image_blob:
            image = Image.open(io.BytesIO(image_blob))
        else:
            image = None
        results.append((thongbao_id, title, content, ngay_dang, image))

    cursor.close()
    conn.close()
    return results



        
def get_schedule(tendangnhap):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM view_lichphancong WHERE TenDangNhap = %s;", (tendangnhap, ))
    data = []
    
    for row in cursor.fetchall():
        tendangnhap, tenlop, tenhocphan, hocky, sobuoi = row
        data.append((tenlop, tenhocphan, hocky, sobuoi))
        
    if data:
        return data
    else:
        return False
    
def get_classes_of_lecturer(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT TenLop 
        FROM view_lichphancong
        WHERE TenDangNhap = %s;
    """, (username,))
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]

def get_subjects_by_class(username, class_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT TenHocPhan 
        FROM view_lichphancong
        WHERE TenDangNhap = %s AND TenLop = %s;
    """, (username, class_name))
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]


def get_schedule_by_week(class_name, subject_name, week_offset=0):
    conn = connect_db()
    cursor = conn.cursor()

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)

    cursor.execute("""
        SELECT TenLop, TenHocPhan, MaBuoiHoc, NgayHoc, Thu, GhiChu, MaLoaiDiemDanh, MaLopHocPhan
        FROM view_lichdiemdanh_lop
        WHERE TenLop = %s AND TenHocPhan = %s
            AND NgayHoc BETWEEN %s AND %s
        ORDER BY NgayHoc ASC;

         """, (class_name, subject_name, start_of_week.date(), end_of_week.date()))

    result = cursor.fetchall()
    conn.close()

    return result

def get_subject_detail_from_hocphan(subject_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MaHocPhan, TenHocPhan, SoTinChi, TongSoTiet
        FROM HocPhan
        WHERE TenHocPhan = %s
        LIMIT 1
    """, (subject_name,))
    row = cursor.fetchone()
    return row if row else ("", "", "", "")

def get_student_by_id(maSV):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            sv.MaSV, 
            b.TenBac,         -- Tên bậc học
            nk.TenNienKhoa,   -- Tên niên khoá
            n.TenNganh,       -- Tên ngành
            sv.MaBac,
            sv.MaNienKhoa,
            sv.MaNganh,
            sv.STTLop,
            sv.HoTenSV,
            sv.NamSinh,
            sv.DiaChi,
            sv.GioiTinh,
            sv.GhiChu
        FROM sinhvien sv
        LEFT JOIN bac b ON sv.MaBac = b.MaBac
        LEFT JOIN nienkhoa nk ON sv.MaNienKhoa = nk.MaNienKhoa
        LEFT JOIN nganh n ON sv.MaNganh = n.MaNganh
        WHERE sv.MaSV = %s
    """, (maSV,))
    return cursor.fetchone()

def get_subjects_of_lecturer(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT hp.TenHocPhan
        FROM taikhoan tk
        JOIN giangvien gv ON tk.MaGV = gv.MaGV
        JOIN lophocphan lhp ON lhp.MaGV = gv.MaGV
        JOIN hocphan hp ON lhp.MaHocPhan = hp.MaHocPhan
        WHERE tk.TenDangNhap = %s
    """, (username,))
    result = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return result

def get_dates_of_subject(username, ten_hocphan):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT bh.NgayHoc
        FROM taikhoan tk
        JOIN giangvien gv ON tk.MaGV = gv.MaGV
        JOIN lophocphan lhp ON lhp.MaGV = gv.MaGV
        JOIN hocphan hp ON lhp.MaHocPhan = hp.MaHocPhan
        JOIN buoihoc bh ON bh.MaLopHocPhan = lhp.MaLopHocPhan
        WHERE tk.TenDangNhap = %s AND hp.TenHocPhan = %s
        ORDER BY bh.NgayHoc DESC
    """, (username, ten_hocphan))
    result = [row[0].strftime("%d/%m/%Y") if hasattr(row[0], 'strftime') else str(row[0]) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return result

def get_sessions_of_date(username, ten_hocphan, ngay):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        date_obj = datetime.strptime(ngay, "%d/%m/%Y")
        ngay_sql = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return []

    cursor.execute("""
        SELECT ldd.TenLoaiDiemDanh
        FROM taikhoan tk
        JOIN giangvien gv ON tk.MaGV = gv.MaGV
        JOIN lophocphan lhp ON lhp.MaGV = gv.MaGV
        JOIN hocphan hp ON lhp.MaHocPhan = hp.MaHocPhan
        JOIN buoihoc bh ON bh.MaLopHocPhan = lhp.MaLopHocPhan
        JOIN loaidiemdanh ldd ON bh.MaLoaiDiemDanh = ldd.MaLoaiDiemDanh
        WHERE tk.TenDangNhap = %s AND hp.TenHocPhan = %s AND bh.NgayHoc = %s
        ORDER BY bh.MaBuoiHoc
    """, (username, ten_hocphan, ngay_sql))

    result = [str(row[0]) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return result



def get_loai_diem_danh(username, ten_hocphan, ngay):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        date_obj = datetime.strptime(ngay, "%d/%m/%Y")
        ngay_sql = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print("Lỗi định dạng ngày!")
        return []

    cursor.execute("""
        SELECT DISTINCT ldd.MaLoaiDiemDanh, ldd.TenLoaiDiemDanh
        FROM taikhoan tk
        JOIN giangvien gv ON tk.MaGV = gv.MaGV
        JOIN lophocphan lhp ON lhp.MaGV = gv.MaGV
        JOIN hocphan hp ON lhp.MaHocPhan = hp.MaHocPhan
        JOIN buoihoc bh ON bh.MaLopHocPhan = lhp.MaLopHocPhan
        JOIN loaidiemdanh ldd ON bh.MaLoaiDiemDanh = ldd.MaLoaiDiemDanh
        WHERE tk.TenDangNhap = %s AND hp.TenHocPhan = %s AND bh.NgayHoc = %s
    """, (username, ten_hocphan, ngay_sql))

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    # Lưu dưới dạng dict: {tên: mã}
    return {ten: ma for ma, ten in result}

def get_attendance_of_student(maSV, ten_hocphan, ngay, buoi):  
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
                        SELECT 
                            hp.TenHocPhan,
                            bh.NgayHoc,
                            bh.MaLoaiDiemDanh,
                            dd.ThoiGianGhiNhan,
                            tt.TenTrangThai
                        FROM buoihoc bh
                        JOIN lophocphan lhp ON bh.MaLopHocPhan = lhp.MaLopHocPhan
                        JOIN hocphan hp ON lhp.MaHocPhan = hp.MaHocPhan
                        LEFT JOIN diemdanhsv dd ON dd.MaBuoiHoc = bh.MaBuoiHoc AND dd.MaSV = %s
                        LEFT JOIN trangthaidiemdanh tt ON dd.MaTrangThai = tt.MaTrangThai
                        WHERE TRIM(hp.TenHocPhan) = %s
                        AND bh.NgayHoc = %s
                        AND UPPER(TRIM(bh.MaLoaiDiemDanh)) = UPPER(%s)
                    """, (maSV, ten_hocphan.strip(), ngay, buoi.strip()))
    
    result = cursor.fetchone()
    return result

def get_attendance_list_of_class(class_name, subject_name, ngay, buoi):
    conn = connect_db()
    cursor = conn.cursor(buffered=True) # Sử dụng buffered=True để tránh lỗi nếu có nhiều kết quả

    try:
        # Chuyển đổi ngày sang định dạng 'YYYY-MM-DD' để phù hợp với tham số DATE của Stored Procedure
        date_obj = datetime.strptime(ngay, "%d/%m/%Y")
        ngay_sql = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print("Lỗi định dạng ngày. Vui lòng nhập ngày theo định dạng dd/mm/YYYY (ví dụ: 15/01/2025).")
        if conn:
            conn.close()
        return []

    try:
        # Gọi Stored Procedure và truyền các tham số
        # Tên Stored Procedure là GetAttendanceListByClass
        # Tham số truyền vào phải đúng thứ tự: class_name, subject_name, ngay, buoi
        call_proc_sql = "CALL GetAttendanceListByClass(%s, %s, %s, %s);"
        
        # Thực thi Stored Procedure với các tham số đã chuẩn bị
        cursor.execute(call_proc_sql, (class_name, subject_name, ngay_sql, buoi))

        # Lấy tất cả kết quả trả về từ Stored Procedure
        results = cursor.fetchall()
        
    except Exception as e:
        # Xử lý lỗi nếu có vấn đề khi gọi Stored Procedure
        print(f"Lỗi khi gọi Stored Procedure 'GetAttendanceListByClass': {e}")
        results = [] # Trả về danh sách rỗng nếu có lỗi
    finally:
        # Đảm bảo kết nối database luôn được đóng
        if conn:
            conn.close()
    
    return results

def get_data_face_trainning(MaSV):
    conn = connect_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT AnhDaiDien, FaceEncoding, ThoiGianTao FROM dulieukhuonmat WHERE MaSV = %s"
        cursor.execute(query, (MaSV,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        print(f"Lỗi khi truy vấn dữ liệu khuôn mặt cho MaSV {MaSV}: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def load_face_encodings():
    """
    Tải tất cả các FaceEncoding và MaSV tương ứng từ bảng dulieukhuonmat vào bộ nhớ.
    Trả về hai danh sách: known_face_encodings và known_face_student_ids.
    """
    known_face_encodings = []
    known_face_student_ids = []
    conn = connect_db()
    if conn is None:
        return known_face_encodings, known_face_student_ids

    try:
        cursor = conn.cursor()
        query = "SELECT MaSV, FaceEncoding FROM dulieukhuonmat"
        cursor.execute(query)

        for (ma_sv, face_encoding_blob) in cursor:
            try:
                # Giải mã dữ liệu BLOB thành mảng numpy
                face_encoding_array = pickle.loads(face_encoding_blob)
                known_face_encodings.append(face_encoding_array)
                known_face_student_ids.append(ma_sv)
            except Exception as e:
                print(f"Lỗi khi giải mã FaceEncoding cho MaSV {ma_sv}: {e}")
                continue

    except mysql.connector.Error as err:
        print(f"Lỗi khi truy vấn dữ liệu khuôn mặt: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    print(f"Đã tải {len(known_face_encodings)} khuôn mặt từ CSDL.")
    return known_face_encodings, known_face_student_ids

def save_face_encoding(ma_sv, face_encoding_array, ghi_chu=None):
    """
    Lưu một FaceEncoding mới hoặc cập nhật FaceEncoding nếu MaSV đã tồn tại.
    """
    conn = connect_db()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        face_encoding_blob = pickle.dumps(face_encoding_array)

        # Kiểm tra xem MaSV đã tồn tại chưa
        check_query = "SELECT COUNT(*) FROM dulieukhuonmat WHERE MaSV = %s"
        cursor.execute(check_query, (ma_sv,))
        if cursor.fetchone()[0] > 0:
            # Nếu đã tồn tại, cập nhật
            update_query = """
                UPDATE dulieukhuonmat
                SET FaceEncoding = %s, ThoiGianTao = NOW(), GhiChu = %s
                WHERE MaSV = %s
            """
            cursor.execute(update_query, (face_encoding_blob, ghi_chu, ma_sv))
            print(f"Đã cập nhật FaceEncoding cho MaSV {ma_sv} thành công.")
        else:
            # Nếu chưa tồn tại, thêm mới
            insert_query = """
                INSERT INTO dulieukhuonmat (MaSV, FaceEncoding, ThoiGianTao, GhiChu)
                VALUES (%s, %s, NOW(), %s)
            """
            cursor.execute(insert_query, (ma_sv, face_encoding_blob, ghi_chu))
            print(f"Đã lưu FaceEncoding cho MaSV {ma_sv} thành công.")
        
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Lỗi khi lưu/cập nhật FaceEncoding cho MaSV {ma_sv}: {err}")
        conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_student_info_by_ma_sv(ma_sv):
    """
    Lấy thông tin chi tiết của sinh viên để hiển thị trên bảng điểm danh
    khi sinh viên được nhận dạng (ví dụ: Tên, Năm Sinh, Giới tính).
    """
    conn = connect_db()
    if conn is None:
        return None

    student_info = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT TenSV, NamSinh, GioiTinh
            FROM sinhvien
            WHERE MaSV = %s
        """
        cursor.execute(query, (ma_sv,))
        result = cursor.fetchone()
        if result:
            student_info = {
                "TenSV": result[0],
                "NamSinh": result[1],
                "GioiTinh": result[2]
            }
    except mysql.connector.Error as err:
        print(f"Lỗi khi lấy thông tin sinh viên cho MaSV {ma_sv}: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return student_info

def record_attendance(ma_sv, ma_buoi_hoc, ma_trang_thai="CM"):
    conn = connect_db()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        # Lấy MaTrangThai từ TenTrangThai hoặc nếu 'DD' là mã thì dùng trực tiếp
        # Nếu TenTrangThai lưu tên, đổi logic phù hợp. Đây ví dụ giả sử 'DD' là MaTrangThai.
        ma_trang_thai = ma_trang_thai

        # Kiểm tra đã điểm danh chưa
        cursor.execute("SELECT COUNT(*) FROM diemdanhsv WHERE MaSV=%s AND MaBuoiHoc=%s", (ma_sv, ma_buoi_hoc))
        if cursor.fetchone()[0] > 0:
            return False

        cursor.execute("INSERT INTO diemdanhsv (MaBuoiHoc, MaSV , MaTrangThai, ThoiGianGhiNhan) VALUES (%s, %s, %s, NOW())",
                       (ma_buoi_hoc, ma_sv, ma_trang_thai))
        conn.commit()
        return True
    except Exception as e:
        print("record_attendance_by_ma_buoi error:", e)
        conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_ma_lop_hoc_phan(class_name_str, subject_name):
    """
    Lấy MaLopHocPhan dựa trên chuỗi lớp (ví dụ: DH21TINTT01) và tên học phần.
    Hữu ích khi bạn cần MaLopHocPhan để ghi nhận điểm danh.
    """
    conn = connect_db()
    if conn is None:
        return None

    ma_lop_hoc_phan = None
    try:
        cursor = conn.cursor()
        # Phân tích class_name_str để lấy các thành phần
        ma_bac = class_name_str[0:2]
        ma_nien_khoa = class_name_str[2:4]
        # Giả định MaNganh có thể có độ dài thay đổi, lấy phần còn lại trước 2 ký tự cuối
        ma_nganh = class_name_str[4:-2] 
        stt_lop = class_name_str[-2:]

        query = """
            SELECT lhp.MaLopHocPhan
            FROM lophocphan lhp
            JOIN hocphan hp ON lhp.MaHocPhan = hp.MaHocPhan
            WHERE lhp.MaBac = %s AND lhp.MaNienKhoa = %s AND lhp.MaNganh = %s AND lhp.STTLop = %s
            AND hp.TenHocPhan = %s
        """
        cursor.execute(query, (ma_bac, ma_nien_khoa, ma_nganh, stt_lop, subject_name))
        result = cursor.fetchone()
        if result:
            ma_lop_hoc_phan = result[0]
    except mysql.connector.Error as err:
        print(f"Lỗi khi lấy MaLopHocPhan: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return ma_lop_hoc_phan

def get_ma_loai_diem_danh(ten_loai_diem_danh):
    """
    Lấy MaLoaiDiemDanh từ TenLoaiDiemDanh.
    """
    conn = connect_db()
    if conn is None:
        return None
    
    ma_loai = None
    try:
        cursor = conn.cursor()
        query = "SELECT MaLoaiDiemDanh FROM loaidiemdanh WHERE TenLoaiDiemDanh = %s"
        cursor.execute(query, (ten_loai_diem_danh,))
        result = cursor.fetchone()
        if result:
            ma_loai = result[0]
    except mysql.connector.Error as err:
        print(f"Lỗi khi lấy MaLoaiDiemDanh: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return ma_loai


def update_student_face_data(ma_sv, embedding_blob, image_blob, thoi_gian_cap_nhat):
    """
    Saves or updates a student's face data (embedding and image) in the database.
    """
    conn = connect_db()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check if the student ID already has a face record
        check_query = "SELECT COUNT(*) FROM dulieukhuonmat WHERE MaSV = %s"
        cursor.execute(check_query, (ma_sv,))
        record_exists = cursor.fetchone()[0] > 0

        if record_exists:
            # If a record exists, update it
            update_query = """
                UPDATE dulieukhuonmat
                SET FaceEncoding = %s, AnhDaiDien = %s, ThoiGianTao = %s
                WHERE MaSV = %s
            """
            cursor.execute(update_query, (embedding_blob, image_blob, thoi_gian_cap_nhat, ma_sv))
            print(f"Đã cập nhật dữ liệu khuôn mặt cho MaSV {ma_sv} thành công.")
        else:
            # If no record exists, insert a new one
            insert_query = """
                INSERT INTO dulieukhuonmat (MaSV, AnhDaiDien, FaceEncoding, ThoiGianTao)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (ma_sv, image_blob, embedding_blob, thoi_gian_cap_nhat))
            print(f"Đã thêm dữ liệu khuôn mặt mới cho MaSV {ma_sv} thành công.")
        
        conn.commit()
        return True
    
    except mysql.connector.Error as err:
        print(f"Lỗi khi lưu dữ liệu khuôn mặt cho MaSV {ma_sv}: {err}")
        conn.rollback()
        return False
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
def get_student_face_data(ma_sv):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AnhDaiDien, FaceEncoding, ThoiGianTao
        FROM dulieukhuonmat
        WHERE MaSV=%s
    """, (ma_sv,))
    conn.commit()
    cursor.close()
    conn.close()

def get_ma_buoi_hoc(class_name, subject_name, date_str, session_name):
    """
    Lấy MaBuoiHoc từ CSDL.
    """
    conn = connect_db()
    if conn is None:
        return None

    # --- Bước 1: Phân tích chuỗi tên lớp (class_name) ---
    # Ví dụ: "DH21TINTT01"
    try:
        ma_bac = class_name[0:2]          # -> "DH"
        # MaNienKhoa trong CSDL là kiểu INT [cite: 182]
        ma_nien_khoa = int(class_name[2:4]) # -> 21 
        ma_nganh = class_name[4:-2]       # -> "TINTT"
        stt_lop = class_name[-2:]         # -> "01"
    except (IndexError, ValueError) as e:
        # Xử lý nếu chuỗi class_name không đúng định dạng
        print(f"Lỗi nghiêm trọng: Định dạng tên lớp '{class_name}' không hợp lệ. Không thể phân tích. Lỗi: {e}")
        return None
        
    # --- Bước 2: Chuyển đổi định dạng ngày ---
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        ngay_sql = date_obj.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        print(f"Lỗi: Định dạng ngày không hợp lệ: {date_str}")
        return None

    ma_buoi_hoc = None
    try:
        cursor = conn.cursor()
        # --- Bước 3: Truy vấn với các thành phần đã phân tích ---
        query = """
            SELECT bh.MaBuoiHoc
            FROM buoihoc bh
            JOIN lophocphan lhp ON bh.MaLopHocPhan = lhp.MaLopHocPhan
            JOIN hocphan hp ON lhp.MaHocPhan = hp.MaHocPhan
            JOIN loaidiemdanh ldd ON bh.MaLoaiDiemDanh = ldd.MaLoaiDiemDanh
            WHERE lhp.MaBac = %s
              AND lhp.MaNienKhoa = %s
              AND lhp.MaNganh = %s
              AND lhp.STTLop = %s
              AND TRIM(hp.TenHocPhan) = TRIM(%s)
              AND bh.NgayHoc = %s
              AND TRIM(ldd.TenLoaiDiemDanh) = TRIM(%s)
            LIMIT 1;
        """
        # Các tham số truyền vào phải đúng thứ tự
        params = (ma_bac, ma_nien_khoa, ma_nganh, stt_lop, subject_name, ngay_sql, session_name)
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            ma_buoi_hoc = result[0]

    except mysql.connector.Error as err:
        print(f"Lỗi khi truy vấn MaBuoiHoc: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
    return ma_buoi_hoc

def get_total_students_by_class(class_name):
    conn = connect_db()
    if conn is None:
        return None

    # --- Bước 1: Phân tích chuỗi tên lớp (class_name) ---
    # Ví dụ: "DH21TINTT01"
    try:
        ma_bac = class_name[0:2]          # -> "DH"
        # MaNienKhoa trong CSDL là kiểu INT [cite: 182]
        ma_nien_khoa = int(class_name[2:4]) # -> 21 
        ma_nganh = class_name[4:-2]       # -> "TINTT"
        stt_lop = class_name[-2:]         # -> "01"
    except (IndexError, ValueError) as e:
        # Xử lý nếu chuỗi class_name không đúng định dạng
        print(f"Lỗi nghiêm trọng: Định dạng tên lớp '{class_name}' không hợp lệ. Không thể phân tích. Lỗi: {e}")
        return None
    
    tong_sv = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT count(*) as TongSV
            FROM sinhvien
            WHERE MaBac = %s
                    AND MaNienKhoa = %s
                    AND MaNganh = %s
                    AND STTLop = %s
        """
        # Các tham số truyền vào phải đúng thứ tự
        params = (ma_bac, ma_nien_khoa, ma_nganh, stt_lop)
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            tong_sv = result[0]

    except mysql.connector.Error as err:
        print(f"Lỗi khi truy vấn MaBuoiHoc: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return tong_sv

def get_attendace_success(MaSV, MaBuoiHoc):
    conn = connect_db()
    if conn is None:
        return None

    attendance_status = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT 
                sv.HoTenSV,
                ddsv.ThoiGianGhiNhan,
                dlkm.AnhDaiDien
            FROM 
                sinhvien sv 
            JOIN diemdanhsv ddsv on sv.MaSV = ddsv.MaSV
            JOIN dulieukhuonmat dlkm on dlkm.MaSV = sv.MaSV
            WHERE
                    sv.MaSV = %s
                AND ddsv.MaBuoiHoc = %s

        """
        cursor.execute(query, (MaSV, MaBuoiHoc))
        result = cursor.fetchone()

        if result:
            attendance_status = result[0] , result[1], result[2]

    except mysql.connector.Error as err:
        print(f"Lỗi khi truy vấn trạng thái điểm danh: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return attendance_status