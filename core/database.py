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
import mysql.connector
from core.utils import *
from PIL import Image
from datetime import datetime, timedelta
import io
import pickle
import numpy as np

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
    
def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT TenDangNhap, MatKhau, VaiTro FROM taikhoan WHERE TenDangNhap = %s", (username,))
    result = cursor.fetchone()

    if not result:
        return False

    user_id, bcrypt_password, role = result

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
    cursor.execute("SELECT * FROM View_LichPhanCong WHERE TenDangNhap = %s;", (tendangnhap, ))
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

def record_attendance(ma_sv, ma_lop_hoc_phan, ngay_hoc, ma_loai_diem_danh, trang_thai="Có mặt"):
    """
    Ghi nhận điểm danh vào bảng diemdanh.
    Lưu ý: Bảng 'diemdanh' của bạn trong 333.sql không có cột MaLoaiDiemDanh và NgayHoc trực tiếp.
    Thay vào đó, nó liên kết với MaBuoiHoc.
    Chúng ta cần tìm MaBuoiHoc tương ứng.
    """
    conn = connect_db()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        # 1. Tìm MaBuoiHoc dựa trên MaLopHocPhan, NgayHoc và MaLoaiDiemDanh
        # Cần chuyển đổi ngay_hoc từ chuỗi "%d/%m/%Y" sang date object cho SQL
        try:
            ngay_hoc_obj = datetime.strptime(ngay_hoc, '%d/%m/%Y').date()
        except ValueError:
            print(f"record_attendance: Lỗi định dạng ngày {ngay_hoc}. Cần định dạng dd/mm/YYYY.")
            return False

        query_ma_buoi_hoc = """
            SELECT MaBuoiHoc 
            FROM buoihoc 
            WHERE MaLopHocPhan = %s AND NgayHoc = %s AND MaLoaiDiemDanh = %s
            LIMIT 1
        """
        cursor.execute(query_ma_buoi_hoc, (ma_lop_hoc_phan, ngay_hoc_obj, ma_loai_diem_danh))
        result_buoi_hoc = cursor.fetchone()

        if not result_buoi_hoc:
            print(f"Không tìm thấy buổi học cho lớp {ma_lop_hoc_phan}, ngày {ngay_hoc}, buổi {ma_loai_diem_danh}")
            return False
        
        ma_buoi_hoc = result_buoi_hoc[0]

        # 2. Lấy MaTrangThai từ TenTrangThai
        query_ma_trang_thai = "SELECT MaTrangThai FROM trangthaidiemdanh WHERE TenTrangThai = %s"
        cursor.execute(query_ma_trang_thai, (trang_thai,))
        result_trang_thai = cursor.fetchone()
        
        if not result_trang_thai:
            print(f"Không tìm thấy trạng thái điểm danh '{trang_thai}'.")
            return False
        
        ma_trang_thai = result_trang_thai[0]

        # 3. Kiểm tra xem sinh viên đã điểm danh cho buổi học này chưa
        check_query = """
            SELECT COUNT(*) FROM diemdanhsv
            WHERE MaSV = %s AND MaBuoiHoc = %s
        """
        cursor.execute(check_query, (ma_sv, ma_buoi_hoc))
        if cursor.fetchone()[0] > 0:
            print(f"MaSV {ma_sv} đã điểm danh cho buổi học {ma_buoi_hoc} này rồi.")
            return False # Không điểm danh lại

        # 4. Ghi nhận điểm danh
        insert_query = """
            INSERT INTO diemdanhsv (MaBuoiHoc, MaSV, MaTrangThai, ThoiGianGhiNhan)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (ma_buoi_hoc, ma_sv, ma_trang_thai))
        conn.commit()
        print(f"MaSV {ma_sv} đã điểm danh thành công cho buổi học {ma_buoi_hoc}.")
        return True
    except mysql.connector.Error as err:
        print(f"Lỗi khi ghi nhận điểm danh cho MaSV {ma_sv}: {err}")
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