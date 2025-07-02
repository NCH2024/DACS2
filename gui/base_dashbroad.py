import customtkinter as ctk
from gui.base_view import BaseView
from gui.utils import ImageProcessor

class DashbroadView(BaseView):
    def __init__(self, master, enable_fullscreen_control=False, disable_resize=False, *args, **kwargs):
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
        for widget in self.content.winfo_children():
            widget.destroy()
            
            
    def logout(self):
        self.master.master.deiconify()
        self.master.destroy()