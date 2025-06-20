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
import hashlib
import re
from datetime import datetime

def hash_password(password):
    """Mã hóa password."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    """Kiểm tra password với hash."""
    return hash_password(password) == hashed

def format_time(dt):
    """Định dạng thời gian sang chuỗi 'YYYY-MM-DD HH:MM'."""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.strftime("%Y-%m-%d %H:%M")

def validate_email(email):
    """Kiểm tra định dạng email đúng chuẩn."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None