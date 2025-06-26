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
from core import utils

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
    """
    Hàm đăng nhập người dùng.
    Nhận vào tên người dùng và mật khẩu, trả về chuỗi role nếu đăng nhập thành công, ngược lại False.
    """
    # Mã hóa mật khẩu
    #password = utils.hash_password(password)

    conn = connect_db()
    if conn is None:
        return False

    cursor = conn.cursor()
    query = "SELECT user_id, role FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        user_id = result[0]
        role = result[1]
        return user_id, role
    else:
        return False

def get_username(user_id):
    pass


if __name__ == "__main__":
        try:
            # Test the database connection
            conn = connect_db() 
            print("Ket noi CSDL thanh cong")
        except Exception as e:
            print(f"Error connecting to the database: {e}")