from gui.base_view import BaseView
import customtkinter as ctk
from gui.utils import ImageProcessor
import tkinter as tk
import core.database 
from gui.dashbroad_lecturer import LecturerDashbroad

class MainWindow(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("PHẦN MỀM ĐIỂM DANH")
        self.master.geometry(f"1280x720+0+0")
        
        
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
        
        self.login_button = self.ButtonTheme(self.sidebar, "Đăng nhập",width=200, height=50, command=self.on_login)
        self.login_button.place(relx=0.5, rely=0.7, anchor="center")

        text_var_second = tk.StringVar(value="Sinh viên: NGUYỄN CHÁNH HIỆP \n Mã số sinh viên: 223408 \n Lớp: 22TIN-TT \n\n Tháng 6/2025")
        self.tittle_second_label = self.LabelFont(self.sidebar, text=text_var_second,
                                                  font=("Bahnschrift", 16, "bold"),
                                                  justify="center", bg_color="transparent",
                                                  width=400, height=80, text_color="white")
        self.tittle_second_label.place(relx=0.5, rely=0.9, anchor="center")

    
    def on_login(self):
        """Xử lý sự kiện khi nút đăng nhập được nhấn."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Kiểm tra đăng nhập
        if not username or not password:
            self.show_message("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        if core.database.login(username, password)==False:
            self.show_message("Thao tác không thành công!", "Sai mật khẩu hoặc tên tài khoản.\nVUI LÒNG THỬ LẠI!")
            return
        else:
            user_id, role = core.database.login(username, password)
    
            if role == "user":
                """Xử lý đăng nhập thành công."""
                lecturer = ctk.CTkToplevel(self.master)
                lecturer_dashbroad = LecturerDashbroad(lecturer, user_id)
                lecturer_dashbroad.pack(expand=True, fill="both")
                self.master.withdraw()  
            else:
                self.show_message("Lỗi", "Đăng nhập thất bại.")
        

def runapp():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    app = MainWindow(master=root)
    root.mainloop()