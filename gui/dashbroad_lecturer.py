from gui.base_dashbroad import DashbroadView
from gui.utils import ImageSlideshow
from gui.lecturer_home import LecturerHome
from gui.lecturer_attendance import LecturerAttendance
from gui.lecturer_schedule import LecturerSchedule
from gui.lecturer_settings import LecturerSettings
import customtkinter as ctk
import core.database as Db  

class LecturerDashbroad(DashbroadView):
    """Tạo giao diện dashboard cho giảng viên."""
    def __init__(self, master, user, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.user = user
        self.master.title("Dashboard Giảng Viên")
        self.master.geometry("1060x640")
        self.nameLecturer = Db.get_username(self.user)
        self.setup_ui_sidebar(self.nameLecturer)

    def ButtonTheme(self, master, text, font=("Bahnschrift", 18, "bold"), fg_color="#31FCA1", hover_color="#00C785", txt_color="#05243F", border_color="white", border_width=2, command=None, **kwargs):
        return super().ButtonTheme(
            master, text, font, fg_color, hover_color, border_color, border_width, command, text_color=txt_color, **kwargs
        )
    
    def setup_ui_sidebar(self, user):
        """Thiết lập các thành phần giao diện."""
        self.infor_app = ctk.CTkLabel(self.sidebar, text="GitHub dự án:@NCH2024\nỨng dụng điểm danh bằng nhận diện khuôn mặt\nĐồ án sinh viên thực hiện.", font=("Bahnschrift", 10, "normal"), justify="center", height=80, text_color="white")
        self.infor_app.pack(pady=5, padx=5, fill="x")
        
        self.say_hello = ctk.CTkLabel(self.sidebar, text=f"Xin chào\n{user}!", font=("Bahnschrift", 18, "bold"), justify="left", height=80, text_color="white")
        self.say_hello.pack(pady=20, padx=10, fill="x")
        # Thêm các nút hoặc thành phần khác vào sidebar
        self.home_btn = self.ButtonTheme(self.sidebar, "Trang chủ", height=50, command=lambda: self.show_home(self.user))
        self.home_btn.pack(pady=10, padx=30, fill="x")
        
        self.attendance_btn = self.ButtonTheme(self.sidebar, "Điểm danh", height=50, command=lambda: self.show_attendance(self.user))
        self.attendance_btn.pack(pady=10, padx=30, fill="x")
        
        self.schedule_btn = self.ButtonTheme(self.sidebar, "Lịch điểm danh", height=50, command=lambda: self.show_schedule(self.user))
        self.schedule_btn.pack(pady=10, padx=30, fill="x")
        
        self.report_btn = self.ButtonTheme(self.sidebar, "Thống kê", height=50)
        self.report_btn.pack(pady=10, padx=30, fill="x")
        
        self.setting_btn = self.ButtonTheme(self.sidebar, "Cài đặt", height=50, command=lambda: self.show_settings(self.user))
        self.setting_btn.pack(pady=10, padx=30, fill="x")
        
        slideshow = ImageSlideshow(self.content, image_folder="resources/slideshow", size=(1024, 768), delay=3000)
        slideshow.pack(pady=0)
        

        
    def show_home(self, user):
        self.clear_content()
        content = LecturerHome(master=self.content, username=user)
        content.pack(fill="both", expand=True, padx=0, pady=0)
        self.current_page = "home"
        self.update_button_highlight()

    def show_attendance(self, user):
        self.clear_content()
        content = LecturerAttendance(master=self.content, username=user)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_page = "attendance"
        self.update_button_highlight()

    def show_schedule(self, username):
        self.clear_content()
        content = LecturerSchedule(master=self.content, lecturer_username=username)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_page = "schedule"
        self.update_button_highlight()
        
    def show_settings(self, user):
        self.clear_content()
        content = LecturerSettings(master=self.content, user=user)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_page = "Settings"
        self.update_button_highlight()
        
        
    def update_button_highlight(self):
        # Reset màu tất cả nút
        normal_color = "#31FCA1"
        hover_color = "#00C785"
        active_color = "#0E8EE9"  # Màu khi được chọn

        self.home_btn.configure(fg_color=normal_color, hover_color=hover_color)
        self.attendance_btn.configure(fg_color=normal_color, hover_color=hover_color)
        self.schedule_btn.configure(fg_color=normal_color, hover_color=hover_color)
        self.setting_btn.configure(fg_color=normal_color, hover_color=hover_color)

        # Tô đậm nút đang được chọn
        if self.current_page == "home":
            self.home_btn.configure(fg_color=active_color)
        elif self.current_page == "attendance":
            self.attendance_btn.configure(fg_color=active_color)
        elif self.current_page == "schedule":
            self.schedule_btn.configure(fg_color=active_color)
        elif self.current_page == "Settings":
            self.setting_btn.configure(fg_color=active_color)

