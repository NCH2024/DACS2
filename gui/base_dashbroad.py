'''
FILE NAME: gui/base_dashbroad.py
CODE BY: Nguyễn Chánh Hiệp 
DATE: 22/06/2025
DESCRIPTION:
        + Đây là lớp cơ sở (base class) cho các giao diện dạng Bảng điều khiển (Dashboard).
        + Định nghĩa bố cục chung bao gồm một thanh bên (sidebar) và một khu vực nội dung (content).
        + Cung cấp các thành phần chung như logo, nút đăng xuất và phương thức 'clear_content' để chuyển đổi giữa các trang.
VERSION: 1.0.0
'''
import customtkinter as ctk
from gui.base_view import BaseView
from gui.utils import ImageProcessor

class DashbroadView(BaseView):
    """
    Lớp cơ sở cho các giao diện Bảng điều khiển (Dashboard).

    Kế thừa từ `BaseView` và thiết lập một bố cục hai cột tiêu chuẩn:
    - Một thanh bên (sidebar) cho điều hướng và các chức năng chung.
    - Một khu vực nội dung (content) để hiển thị các trang con.
    """
    def __init__(self, master, enable_fullscreen_control=False, disable_resize=False, *args, **kwargs):
        """
        Khởi tạo giao diện Bảng điều khiển.

        Args:
            master: Widget cha (thường là một cửa sổ Toplevel).
        """
        super().__init__(master, enable_fullscreen_control=enable_fullscreen_control, disable_resize=disable_resize, *args, **kwargs)
        self.pack(fill="both", expand=True)
        self.master.state("zoomed")
        self.configure(fg_color="#05243F")

        # Sidebar (menu bên trái)
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="#05243F")
        # Content area (bên phải)
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="white")

        # Sử dụng grid thay cho pack
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.content.grid(row=0, column=1, sticky="nsew")

        # Cấu hình grid để sidebar rộng 400, content mở rộng
        self.grid_columnconfigure(0, minsize=300)      
        self.grid_columnconfigure(1, weight=1)         
        self.grid_rowconfigure(0, weight=1)            

        # Thêm hình ảnh logo
        self.bg_ctkimage = ImageProcessor("resources/images/dnc.png") \
                                .crop_to_aspect(150, 150) \
                                .resize(150, 150) \
                                .to_ctkimage(size=(150, 150))

        self.bg_label = ctk.CTkLabel(self.sidebar, image=self.bg_ctkimage, text="")
        self.bg_label.pack(pady=10, padx=5)
        
        self.btn_logout = self.ButtonTheme(self.sidebar, "Đăng xuất",font=("Bahnschrift", 12, "normal"),height=30, width=120, fg_color="#73B8E9", hover_color="blue", command=self.logout)
        self.btn_logout.pack(pady=5, padx=5, anchor="s", fill="y")
        
    def clear_content(self):
        """
        Xóa tất cả các widget con khỏi khu vực nội dung (content frame).

        Phương thức này được sử dụng để dọn dẹp giao diện trước khi hiển thị một trang mới,
        đảm bảo không có widget cũ nào còn sót lại.
        """
        for widget in self.content.winfo_children():
            widget.destroy()
            
            
    def logout(self):
        """
        Xử lý sự kiện đăng xuất.
        
        Phương thức này sẽ đóng cửa sổ dashboard hiện tại và hiển thị lại cửa sổ đăng nhập.
        """
        self.master.master.deiconify()
        self.master.destroy()