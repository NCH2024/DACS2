from logging import root
from gui.base_view import BaseView
import customtkinter as ctk
from gui.utils import ImageProcessor
import tkinter as tk
import core.database 
from core.utils import bcrypt_password, check_password
from gui.dashbroad_lecturer import LecturerDashbroad

from core.app_config import load_config, save_config


class MainWindow(BaseView):
    def __init__(self, master, config):
        super().__init__(master)
        self.master.title("PHẦN MỀM ĐIỂM DANH")
        self.master.geometry(f"1280x720+0+0")
        self.AppConfig = config
        

        self.sidebar = ctk.CTkFrame(self, width=450, corner_radius=0, fg_color="#05243F")
        self.sidebar.pack(side="left", fill="y")
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="#05243F")
        self.content.pack(side="right", fill="both", expand=True)
        
        self.bg_ctkimage = ImageProcessor("resources/images/bg_main_window.png") \
                                .crop_to_aspect(1280, 720) \
                                .resize(1280, 720) \
                                .to_ctkimage(size=(1280,720))
        self.bg_label = ctk.CTkLabel(self.content, image=self.bg_ctkimage, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.setup_ui()
        
    def setup_ui(self):
        text_var_first = tk.StringVar(value="KHOA CÔNG NGHỆ THÔNG TIN\nTRƯỜNG ĐẠI HỌC NAM CẦN THƠ\n---------------\n\nĐỒ ÁN CƠ SỞ 2")
        self.tittle_first_label = self.LabelFont(self.sidebar, text=text_var_first,
                                                  font=("Bahnschrift", 20, "bold"),
                                                  justify="center", bg_color="transparent",
                                                  width=400, height=80, text_color="white")
        self.tittle_first_label.place(relx=0.5, rely=0.1, anchor="center")
        
        

        text_var = tk.StringVar(value="PHẦN MỀM ĐIỂM DANH")
        text_var2 = tk.StringVar(value="(Bằng công nghệ nhận dạng khuôn mặt)")
        self.title_label = self.LabelFont(self.sidebar, text=text_var, font=("Bahnschrift", 30, "bold"),
                                          justify="center", text_color="white", width=1280, height=50)
        self.title_label.place(relx=0.5, rely=0.35, anchor="center")
        
        self.tittle_label2 = self.LabelFont(self.sidebar, text=text_var2, font=("Bahnschrift", 13, "italic"), text_color="white")
        self.tittle_label2.place(relx=0.5, rely=0.4, anchor="center")

        
        
        self.username_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Tên đăng nhập", 
                                            width=200, height=40, font=("Bahnschrift", 16))
        self.username_entry.place(relx=0.5, rely=0.5, anchor="center")  
        self.password_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Mật khẩu", show="*", 
                                            width=200, height=40, font=("Bahnschrift", 16))
        self.password_entry.place(relx=0.5, rely=0.6, anchor="center")
        
        self.check_save_login = ctk.CTkCheckBox(self.sidebar, text="Lưu đăng nhập", text_color="white", command=self.on_check_save_login)
        self.check_save_login.place(relx=0.5, rely=0.67, anchor="center")

        self.login_button = self.ButtonTheme(self.sidebar, "Đăng nhập",width=200, height=50, command=lambda: self.on_login(self.username_entry.get(), self.password_entry.get()))
        self.login_button.place(relx=0.5, rely=0.75, anchor="center")

        text_var_second = tk.StringVar(value="Sinh viên: NGUYỄN CHÁNH HIỆP \n Mã số sinh viên: 223408 \n Lớp: 22TIN-TT \n\n Tháng 6/2025")
        self.tittle_second_label = self.LabelFont(self.sidebar, text=text_var_second,
                                                  font=("Bahnschrift", 15, "bold"),
                                                  justify="center", bg_color="transparent",
                                                  width=400, height=80, text_color="white")
        self.tittle_second_label.place(relx=0.5, rely=0.9, anchor="center")

    def on_login(self, username=None, password=None):
        """Xử lý sự kiện khi nút đăng nhập được nhấn."""
        
        # Kiểm tra đăng nhập
        result = core.database.login(username, password)

        if result is False:
            self.show_message("Thao tác không thành công!", "Sai mật khẩu hoặc tên tài khoản.\nVUI LÒNG THỬ LẠI!")
        else:
            user_id, role = result
            if role == "giangvien":
                lecturer = ctk.CTkToplevel(self.master)
                lecturer_dashbroad = LecturerDashbroad(lecturer, user_id, config=self.AppConfig)
                lecturer_dashbroad.pack(expand=True, fill="both")
                self.master.withdraw()
            else:
                self.show_message("Lỗi", "Đăng nhập thất bại.")
                
    def on_check_save_login(self):
        """Xử lý sự kiện khi checkbox lưu đăng nhập được thay đổi."""
        if self.check_save_login.get():
            username = self.username_entry.get()
            password = self.password_entry.get()
            if username and password:
                self.AppConfig.login_info.username = username
                self.AppConfig.login_info.password = password
                save_config(self.AppConfig)
                
        else:
            self.AppConfig.login_info.username = None
            self.AppConfig.login_info.password = None
            save_config(self.AppConfig)
            

        

def runapp(config):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    root.withdraw()

    app = MainWindow(master=root, config=config)
    username = config.login_info.username
    password = config.login_info.password

    def show_window():
        root.deiconify()
        root.lift()
        root.focus_force()
        root.attributes('-topmost', True)
        root.after(100, lambda: root.attributes('-topmost', False))

    root.after(200, show_window)

    # Đăng nhập tự động sau 100ms, khi GUI đã sẵn sàng
    if username and password:
        root.after(200, lambda: app.on_login(username, password))

    root.mainloop()
