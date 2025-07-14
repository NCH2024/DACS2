import customtkinter as ctk
from gui.utils import *
from tkinter import messagebox

class LecturerAccount_Setting(ctk.CTkFrame):
    def __init__(self, master=None, user=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        
        self.user = user

        # Tiêu đề
        self.title = ctk.CTkLabel(self, text="Dashboard > Cài đặt Tài khoản", font=("Bahnschrift", 14, "bold"))
        self.title.grid(row=0, column=0, columnspan=3, padx=15, pady=(20, 5), sticky="w")

        # Phân nhóm
        # Nhóm thông tin chung
        self.name_setting = ctk.CTkLabel(self, text="THIẾT LẬP CHUNG", font=("Bahnschrift", 12), text_color="#0044FF")
        self.name_setting.grid(row=1, column=0, padx=5, pady=(5, 15), sticky="nw")
        
        self.user_info = ctk.CTkFrame(self, fg_color="white")
        self.user_info.grid(row=2, column=0,padx=20, columnspan=3, sticky="news")
        
        self.user_info_name = LabelCustom(self.user_info, "Username:", value=self.user)
        
        # Các tuỳ chọn bật/tắt
        self.switch_realtime = SwitchOption(self, "Lưu đăng nhập cho lần kế tiếp", initial=False, command=self.on_check)
        self.switch_realtime.grid(row=3, column=0,padx=10, columnspan=3, pady=5, sticky="ew")
        
        # Nhóm cài đặt mật khẩu
        self.password_setting = ctk.CTkLabel(self, text="THIẾT LẬP MẬT KHẨU", font=("Bahnschrift", 12), text_color="#0044FF")
        self.password_setting.grid(row=4, column=0, padx=5, pady=(5, 15), sticky="nw")
        
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Nhập mật khẩu mới", show="*", 
                                            width=200, height=40, font=("Bahnschrift", 16))
        self.password_entry.grid(row=5, column=0,padx=20, sticky="we")
        
        self.password_entry_again = ctk.CTkEntry(self, placeholder_text="Nhập lại mật khẩu mới", show="*", 
                                            width=200, height=40, font=("Bahnschrift", 16))
        self.password_entry_again.grid(row=6, column=0,padx=20, pady=(20,0), sticky="we")




        self.save_btn = ButtonTheme(self, text="LƯU THAY ĐỔI", fg_color="#3389F1", width=100)
        self.save_btn.grid(row=7, column=0, pady=(20,0), sticky="se")
        
        
        # Hàm chức năng nút

    def on_check(self, is_checked=bool):
        if is_checked:
            messagebox.showinfo("Thông báo", "Đã lưu thông tin đăng nhập thành công!")
        else:
            messagebox.showinfo("Thông báo", "Không lưu đăng nhập cho lần tới!")

        
        



