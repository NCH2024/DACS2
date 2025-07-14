# FILE NAME: 

import customtkinter as ctk
from tkinter import messagebox

import core.database as Db
from gui.utils import *

from gui.lecturer_attendance_searchStudent import * 
from gui.lecturer_attendance_setting import * 
from app_face_recognition.widget_trainning_face import *

class LecturerAttendance(ctk.CTkFrame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)
        self.username = username
        self._border_width = 1
        self._border_color = "white"
        self._fg_color = "white"

        # Biến màu sắc
        self.widget_color = "#2DFCB0"
        self.txt_color_title = "#0412A9"

        # Khởi tạo các đối tượng xử lý
        self.attendance_processor = None
        self.camera_window = None # Biến để lưu trữ cửa sổ camera Toplevel

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
        self.widget_menu.grid(row=1, column=0, rowspan=2, pady=0, padx=0, sticky="nsw")
        self.widget_menu.grid_rowconfigure((0, 1, 2), weight=1)
        self.widget_menu.grid_columnconfigure(0, weight=1)
        self.widget_menu.grid_propagate(False)

        # --- Menu nâng cao ---
        self.widget_menu_advanced = ctk.CTkFrame(self.widget_menu, fg_color=self.widget_color)
        self.widget_menu_advanced.grid(row=0, column=0, padx=0, pady=5, sticky="nsew")
        self.widget_menu_advanced.grid_propagate(False)
        self.widget_menu_advanced.grid_columnconfigure(0, weight=1)

        self.title_wm_advanced = LabelCustom(self.widget_menu_advanced, "CHỨC NĂNG NÂNG CAO", font_size=12, font_weight="bold", text_color=self.txt_color_title)
        self.title_wm_advanced.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nw")

        self.widget_menu_advanced_btn_historyAttendance = ButtonTheme(self.widget_menu_advanced, "Xem lịch sử điểm danh")
        self.widget_menu_advanced_btn_historyAttendance.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.widget_menu_advanced_btn_searchStudent = ButtonTheme(self.widget_menu_advanced, "Tra cứu sinh viên", command=self.show_searchStudent)
        self.widget_menu_advanced_btn_searchStudent.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")


        # --- Menu sinh trắc học ---
        self.widget_menu_face = ctk.CTkFrame(self.widget_menu, fg_color=self.widget_color)
        self.widget_menu_face.grid(row=1, column=0, padx=0, pady=(0,5), sticky="nsew")
        self.widget_menu_face.grid_columnconfigure(0, weight=1)
        self.widget_menu_face.grid_propagate(False)

        self.title_wm_face = LabelCustom(self.widget_menu_face, "CẬP NHẬT SINH TRẮC HỌC", font_size=12, font_weight="bold", text_color=self.txt_color_title)
        self.title_wm_face.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nw")

        self.widget_menu_face_trainFace = ButtonTheme(self.widget_menu_face, "Đào tạo dữ liệu khuôn mặt", command=self.show_tranning_face)
        self.widget_menu_face_trainFace.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.widget_menu_face_seenDataFace = ButtonTheme(self.widget_menu_face, "Xem dữ liệu khuôn mặt")
        self.widget_menu_face_seenDataFace.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        # --- Menu thiết bị ---
        self.widget_menu_devices = ctk.CTkFrame(self.widget_menu, fg_color=self.widget_color)
        self.widget_menu_devices.grid(row=2, column=0, padx=0, pady=(0,5), sticky="nsew")
        self.widget_menu_devices.grid_columnconfigure(0, weight=1)
        self.widget_menu_devices.grid_propagate(False)

        self.title_wm_devives = LabelCustom(self.widget_menu_devices, "THIẾT BỊ", font_size=12, font_weight="bold", text_color=self.txt_color_title)
        self.title_wm_devives.grid(row=0, column=0, padx=10, pady=0, sticky="nw")

        self.widget_menu_devices_cbx_camera = ComboboxTheme(self.widget_menu_devices, values=["ADM camera", "Canon a342 1600xz"])
        self.widget_menu_devices_cbx_camera.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # THAY ĐỔI: Gán command cho nút Test Camera
        self.widget_menu_devices_testCamera = ButtonTheme(self.widget_menu_devices, "Test Camera", width=80, fg_color="#0099FF", hover_color="#003462")
        self.widget_menu_devices_testCamera.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ne")

        # === KHUNG PHẢI - THÔNG TIN ĐIỂM DANH ===
        self.widget_attendance_options = ctk.CTkFrame(self, fg_color="transparent", height=120)
        self.widget_attendance_options.grid(row=1, column=1, pady=0, padx=0, sticky="nsew")
        self.widget_attendance_options.grid_columnconfigure((0,1), weight=1)
        self.widget_attendance_options.grid_rowconfigure(0, weight=1)
        self.widget_attendance_options.grid_propagate(False)

        # --- Menu chọn thông tin ----
        self.widget_attendance_options_left = ctk.CTkFrame(
            self.widget_attendance_options,
            fg_color=self.widget_color,
            width=500,
            height=140  # tăng chiều cao nhẹ
        )
        self.widget_attendance_options_left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.widget_attendance_options_left.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.widget_attendance_options_left.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.widget_attendance_options_left.grid_propagate(False)

        # Tiêu đề
        self.widget_attendance_options_left_title = LabelCustom(
            self.widget_attendance_options_left,
            "THÔNG TIN ĐIỂM DANH",
            font_size=12,
            font_weight="bold",
            text_color=self.txt_color_title
        )
        self.widget_attendance_options_left_title.grid(row=0, column=0, columnspan=4, padx=10, pady=0, sticky="nw")

        # Tạo combobox LỚP
        self.widget_attendance_options_left_cbxClass = ComboboxTheme(
            self.widget_attendance_options_left, values=["Đang tải..."], state="readonly"
        )
        self.widget_attendance_options_left_cbxClass.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.widget_attendance_options_left_cbxClass.configure(command=self.on_class_selected)

        # Tạo combobox HỌC PHẦN
        self.widget_attendance_options_left_cbxSubject = ComboboxTheme(
            self.widget_attendance_options_left, values=["Đang tải..."], state="disabled"
        )
        self.widget_attendance_options_left_cbxSubject.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")
        self.widget_attendance_options_left_cbxSubject.configure(command=self.on_subject_selected)

        # Tạo combobox NGÀY
        self.widget_attendance_options_left_cbxDate = ComboboxTheme(
            self.widget_attendance_options_left, values=["Đang tải..."], state="disabled"
        )
        self.widget_attendance_options_left_cbxDate.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.widget_attendance_options_left_cbxDate.configure(command=self.on_date_selected)

        # Tạo combobox BUỔI
        self.widget_attendance_options_left_cbxSession = ComboboxTheme(
            self.widget_attendance_options_left, values=["Đang tải..."], state="disabled"
        )
        self.widget_attendance_options_left_cbxSession.grid(row=2, column=1, padx=5, pady=(0, 5), sticky="ew")


        # Label ghi chú
        self.widget_attendance_options_left_note = ctk.CTkLabel(
            self.widget_attendance_options_left,
            text="*Click vào nút trên để kiểm tra/Xem thông tin đã chọn",
            font=("Bahnschrift", 10),
            text_color="black",
            wraplength=200,
            justify="center"
        )
        self.widget_attendance_options_left_note.grid(row=2, column=2, columnspan=2, padx=5, pady=(0, 0), sticky="ew")

        # Nút Xem Danh sách
        self.widget_attendance_options_left_btnSeen = ButtonTheme(
            self.widget_attendance_options_left,
            text="Xem Danh sách",
            fg_color="#0099FF",
            hover_color="#003462",
            width=80,
            height=40, 
            command=self.show_attendance_list
        )
        self.widget_attendance_options_left_btnSeen.grid(row=1, column=2, columnspan=2, padx=30, pady=5, sticky="n")


        # --- Menu điểm danh ---
        self.widget_attendance_options_right = ctk.CTkFrame(self.widget_attendance_options, fg_color=self.widget_color, height=120)
        self.widget_attendance_options_right.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        self.widget_attendance_options_right.grid_columnconfigure((0,1), weight=1)
        self.widget_attendance_options_right.grid_propagate(False)

        self.widget_attendance_options_right_title = LabelCustom(self.widget_attendance_options_right, "ĐIỂM DANH", font_size=12, font_weight="bold", text_color=self.txt_color_title)
        self.widget_attendance_options_right_title.grid(row=0, column=0, columnspan=2, padx=10, pady=0, sticky="nw")

        self.attendance_mode_var = ctk.StringVar(value="single")
        self.radio_single = ctk.CTkRadioButton(self.widget_attendance_options_right, text="Điểm danh từng SV", variable=self.attendance_mode_var, value="single")
        self.radio_single.grid(row=1, column=0, padx=20, pady=(5, 2), sticky="w")

        self.radio_all = ctk.CTkRadioButton(self.widget_attendance_options_right, text="Điểm danh cả lớp", variable=self.attendance_mode_var, value="all")
        self.radio_all.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="w")

        # THAY ĐỔI: Gán command cho nút Điểm danh
        self.btn_attendance = ButtonTheme(self.widget_attendance_options_right, text="Điểm danh", fg_color="#0099FF", hover_color="#003462", width=120)
        self.btn_attendance.grid(row=1, column=1, rowspan=3, padx=10, pady=5, sticky="e")

        # === KHUNG PHẢI - DANH SÁCH SINH VIÊN ===
        self.widget_list_attendance = ctk.CTkFrame(self, fg_color="white", border_color=self.widget_color, border_width=2)
        self.widget_list_attendance.grid(row=2, column=1, pady=(0,5), padx=5, sticky="nsew")
        self.widget_list_attendance.grid_columnconfigure((0,1), weight=1)
        self.widget_list_attendance.grid_rowconfigure(1, weight=1)

        self.widget_list_attendance_title = LabelCustom(self.widget_list_attendance, "DANH SÁCH SINH VIÊN ĐIỂM DANH", font_size=12)
        self.widget_list_attendance_title.grid(row=0, column=0, padx=10, pady=3, sticky="nw")
        
        self.widget_list_attendance_table = ctk.CTkFrame(self.widget_list_attendance, fg_color="transparent")
        self.widget_list_attendance_table.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nwse")
        self.widget_list_attendance_table.grid_rowconfigure(0, weight=1)
        self.widget_list_attendance_table.grid_columnconfigure(0, weight=1)

        
        self.table = CustomTable(master=self.widget_list_attendance_table, columns=["Họ Tên Sinh Viên", "Thời gian điểm danh", "Trạng thái", "Lớp", "Năm Sinh", "Giới tính", "Ghi Chú"],
                                 column_widths=[220, 130, 130, 100, 100, 100, 200],
                                 data=[[None, None, None, None, None, None, None]],
                                 scroll=True,
                                 highlight_columns=[1, 2],
                                 highlight_color="#F2BEEF"
                                 )
        self.table.grid(padx=0, pady=0, sticky="nsew")
        

        # === THIẾT LẬP LƯỚI TỔNG ===
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # +++ HÀM LOAD DATA +++
        # Load combobox
        self.populate_comboboxes()



    # === CÁC HÀM CHỨC NĂNG NÚT ===
    def show_searchStudent(self):
        LecturerAttendance_SearchStudent.show_window(parent=self, username=self.username)
        
        
    def show_tranning_face(self):
        WidgetTranningFace.show_window(parent=self)
        
    # === CÁC HÀM CHỨC NĂNG (ĐÃ CẢI TIẾN) ===

    def on_class_selected(self, selected_class):
        """
        Khi một lớp được chọn, bắt đầu một luồng mới để tải dữ liệu
        mà không làm treo giao diện.
        """
        # (Tùy chọn) Vô hiệu hóa các combobox để người dùng không thao tác khi đang tải
        self.widget_attendance_options_left_cbxSubject.configure(state="disabled")
        self.widget_attendance_options_left_cbxDate.configure(state="disabled")
        self.widget_attendance_options_left_cbxSession.configure(state="disabled")
        # Hiển thị trạng thái đang tải, ví dụ:
        self.widget_attendance_options_left_cbxSubject.set("Đang tải...")
        self.widget_attendance_options_left_cbxDate.set("Đang tải...")
        self.widget_attendance_options_left_cbxSession.set("Đang tải...")


        # Tạo và bắt đầu luồng mới
        thread = threading.Thread(target=self._load_data_for_selection, args=(selected_class,))
        thread.daemon = True  # Đảm bảo luồng sẽ tắt khi chương trình chính tắt
        thread.start()

    def _load_data_for_selection(self, selected_class):
        """
        Hàm này chạy trong luồng nền để lấy dữ liệu từ DB.
        """
        # 1. Lấy danh sách môn học
        subjects = Db.get_subjects_by_class(self.username, selected_class)
        dates = []
        sessions = []
        
        default_subject = "Không có"
        default_date = "Không có"
        default_session = "Không có"

        if subjects:
            default_subject = subjects[0]
            # 2. Lấy danh sách ngày
            dates = Db.get_dates_of_subject(self.username, default_subject)
            if dates:
                default_date = dates[0]
                # 3. Lấy danh sách buổi
                sessions = Db.get_sessions_of_date(self.username, default_subject, default_date)
                if sessions:
                    default_session = sessions[0]

        # Dữ liệu đã sẵn sàng, yêu cầu luồng chính cập nhật giao diện
        self.after(0, self._update_comboboxes_from_thread, 
                  subjects, default_subject, 
                  dates, default_date, 
                  sessions, default_session)

    def _update_comboboxes_from_thread(self, subjects, default_subject, dates, default_date, sessions, default_session):
        """
        Hàm này được gọi bởi luồng chính để cập nhật an toàn các widget.
        """
        # Cập nhật combobox Môn học
        if subjects:
            self.widget_attendance_options_left_cbxSubject.configure(values=subjects, state="readonly")
            self.widget_attendance_options_left_cbxSubject.set(default_subject)
        else:
            self.widget_attendance_options_left_cbxSubject.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxSubject.set("Không có")

        # Cập nhật combobox Ngày
        if dates:
            self.widget_attendance_options_left_cbxDate.configure(values=dates, state="readonly")
            self.widget_attendance_options_left_cbxDate.set(default_date)
        else:
            self.widget_attendance_options_left_cbxDate.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxDate.set("Không có")
        
        # Cập nhật combobox Buổi
        if sessions:
            self.widget_attendance_options_left_cbxSession.configure(values=sessions, state="readonly")
            self.widget_attendance_options_left_cbxSession.set(default_session)
        else:
            self.widget_attendance_options_left_cbxSession.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxSession.set("Không có")


        # Cuối cùng, cập nhật bảng điểm danh
        self.show_attendance_list()


    def on_subject_selected(self, selected_subject):
        """(Luồng chính) Bắt đầu luồng tải dữ liệu cho Ngày và Buổi."""
        if not selected_subject or "Đang tải" in selected_subject or selected_subject == "Không có":
            return

        # Vô hiệu hóa các widget phụ thuộc
        self.widget_attendance_options_left_cbxDate.configure(state="disabled")
        self.widget_attendance_options_left_cbxDate.set("Đang tải...")
        self.widget_attendance_options_left_cbxSession.configure(state="disabled")
        self.widget_attendance_options_left_cbxSession.set("Đang tải...")

        # Bắt đầu luồng mới
        thread = threading.Thread(target=self._load_data_for_subject, args=(selected_subject,))
        thread.daemon = True
        thread.start()

    def _load_data_for_subject(self, selected_subject):
        """(Luồng nền) Lấy danh sách Ngày và Buổi từ DB."""
        dates = Db.get_dates_of_subject(self.username, selected_subject)
        sessions = []
        default_date = "Không có"
        default_session = "Không có"

        if dates:
            default_date = dates[0]
            sessions = Db.get_sessions_of_date(self.username, selected_subject, default_date)
            if sessions:
                default_session = sessions[0]

        # Yêu cầu luồng chính cập nhật giao diện
        self.after(0, self._update_date_session_from_thread, 
                  dates, default_date, 
                  sessions, default_session)

    def _update_date_session_from_thread(self, dates, default_date, sessions, default_session):
        """(Luồng chính) Cập nhật combobox Ngày và Buổi."""
        # Cập nhật combobox Ngày
        if dates:
            self.widget_attendance_options_left_cbxDate.configure(values=dates, state="readonly")
            self.widget_attendance_options_left_cbxDate.set(default_date)
        else:
            self.widget_attendance_options_left_cbxDate.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxDate.set("Không có")

        # Cập nhật combobox Buổi
        if sessions:
            self.widget_attendance_options_left_cbxSession.configure(values=sessions, state="readonly")
            self.widget_attendance_options_left_cbxSession.set(default_session)
        else:
            self.widget_attendance_options_left_cbxSession.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxSession.set("Không có")

        # Cập nhật bảng
        self.show_attendance_list()

    def on_date_selected(self, selected_date):
        """(Luồng chính) Bắt đầu luồng tải dữ liệu cho Buổi học."""
        if not selected_date or "Đang tải" in selected_date or selected_date == "Không có":
            return

        # Vô hiệu hóa widget phụ thuộc
        self.widget_attendance_options_left_cbxSession.configure(state="disabled")
        self.widget_attendance_options_left_cbxSession.set("Đang tải...")

        # Bắt đầu luồng mới
        thread = threading.Thread(target=self._load_data_for_date, args=(selected_date,))
        thread.daemon = True
        thread.start()

    def _load_data_for_date(self, selected_date):
        """(Luồng nền) Lấy danh sách Buổi từ DB."""
        # Phải lấy môn học hiện tại từ combobox
        subject = self.widget_attendance_options_left_cbxSubject.get()
        
        sessions = Db.get_sessions_of_date(self.username, subject, selected_date)
        default_session = sessions[0] if sessions else "Không có"

        # Yêu cầu luồng chính cập nhật giao diện
        self.after(0, self._update_session_from_thread, sessions, default_session)

    def _update_session_from_thread(self, sessions, default_session):
        """(Luồng chính) Cập nhật combobox Buổi."""
        if sessions:
            self.widget_attendance_options_left_cbxSession.configure(values=sessions, state="readonly")
            self.widget_attendance_options_left_cbxSession.set(default_session)
        else:
            self.widget_attendance_options_left_cbxSession.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxSession.set("Không có")
        
        # Cập nhật bảng
        self.show_attendance_list()

    def populate_comboboxes(self):
        """
        Hàm khởi tạo, load dữ liệu lần đầu cho tất cả các combobox.
        Logic được rút gọn vì các hàm on_..._selected đã xử lý chuỗi.
        """
        self.all_classes = Db.get_classes_of_lecturer(self.username)
        if self.all_classes:
            self.widget_attendance_options_left_cbxClass.configure(values=self.all_classes, state="readonly")
            default_class = self.all_classes[0]
            self.widget_attendance_options_left_cbxClass.set(default_class)
            self.on_class_selected(default_class)
        else:
            self.widget_attendance_options_left_cbxClass.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxClass.set("Không có")
            # Vô hiệu hóa các combobox còn lại nếu không có lớp nào
            self.widget_attendance_options_left_cbxSubject.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxSubject.set("Không có")
            self.widget_attendance_options_left_cbxDate.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxDate.set("Không có")
            self.widget_attendance_options_left_cbxSession.configure(values=["Không có"], state="disabled")
            self.widget_attendance_options_left_cbxSession.set("Không có")
            messagebox.showinfo("Thông báo", "Giảng viên này chưa được phân công lớp học phần nào.")
            self.show_attendance_list() # Cập nhật bảng với dữ liệu trống

    def show_attendance_list(self):
        class_name = self.widget_attendance_options_left_cbxClass.get()
        subject_name = self.widget_attendance_options_left_cbxSubject.get()
        date = self.widget_attendance_options_left_cbxDate.get()
        session = self.widget_attendance_options_left_cbxSession.get()
        
        # Kiểm tra nếu thiếu thông tin hoặc thông tin là "Không có" thì không load
        if not all([class_name, subject_name, date, session]) or \
           "Không có" in [class_name, subject_name, date, session]:
            data = [[None, None, None, None, None, None, None]]
        else:
            data = Db.get_attendance_list_of_class(class_name, subject_name, date, session)
            if not data: # Nếu không có dữ liệu trả về từ DB
                data = [[None, None, None, None, None, None, None]]


        self.table.update_data(data)
