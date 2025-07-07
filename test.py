import customtkinter as ctk
from gui.lecturer_attendance_setting import *
from gui.lecturer_attendance_searchStudent import *

def run_setting_window():


    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.withdraw()  # ẩn gốc

    LecturerAttendance_Setting.show_window(parent=root)

    root.mainloop()

if __name__ == "__main__":
    run_setting_window()
