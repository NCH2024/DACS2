import customtkinter as ctk
from gui.utils import *
from tkinter import messagebox
from core.models import SinhVien
import core.database as Db
from core.utils import *

class WidgetTranningFace(ctk.CTkFrame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)
        self.username = username 
        self.session_map = {}
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
        self.txt_title = LabelCustom(self, "Dashboard > Điểm danh sinh viên > Đào tạo dữ liệu khuôn mặt",
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
        
        self.txt_HoTen = LabelCustom(self.widget_student_info, "Họ và Tên: ", value="---")
        self.txt_Class = LabelCustom(self.widget_student_info, "Lớp: ", value="---")
        self.txt_Birthday = LabelCustom(self.widget_student_info, "Năm sinh: ", value="---")
        self.txt_Level = LabelCustom(self.widget_student_info, "Bậc học: ", value="---")
        self.txt_SchoolYear = LabelCustom(self.widget_student_info, "Niên khoá: ", value="---")
        self.txt_Specialized = LabelCustom(self.widget_student_info, "Chuyên ngành: ", value="---")
        self.txt_Notes = LabelCustom(self.widget_student_info, "Ghi chú: ", value="---")

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
            "THÔNG TIN DỮ LIỆU KHUÔN MẶT",
            font_size=12,
            text_color=self.txt_color_title
        )
        self.widget_aboutAttendance_title.pack(anchor="w", padx=5, pady=(5, 2))
        
        self.widget_aboutAttendance_content1 = LabelCustom(self.widget_aboutAttendance, "DỮ LIỆU KHUÔN MẶT: ", value="---")
        self.widget_aboutAttendance_content2 = LabelCustom(self.widget_aboutAttendance, "THỜI GIAN LƯU TRỮ: ", value="---")


        # === KHUNG PHẢI ===
        self.widget_search = ctk.CTkFrame(self, fg_color=self.widget_color, width=300)
        self.widget_search.grid(row=1, column=1, padx=(7, 15), pady=10, sticky="nsew")
        self.widget_search.grid_propagate(False)
        self.widget_search.grid_columnconfigure((0,1), weight=1)
        self.widget_search.grid_rowconfigure(0, weight=0)
        
        self.widget_search_title = LabelCustom(self.widget_search, "ĐÀO TẠO NHẬN DẠNG", font_size=12, text_color=self.txt_color_title)
        self.widget_search_title.grid(row=0, column=0, columnspan=2, padx=5, pady=0, sticky="nw")
        
        self.ent_IDStudent = ctk.CTkEntry(self.widget_search, placeholder_text="Nhập vào MSSV", 
                                            width=150, height=40, font=("Bahnschrift", 14))
        self.ent_IDStudent.grid(row=1, column=0, padx=(10,0), pady=0, sticky="nw")
        
        # Kết nối nút Tìm kiếm nhanh với chức năng tra cứu sinh viên
        self.btn_searchQuickly = ButtonTheme(self.widget_search, "Tìm kiếm sinh viên", width=100, command=self.search_student)
        self.btn_searchQuickly.grid(row=1, column=1, padx=(0,10), pady=0, sticky="ne")
        
        self.widget_search_title = LabelCustom(self.widget_search, "Chọn chế độ đào tạo: ", font_size=12, text_color=self.txt_color_title)
        self.widget_search_title.grid(row=2, column=0, columnspan=2, padx=10, pady=(20, 0), sticky="nw")
        
        self.cbx_subject = ComboboxTheme(self.widget_search, values=["Đào tạo chuyên sâu", "Đào tạo nhanh"])
        self.cbx_subject.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nwe")
        
        self.check_setAvarta = SwitchOption(self.widget_search, "Dùng ảnh sau khi đào tạo làm Avatar cho sinh viên\n(Không nên bật nếu SV đã thiết lập avatar!)", wraplenght=300, initial=False, command=self.check_option)
        self.check_setAvarta.grid(row=4, column=0, columnspan=2, padx=5 , pady=20, sticky="nwe")

        
        self.btn_searchAll = ButtonTheme(self.widget_search, "Đào tạo dữ liệu", width=100)
        self.btn_searchAll.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="new")

    
    # ==== HÀM CHỨC NĂNG ====
    def _fix_none(self, val):
        return "Chưa có dữ liệu" if val is None or (isinstance(val, str) and val.strip() == "") else str(val)
    
    def check_option(self, is_checked=bool):
        if is_checked:
            messagebox.showwarning("Cảnh báo!", "Bật tuỳ chọn này sẽ thay đổi ảnh avatar của sinh viên ngay cả khi sinh viên đã tự thiết lập ảnh!")
        else:
            messagebox.showinfo("Thông báo", "Đã tắt tuỳ chọn thành công!")

    def search_student(self):
        maSV = self.ent_IDStudent.get().strip()
        if not maSV:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập MSSV.")
            return
        sv_tuple = Db.get_student_by_id(maSV)
        if not sv_tuple:
            messagebox.showinfo("Không tìm thấy", f"Không tìm thấy sinh viên với MSSV {maSV}.")
            self.clear_info()
            return

        # Lấy các trường tên riêng biệt ra biến
        ten_bac = self._fix_none(sv_tuple[1])
        ten_nienkhoa = self._fix_none(sv_tuple[2])
        ten_nganh = self._fix_none(sv_tuple[3])

        # Tạo SinhVien chỉ với các trường đúng định nghĩa (giả sử đúng thứ tự cũ)
        sv = SinhVien(
            MaSV=sv_tuple[0],
            MaBac=sv_tuple[4],
            MaNienKhoa=sv_tuple[5],
            MaNganh=sv_tuple[6],
            STTLop=sv_tuple[7],
            HoTenSV=sv_tuple[8],
            NamSinh=sv_tuple[9],
            DiaChi=sv_tuple[10],
            GioiTinh=sv_tuple[11],
            GhiChu=sv_tuple[12]
        )
        # Cập nhật giao diện, dùng _fix_none cho tất cả trường
        self.txt_Level.value.configure(text=ten_bac)
        self.txt_SchoolYear.value.configure(text=ten_nienkhoa)
        self.txt_Specialized.value.configure(text=ten_nganh)
        self.txt_Class.value.configure(text=f"{self._fix_none(sv.MaBac)}{self._fix_none(sv.MaNienKhoa)}{self._fix_none(sv.MaNganh)}{self._fix_none(sv.STTLop)}")
        self.txt_HoTen.value.configure(text=self._fix_none(sv.HoTenSV))
        self.txt_Birthday.value.configure(text=self._fix_none(sv.NamSinh))
        self.txt_Notes.value.configure(text=self._fix_none(sv.GhiChu))

    # ==== CHẾ ĐỘ HIỂN THỊ DẠNG CỬA SỔ ====
    _window_instance = None

    @classmethod
    def show_window(cls, parent=None, username=None):
        if cls._window_instance is None or not cls._window_instance.winfo_exists():
            top = ctk.CTkToplevel()
            top.geometry("950x500")
            top.title("Đào tạo dữ liệu khuôn mặt")
            top.configure(fg_color="white")
            if parent:
                top.transient(parent.winfo_toplevel())
            top.lift()
            top.focus_force()
            cls._window_instance = top

            # Truyền username vào đây
            cls(master=top)

            def on_close():
                cls._window_instance.destroy()
                cls._window_instance = None

            top.protocol("WM_DELETE_WINDOW", on_close)
        else:
            cls._window_instance.focus_force()