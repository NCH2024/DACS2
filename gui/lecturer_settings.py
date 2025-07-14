import customtkinter as ctk
from gui.utils import *
from gui.lecturer_attendance_setting import LecturerAttendance_Setting
from gui.lecturer_account_settings import LecturerAccount_Setting


class LecturerSettings(ctk.CTkFrame):
    def __init__(self, master=None, user=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.user = user
        
        self._border_width = 1
        self._border_color = "white"
        self._fg_color = "white"
        
        # Bién màu sắc
        self.widget_color = "#2DFCB0"

        # Cấu hình grid tổng thể
        self.grid_rowconfigure((0,1,2), weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        
        # Khung cài đặt dành cho phần mềm
        self.widget_settings_attendace = ctk.CTkFrame(self, fg_color="white", border_color=self.widget_color, border_width=2)
        self.widget_settings_attendace.grid(row=1, column=0, padx=5, pady=5, sticky="news")
        self.widget_settings_attendace.grid_columnconfigure(0,weight=1)
        self.widget_settings_attendace.grid_rowconfigure(0,weight=1)
        
        self.widget_settings_attendace_content = LecturerAttendance_Setting(master=self.widget_settings_attendace)
        self.widget_settings_attendace_content.grid(row=0, column=0, sticky="news")
        
        
        
        # Khung cài đặt dành cho tài khoản user
        self.widget_settings_account = ctk.CTkFrame(self, fg_color=self.widget_color)
        self.widget_settings_account.grid(row=1, column=1, padx=5, pady=5, sticky="news")
        
        self.widget_settings_account_content = LecturerAccount_Setting(master=self.widget_settings_account, user=self.user)
        self.widget_settings_account_content.grid(row=0, column=0, sticky="news")
        
        