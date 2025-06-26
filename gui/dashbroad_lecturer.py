from gui.base_dashbroad import DashbroadView
from gui.utils import ImageSlideshow
import customtkinter as ctk
import tkinter as tk

class LecturerDashbroad(DashbroadView):
    """Tạo giao diện dashboard cho giảng viên."""
    def __init__(self, master, user, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master.title("Dashboard Giảng Viên")
        self.master.geometry("1060x640")
        self.user = user
        self.setup_ui(user)

    def ButtonTheme(self, master, text, font=("Bahnschrift", 18, "bold"), fg_color="#31FCA1", hover_color="#00C785", txt_color="#05243F", border_color="white", border_width=2, command=None, **kwargs):
        return super().ButtonTheme(
            master, text, font, fg_color, hover_color, border_color, border_width, command, text_color=txt_color, **kwargs
        )
    
    def setup_ui(self, user):
        """Thiết lập các thành phần giao diện."""
        self.say_hello = ctk.CTkLabel(self.sidebar, text=f"Xin chào\n{user}!", font=("Bahnschrift", 20, "normal"), justify="center", height=80, text_color="white")
        self.say_hello.pack(pady=30, padx=10, fill="x")
        # Thêm các nút hoặc thành phần khác vào sidebar
        self.home_btn = self.ButtonTheme(self.sidebar, "Trang chủ", height=50, command=self.show_home)
        self.home_btn.pack(pady=10, padx=30, fill="x")
        
        self.attendance_btn = self.ButtonTheme(self.sidebar, "Điểm danh", height=50)
        self.attendance_btn.pack(pady=10, padx=30, fill="x")
        
        self.schedule_btn = self.ButtonTheme(self.sidebar, "Lịch học", height=50)
        self.schedule_btn.pack(pady=10, padx=30, fill="x")
        
        self.report_btn = self.ButtonTheme(self.sidebar, "Báo cáo", height=50)
        self.report_btn.pack(pady=10, padx=30, fill="x")
        
        
        
        # Ban đầu hiển thị trang chủ
        self.show_home()
        

        
    def show_home(self):
        """Hiển thị trang chủ."""
        self.clear_content()
        
        slideshow = ImageSlideshow(self.content, image_folder="resources/slideshow", size=(1024, 768), delay=3000)
        slideshow.pack(pady=0)
        
        