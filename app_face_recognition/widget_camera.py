import customtkinter as ctk
from PIL import *
from gui.utils import *
from PIL import Image, ImageTk

class WidgetCamera(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Biến màu sắc
        self.widget_color = "#2DFCB0"
        self.txt_color_title = "#1736FF"
        self._fg_color = "#05243F"
        
         # Màu nền đen tổng thể
        self.configure(fg_color=self._fg_color)
        
        # Biến Lưu trữ hình ảnh nút trên giao diện
        play_img = Image.open("resources/images/play-button.png")
        pause_img = Image.open("resources/images/pause.png")
        exit_img = Image.open("resources/images/cross.png")
        
        self.play_img = ImageProcessor(play_img)
        self.pause_img = ImageProcessor(pause_img)
        self.exit_img = ImageProcessor(exit_img)
        
        self.camera_label = None
        self.camera_manager = None

        self.is_playing = False # Biến để theo dõi trạng thái play/pause

        
        # --- Bố cục tổng thể ---
        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=95)
        self.grid_rowconfigure(1, weight=5)
             
        
        # --- Frame trên hiển thị hình ảnh trực tiếp ---
        self.widget_videoCapture = ctk.CTkFrame(self, fg_color="black", height=480, width=320, corner_radius=0)
        self.widget_videoCapture.grid(row=0, column=0, padx=10, pady=(20,10), sticky="news")
        self.widget_videoCapture.propagate(False)
        self.widget_videoCapture.grid_columnconfigure(0, weight=1)
        
        
        # --- Frame dưới hiển thị nút tạm dừng, dừng, thoát ---
        self.widget_groupBtn = ctk.CTkFrame(self, fg_color="transparent", height=100)
        self.widget_groupBtn.grid(row=1, column=0, padx=50, pady=(0,10), sticky="we")
        self.widget_groupBtn.grid_columnconfigure((0,1), weight=1)
        self.widget_groupBtn.grid_rowconfigure(0, weight=1)
        self.widget_groupBtn.propagate(False)
        
        self.play_btn = ButtonTheme(self.widget_groupBtn, 
                                    text="", 
                                    image=self.play_img.to_ctkimage(), 
                                    fg_color="#05243F", 
                                    hover_color=self.widget_color,
                                    width=35, 
                                    command=self.click_play)

        self.play_tooltip = Tooltip(self.play_btn, "Bắt đầu/Tạm dừng Camera")

        self.play_btn.grid(row=0, column=0, padx=2, pady=2, sticky="we")
        
        self.exit_btn = ButtonTheme(self.widget_groupBtn, 
                                    text="", 
                                    image=self.exit_img.to_ctkimage(), 
                                    fg_color="#05243F", 
                                    hover_color=self.widget_color,
                                    width=35,
                                    command=self.exit)

        self.exit_tooltip = Tooltip(self.exit_btn, "Thoát cửa sổ Camera")

        self.exit_btn.grid(row=0, column=1, padx=2, pady=2, sticky="we")
        
    def click_play(self):
        self.is_playing = not self.is_playing  

        if self.is_playing:
            self.play_btn.configure(image=self.pause_img.to_ctkimage())
             # <<< Thêm logic bắt đầu camera của bạn ở đây
        else:
            self.play_btn.configure(image=self.play_img.to_ctkimage())
             # <<< Thêm logic tạm dừng camera của bạn ở đây
             
    def exit(self):
        self.master.destroy()
        

 # ==== CHẾ ĐỘ HIỂN THỊ DẠNG CỬA SỔ ====
    _window_instance = None

    @classmethod
    def show_window(cls, parent=None, width=None, height=None, enable=1, config="fill-y"):
        if cls._window_instance is None or not cls._window_instance.winfo_exists():
            top = ctk.CTkToplevel()
            
            # --- BẮT ĐẦU: Logic để căn giữa cửa sổ ---
            if config == "fill-y":
                width = 350
                height = 620
            elif config == "fill-x":
                width = 600
                height = 420
            
            window_width = width
            window_height = height

            # Lấy kích thước màn hình
            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()

            # Tính toán vị trí x, y để cửa sổ ở giữa
            center_x = int(screen_width / 2 - window_width / 2)
            center_y = int(screen_height / 2 - window_height / 2)
            
            top.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
            top.title("CAMERA")
            top.configure(fg_color="#05243F")
            
            if enable == 0:
                top.withdraw()  
            else:
                top.deiconify()
            
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