'''
FILE NAME: core/models.py
CODE BY: Nguyễn Chánh Hiệp 
DATE: 17/06/2025
DESCRIPTION:
        + Đây là file chứa các model của ứng dụng 
        + Định nghĩa các đôi tượng
        + Các model sẽ được sử dụng để lưu trữ dữ liệu và tương tác với cơ sở dữ liệu
VERSION: 1.0.0
'''
from datetime import datetime

class User:
    '''
    Mô hình người dùng/Người quản trị hệ thống
    Attributes:
        - username: Tên đăng nhập của người dùng
        - password: Mật khẩu của người dùng
        - role: Vai trò của người dùng (ví dụ: admin, user)
        - email: Địa chỉ email của người dùng
    Methods:
        - to_dict: Chuyển đổi đối tượng thành từ điển
    '''
    def __init__(self, username, password, role, email=None):
        self.username = username
        self.password = password
        self.role = role
        self.email = email
        
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'email': self.email
        }
        
    class Attendance:
        '''
        Mô hình điểm danh
        Attributes:
            - user_id: Đối tượng người dùng liên kết với điểm danh
            - timestamp: lưu dấu thời gian điểm danh
            - status: Trạng thái điểm danh (ví dụ: có mặt, vắng mặt, có phép, chưa xác định)
            - class_id: ID của lớp học liên kết với điểm danh
        Methods:
            - to_dict: Chuyển đổi đối tượng thành từ điển
        '''
        def __init__(self, user_id, timestamp=None, status="Chưa xác định", class_id=None):
            self.user_id = user_id
            self.timestamp = timestamp or datetime.now()
            self.status = status
            self.class_id = class_id

        def to_dict(self):
            return {
                'user_id': self.user_id,
                'timestamp': self.timestamp,
                'status': self.status,
                'class_id': self.class_id
            }
    
    class Schedule:
        '''
        Mô hình thời khóa biểu
        Attributes:
            - class_id: ID của lớp học liên kết với thời khóa biểu
            - start_time: Thời gian bắt đầu của lớp học
            - end_time: Thời gian kết thúc của lớp học
            - subject: Môn học của lớp học
        Methods:
            - to_dict: Chuyển đổi đối tượng thành từ điển
        '''
        def __init__(self, class_id, start_time, end_time, subject=None):
            self.class_id = class_id
            self.start_time = start_time
            self.end_time = end_time
            self.subject = subject

        def to_dict(self):
            return {
                'class_id': self.class_id,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'subject': self.subject,
            }
