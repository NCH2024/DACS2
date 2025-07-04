import customtkinter as ctk
from gui.utils import *

class LecturerAttendance(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self._border_width = 1
        self._border_color = "white"
        self._fg_color = "white"

        # Biến màu sắc
        self.widget_color = "#2DFCB0"
        self.txt_color_title = "#0412A9"

        # Tiêu đề
        self.title_widget = ctk.CTkLabel(
            self,
            text="Dashboard > ĐIỂM DANH SINH VIÊN",
            font=("Bahnschrift", 20, "bold"),
            text_color="#05243F"
        )
        self.title_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

        # === MENU TRÁI ===
        self.widget_menu = ctk.CTkFrame(self, fg_color="transparent", width=250)
        self.widget_menu.grid(row=1, column=0, rowspan=2, pady=5, padx=5, sticky="nsw")
        self.widget_menu.grid_rowconfigure((0, 1, 2), weight=1)
        self.widget_menu.grid_columnconfigure(0, weight=1)
        self.widget_menu.grid_propagate(False)

        # --- Menu nâng cao ---
        self.widget_menu_advanced = ctk.CTkFrame(self.widget_menu, fg_color=self.widget_color)
        self.widget_menu_advanced.grid(row=0, column=0, padx=0, pady=5, sticky="nsew")
        self.widget_menu_advanced.grid_propagate(False)
        #self.widget_menu_advanced.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.widget_menu_advanced.grid_columnconfigure(0, weight=1)

        self.title_wm_advanced = LabelCustom(self.widget_menu_advanced, "CHỨC NĂNG NÂNG CAO", font_size=12, font_weight="bold", text_color=self.txt_color_title)
        self.title_wm_advanced.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nw")

        self.widget_menu_advanced_btn_historyAttendance = ButtonTheme(self.widget_menu_advanced, "Xem lịch sử điểm danh")
        self.widget_menu_advanced_btn_historyAttendance.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.widget_menu_advanced_btn_searchStudent = ButtonTheme(self.widget_menu_advanced, "Tra cứu sinh viên")
        self.widget_menu_advanced_btn_searchStudent.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.widget_menu_advanced_btn_settingDetect = ButtonTheme(self.widget_menu_advanced, "Cài đặt nhận dạng")
        self.widget_menu_advanced_btn_settingDetect.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        # --- Menu sinh trắc học ---
        self.widget_menu_face = ctk.CTkFrame(self.widget_menu, fg_color=self.widget_color)
        self.widget_menu_face.grid(row=1, column=0, padx=0, pady=5, sticky="nsew")
        self.widget_menu_face.grid_columnconfigure(0, weight=1)
        self.widget_menu_face.grid_propagate(False)

        self.title_wm_face = LabelCustom(self.widget_menu_face, "CẬP NHẬT SINH TRẮC HỌC", font_size=12, font_weight="bold", text_color=self.txt_color_title)
        self.title_wm_face.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nw")
        
        self.widget_menu_face_trainFace = ButtonTheme(self.widget_menu_face, "Đào tạo dữ liệu khuôn mặt")
        self.widget_menu_face_trainFace.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.widget_menu_face_seenDataFace = ButtonTheme(self.widget_menu_face, "Xem dữ liệu khuôn mặt")
        self.widget_menu_face_seenDataFace .grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        # --- Menu thiết bị ---
        self.widget_menu_devices = ctk.CTkFrame(self.widget_menu, fg_color=self.widget_color)
        self.widget_menu_devices.grid(row=2, column=0, padx=0, pady=5, sticky="nsew")
        self.widget_menu_devices.grid_columnconfigure(0, weight=1)
        self.widget_menu_devices.grid_propagate(False)

        self.title_wm_devives = LabelCustom(self.widget_menu_devices, "THIẾT BỊ", font_size=12, font_weight="bold", text_color=self.txt_color_title)
        self.title_wm_devives.grid(row=0, column=0, padx=10, pady=0, sticky="nw")
        
        self.widget_menu_devices_cbx_camera = ComboboxTheme(self.widget_menu_devices, values=["ADM camera", "Canon a342 1600xz"])
        self.widget_menu_devices_cbx_camera.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        self.widget_menu_devices_testCamera = ButtonTheme(self.widget_menu_devices, "Test Camera", width=80, fg_color="#0099FF", hover_color="#003462")
        self.widget_menu_devices_testCamera .grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ne")

        # === KHUNG PHẢI - THÔNG TIN ĐIỂM DANH ===
        self.widget_attendance_options = ctk.CTkFrame(self, fg_color=self.widget_color, height=100)
        self.widget_attendance_options.grid(row=1, column=1, pady=5, padx=5, sticky="nsew")
        self.widget_attendance_options.grid_columnconfigure(0, weight=1)
        self.widget_attendance_options.grid_propagate(False)

        self.widget_attendance_options_title = LabelCustom(self.widget_attendance_options, "THÔNG TIN ĐIỂM DANH", font_size=12, font_weight="bold", text_color=self.txt_color_title)
        self.widget_attendance_options_title.grid(row=0, column=0, padx=10, pady=0, sticky="nw")

        # === KHUNG PHẢI - DANH SÁCH SINH VIÊN ===
        self.widget_list_attendance = ctk.CTkFrame(self, fg_color=self.widget_color)
        self.widget_list_attendance.grid(row=2, column=1, pady=5, padx=5, sticky="nsew")
        self.widget_list_attendance.grid_columnconfigure(0, weight=1)

        self.widget_list_attendance_title = LabelCustom(self.widget_list_attendance, "DANH SÁCH SINH VIÊN ĐIỂM DANH", font_size=12)
        self.widget_list_attendance_title.grid(row=0, column=0, padx=10, pady=0, sticky="nw")

        # === THIẾT LẬP LƯỚI TỔNG ===
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
