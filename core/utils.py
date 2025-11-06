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
from datetime import datetime
import bcrypt
import pygame
import os
import sys


def bcrypt_password(password: str) -> str:
    """Mã hóa password bằng bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    b = bcrypt.hashpw(password.encode(), salt) 
    return b.decode()  # Trả về chuỗi để lưu trong DB

def check_password(plain_password: str, bcrypt_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), bcrypt_password.encode())

def get_base_path():
    """ Lấy đường dẫn gốc của ứng dụng, hoạt động cho cả script và file .exe đã đóng gói. """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Chạy từ file .exe (PyInstaller)
        return sys._MEIPASS
    else:
        # Chạy từ script .py
        return os.path.abspath(os.path.dirname(__file__))

def convert_to_mysql_date(date_str):
    """Chuyển từ 'DD/MM/YYYY' sang 'YYYY-MM-DD'."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None