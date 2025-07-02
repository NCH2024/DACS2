import customtkinter as ctk
import core.database as Db
from gui.utils import WigdetFrame as WF
from gui.utils import LabelCustom as LBL
from gui.utils import CustomTable as TB
from gui.utils import NotifyList

class LecturerHome(ctk.CTkFrame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)
        self.username = username

        self._border_width = 1
        self._border_color = "white"
        self._fg_color = "white"

        # Lấy thông tin giảng viên
        self.info = self.getInfoLecturer(self.username)
        
        # Lấy lịch điểm danh sơ bộ
        self.data = self.getSchedule(self.username)

        # Biến màu sắc
        self.widget_color = "#2DFCB0"

        # Cấu hình grid tổng thể
        self.grid_rowconfigure((0,1,2), weight=0)
        self.grid_columnconfigure((0,1,2), weight=1)


        # Tiêu đề
        self.title_widget = ctk.CTkLabel(
            self, text="Dashboard > TRANG CHỦ", 
            font=("Bahnschrift", 20, "bold"), 
            text_color="#05243F"
        )
        self.title_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

        # Widget chứa thông tin giảng viên
        self.info_lecturer = WF(self, width=400, height=300, widget_color=self.widget_color, row=1, column=0, padx=10, pady=10, sticky="nw")
        '''Widget con của info_lecturer'''
        self.slogan = LBL(self.info_lecturer, "THÔNG TIN GIẢNG VIÊN", font_size=12, font_weight="bold", text_color="#011EB1", pack_pady=0, pack_padx=20)

        # Kiểm tra dữ liệu
        if self.info:
            ma_gv, ten_gv, sdt, ma_khoa, namsinh, ghichu = self.info
        else:
            ma_gv = ten_gv = sdt = ma_khoa = namsinh = ghichu = "Không có dữ liệu"

        self.lbl_name = LBL(self.info_lecturer, "Giảng Viên: ", value=ten_gv, font_weight="bold")
        self.lbl_id = LBL(self.info_lecturer, "Mã cán bộ: ", value=ma_gv, font_weight="bold")
        self.lbl_age = LBL(self.info_lecturer, "Năm sinh: ", value=str(namsinh), font_weight="bold")
        self.lbl_numberPhone = LBL(self.info_lecturer, "Số điện thoại: ", value=str(sdt), font_weight="bold")
        self.lbl_faculty = LBL(self.info_lecturer, "Khoa: ", value=ma_khoa, font_weight="bold")
        self.lbl_notes = LBL(self.info_lecturer, "Thông tin khác: ", value=ghichu, font_weight="italic", value_weight="italic")

        # Widget xem lịch nhanh điểm danh các lớp được phân công
        self.info_schedule = WF(self, width=500, height=250, widget_color=self.widget_color, row=2, column=0,rowspan=2, padx=10, pady=10, sticky="nw")
        self.slogan = LBL(self.info_schedule, "PHÂN CÔNG ĐIỂM DANH CÁC LỚP", font_size=12, font_weight="bold", text_color="#011EB1", pack_pady=0, pack_padx=20, row_pad_y=0)
        self.slogan_second = LBL(self.info_schedule, "Xem nhanh lịch mà bạn được phân công: ", font_size=13, pack_pady=0, pack_padx=30, row_pad_y=0)
        """Thiết lập bảng hiển thị lịch"""
        self.tb_schedule = TB(self.info_schedule, 
                              columns=["LỚP", "HỌC PHẦN", "HỌC KỲ", "SỐ BUỔI"],
                              column_widths=[100, 200, 80, 70],
                              data=self.data,
                              scroll=True,
                              table_height=300,
                              table_width=470)
        self.tb_schedule.pack(padx=20, pady=10)
        

        # Widget xem thông báo từ cơ quan - nhà trường
        self.info_notify = WF(self, width=500, height=850, widget_color=self.widget_color, row=1, column=1, rowspan=3, padx=10, pady=5, sticky="ne", grid_propagate=False)
        self.slogan = LBL(self.info_notify, "THÔNG BÁO", font_size=12, font_weight="bold", text_color="#FF0000", pack_pady=0, pack_padx=20)
        self.slogan_second = LBL(self.info_notify, "Cán bộ giảng viên hãy lưu ý thông báo mới nhất!", font_size=12, pack_pady=0, pack_padx=20, row_pad_y=0)
        DataNotify = Db.get_thongbao()
        notifies = NotifyList(self.info_notify, data=DataNotify )
        notifies.pack(fill="both", expand=True, padx=20, pady=20)

    def getInfoLecturer(self, username):
        return Db.get_info_lecturer(username) or None
    
    def getSchedule(self, username):
        data = []
        if Db.get_schedule(username):
            data = Db.get_schedule(username)
            return data
        else:
            return [['','','','']]


