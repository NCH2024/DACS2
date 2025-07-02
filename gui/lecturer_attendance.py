import customtkinter as ctk

class LecturerAttendance(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self._border_width = 1
        self._border_color = "white"
        self._fg_color = "white"

        # Biến màu sắc
        self.widget_color = "#2DFCB0"

        # Cấu hình grid tổng thể
        self.grid_rowconfigure((0,1,2), weight=0)
        self.grid_columnconfigure((0,1,2), weight=1)
        
        # Tiêu đề
        self.title_widget = ctk.CTkLabel(
            self, text="Dashboard > ĐIỂM DANH SINH VIÊN", 
            font=("Bahnschrift", 20, "bold"), 
            text_color="#05243F"
        )
        self.title_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")