'''
FILE NAME: core/utils.py
CODE BY: Nguyễn Chánh Hiệp 
DATE: 17/06/2025
DESCRIPTION:
        + Đây là file chứa các hàm tiện ích cho ứng dụng
        + Định nghĩa các hàm xử lý dữ liệu
        + Các hàm này sẽ được sử dụng để hỗ trợ cho các model và controller
VERSION: 1.0.0
'''
import re
from datetime import datetime
import bcrypt

def bcrypt_password(password: str) -> str:
    """Mã hóa password bằng bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    b = bcrypt.hashpw(password.encode(), salt) 
    return b.decode()  # Trả về chuỗi để lưu trong DB

def check_password(plain_password: str, bcrypt_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), bcrypt_password.encode())


def format_time(dt):
    """Định dạng thời gian sang chuỗi 'YYYY-MM-DD HH:MM'."""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.strftime("%Y-%m-%d %H:%M")

def validate_email(email):
    """Kiểm tra định dạng email đúng chuẩn."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def convert_to_mysql_date(date_str):
    """Chuyển từ 'DD/MM/YYYY' sang 'YYYY-MM-DD'."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None