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
from core.utils import check_password 
from PIL import Image
from datetime import datetime, timedelta
import io

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


   
  