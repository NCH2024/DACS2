import customtkinter as ctk
from gui.utils import *

class LecturerAttendance_SearchStudent(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Màu nền trắng tổng thể
        self.configure(fg_color="white")

        # Biến màu sắc
        self.widget_color = "#2DFCB0"
        self.txt_color_title = "#1736FF"

        # Bố cục tổng thể
        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=70)  # bên trái to hơn
        self.grid_columnconfigure(1, weight=30)  # bên phải nhỏ hơn
        self.grid_rowconfigure(1, weight=1)     # cho phép dãn chiều cao nội dung

        # === TIÊU ĐỀ ===
        self.txt_title = LabelCustom(self, "Dashboard > Điểm danh sinh viên > Tra cứu sinh viên",
                                     wraplength=600, font_size=16, text_color="#05243F")
        self.txt_title.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="nw")

        # === KHUNG TRÁI ===
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=1, column=0, padx=(15, 7), pady=10, sticky="nsew")
        self.left_frame.grid_rowconfigure(0, weight=0)  # info sv
        self.left_frame.grid_rowconfigure(1, weight=1)  # info điểm danh
        self.left_frame.grid_columnconfigure(0, weight=1)

        # --- THÔNG TIN SINH VIÊN ---
        self.widget_student = ctk.CTkFrame(self.left_frame, fg_color="white", height=300, border_color=self.widget_color, border_width=2)
        self.widget_student.grid(row=0, column=0, sticky="nsew", pady=(0, 7))
        self.widget_student.grid_propagate(False)  # Giữ đúng chiều cao
        self.widget_student.grid_columnconfigure(0, weight=10)
        self.widget_student.grid_columnconfigure(1, weight=90)
        self.widget_student.grid_rowconfigure(0, weight=0)
        self.widget_student.grid_rowconfigure(1, weight=1)
        
        self.widget_student_title = LabelCustom(self.widget_student, "THÔNG TIN SINH VIÊN", font_size=12, text_color=self.txt_color_title)
        self.widget_student_title.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky="nw")
        
        # --- Khung chứa ảnh sinh viên ---
        self.widget_student_image = ctk.CTkFrame(self.widget_student, fg_color="transparent")
        self.widget_student_image.grid(row=1, column=0, padx=(2,0), pady=2, sticky="nsew")
        
        self.bg_ctkimage = ImageProcessor("resources/images/avatar_default.jpeg") \
                                .crop_to_aspect(160, 180) \
                                .resize(160, 180) \
                                .to_ctkimage(size=(160,180))
        self.bg_label = ctk.CTkLabel(self.widget_student_image, image=self.bg_ctkimage, text="")
        self.bg_label.pack(anchor="n", pady=5) 
        
        # --- khung chứ thông tin sinh viên ---
        self.widget_student_info = ctk.CTkFrame(self.widget_student, fg_color="transparent")
        self.widget_student_info.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        
        self.txt_HoTen = LabelCustom(self.widget_student_info, "Họ và Tên: ", value=None)
        self.txt_Class = LabelCustom(self.widget_student_info, "Lớp: ", value=None)
        self.txt_Birthday = LabelCustom(self.widget_student_info, "Năm sinh: ", value=None)
        self.txt_Level = LabelCustom(self.widget_student_info, "Bậc học: ", value=None)
        self.txt_SchoolYear = LabelCustom(self.widget_student_info, "Niên khoá: ", value=None)
        self.txt_Specialized = LabelCustom(self.widget_student_info, "Chuyên ngành: ", value=None)
        self.txt_Notes = LabelCustom(self.widget_student_info, "Ghi chú: ", value=None)

       # --- THÔNG TIN ĐIỂM DANH ---
        self.widget_aboutAttendance = ctk.CTkFrame(
            self.left_frame,
            fg_color="white",
            border_color=self.widget_color,
            border_width=2,
            height=120
        )
        self.widget_aboutAttendance.grid(row=1, column=0, sticky="nsew")
        self.widget_aboutAttendance.grid_columnconfigure((0, 1), weight=1)
        self.widget_aboutAttendance.grid_propagate(False)

        self.widget_aboutAttendance_title = LabelCustom(
            self.widget_aboutAttendance,
            "THÔNG TIN ĐIỂM DANH",
            font_size=12,
            text_color=self.txt_color_title
        )
        self.widget_aboutAttendance_title.pack(anchor="w", padx=5, pady=(5, 2))

        # --- GOM NHÓM KHUNG THÔNG TIN ---
        frame_left_info = ctk.CTkFrame(self.widget_aboutAttendance, fg_color="transparent")
        frame_right_info = ctk.CTkFrame(self.widget_aboutAttendance, fg_color="transparent")
        frame_left_info.pack(side="left", padx=(5, 0), pady=0)
        frame_right_info.pack(side="left", padx=(0, 5), pady=0)

        # === BÊN TRÁI: Học phần, Ngày, Buổi ===
        self.widget_aboutAttendance_subject = LabelCustom(frame_left_info, "Học phần:", value="Tư tưởng của chủ tịch Hồ Chí Minh", font_size=14, wraplength=150)
        self.widget_aboutAttendance_subject.pack(anchor="w", pady=(0, 1))
        self.widget_aboutAttendance_date = LabelCustom(frame_left_info, "Ngày:", value="None", font_size=14, wraplength=150)
        self.widget_aboutAttendance_date.pack(anchor="w", pady=(0, 1))
        self.widget_aboutAttendance_session = LabelCustom(frame_left_info, "Buổi:", value="None", font_size=14, wraplength=150)
        self.widget_aboutAttendance_session.pack(anchor="w", pady=(0, 1))

        # === BÊN PHẢI: Thời gian điểm danh, Trạng thái ===
        self.widget_aboutAttendance_timeAttendance = LabelCustom(
            frame_right_info,
            "Thời gian điểm danh:",
            value="None",
            text_color="red",
            font_size=14, wraplength=150
        )
        self.widget_aboutAttendance_timeAttendance.pack(anchor="w", pady=(0, 1))

        self.widget_aboutAttendance_state = LabelCustom(
            frame_right_info,
            "Trạng thái:",
            value="None",
            text_color="red",
            font_size=14, wraplength=150
        )
        self.widget_aboutAttendance_state.pack(anchor="w", pady=(0, 1))


        # === KHUNG PHẢI ===
        self.widget_search = ctk.CTkFrame(self, fg_color=self.widget_color, width=300)
        self.widget_search.grid(row=1, column=1, padx=(7, 15), pady=10, sticky="nsew")
        self.widget_search.grid_propagate(False)
        self.widget_search.grid_columnconfigure((0,1), weight=1)
        self.widget_search.grid_rowconfigure(0, weight=0)
        
        self.widget_search_title = LabelCustom(self.widget_search, "TÌM KIẾM", font_size=12, text_color=self.txt_color_title)
        self.widget_search_title.grid(row=0, column=0, columnspan=2, padx=5, pady=0, sticky="nw")
        
        self.ent_IDStudent = ctk.CTkEntry(self.widget_search, placeholder_text="Nhập vào MSSV", 
                                            width=150, height=40, font=("Bahnschrift", 14))
        self.ent_IDStudent.grid(row=1, column=0, padx=(10,0), pady=0, sticky="nw")
        
        self.btn_searchQuickly = ButtonTheme(self.widget_search, "Tìm kiếm nhanh", width=100)
        self.btn_searchQuickly.grid(row=1, column=1, padx=(0,10), pady=0, sticky="ne")
        
        self.widget_search_title = LabelCustom(self.widget_search, "TÌM KIẾM THÔNG TIN ĐIỂM DANH", font_size=12, text_color=self.txt_color_title)
        self.widget_search_title.grid(row=2, column=0, columnspan=2, padx=5, pady=(10,2), sticky="nw")
        
        self.cbx_subject = ComboboxTheme(self.widget_search, values=["None"])
        self.cbx_subject.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nwe")
        
        self.cbx_date = ComboboxTheme(self.widget_search, values=["None"])
        self.cbx_date.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nwe")
        
        self.cbx_session = ComboboxTheme(self.widget_search, values=["None"])
        self.cbx_session.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nwe")
        
        self.btn_searchAll = ButtonTheme(self.widget_search, "Tìm kiếm điểm danh", width=100)
        self.btn_searchAll.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="new")
        
        self.note = LabelCustom(self.widget_search, "\nHƯỚNG DẪN:\n\n1. Giảng viên nhập vào ô MSSV và bấm Tìm kiếm nhanh để xem thông tin sinh viên.\n\n2. Nếu muốn xem quá trình điểm danh tại một thời điểm của sinh viên, vui lòng nhập đầy đủ MSSV và chọn các thành phần phù hợp rồi mới bấm Tìm kiếm điểm danh.", font_size=10 , wraplength=300)
        self.note.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="wse")
    
    
    # ==== CHẾ ĐỘ HIỂN THỊ DẠNG CỬA SỔ ====
    _window_instance = None

    @classmethod
    def show_window(cls, parent=None):
        if cls._window_instance is None or not cls._window_instance.winfo_exists():
            top = ctk.CTkToplevel()
            top.geometry("950x600")
            top.title("Tra cứu sinh viên")
            top.configure(fg_color="white")

            if parent:
                top.transient(parent.winfo_toplevel())

            top.lift()
            top.focus_force()

            cls._window_instance = top

            cls(master=top)

            def on_close():
                cls._window_instance.destroy()
                cls._window_instance = None

            top.protocol("WM_DELETE_WINDOW", on_close)
        else:
            cls._window_instance.focus_force()
