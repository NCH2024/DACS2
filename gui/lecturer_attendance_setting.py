import customtkinter as ctk
from gui.utils import SliderWithLabel, SwitchOption, ButtonTheme, LabelCustom

class LecturerAttendance_Setting(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="white")
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # Tiêu đề
        self.title = ctk.CTkLabel(self, text="Dashboard > Điểm danh sinh viên > Cài đặt", font=("Bahnschrift", 14, "bold"))
        self.title.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 5), sticky="w")

        # Phân nhóm
        self.name_setting = ctk.CTkLabel(self, text="THIẾT LẬP NHẬN DẠNG", font=("Bahnschrift", 12), text_color="#0044FF")
        self.name_setting.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="w")

        # Thanh trượt tỷ lệ nhận dạng
        self.slider_accuracy = SliderWithLabel(self, "Tỷ lệ chính xác nhận dạng khuôn mặt: (Khuyên dùng mức 0.6)", initial=0.60)
        self.slider_accuracy.grid(row=2, column=0, columnspan=3, padx=20, pady=(0, 10), sticky="ew")

        # Các tuỳ chọn bật/tắt
        self.switch_realtime = SwitchOption(self, "Hiển thị hình ảnh nhận dạng trong thời gian thực:\n(Tuỳ chọn sẽ hiển thị trực tiếp hình ảnh mà camera ghi nhận trong hộp thoại)", initial=True)
        self.switch_realtime.grid(row=3, column=0, columnspan=3, padx=20, pady=5, sticky="ew")

        self.switch_autosave = SwitchOption(self, "Lưu trữ nhận dạng khuôn mặt nếu như dữ liệu khuôn mặt đạt mức tốt nhất:\n(Không nên bật nếu máy có cấu hình yếu!)", initial=False)
        self.switch_autosave.grid(row=4, column=0, columnspan=3, padx=20, pady=5, sticky="ew")

        self.switch_sound = SwitchOption(self, "Cảnh báo âm thanh khi nhận dạng:", initial=False)
        self.switch_sound.grid(row=5, column=0, columnspan=3, padx=20, pady=5, sticky="ew")

        # Nhóm nút chức năng
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=6, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)

        # Nút trái: Cài lại
        self.reset_btn = ButtonTheme(button_frame, text="Cài lại", fg_color="#007BFF", width=100, command=self.reset_settings)
        self.reset_btn.grid(row=0, column=0, sticky="w")

        # Nhóm phải: LƯU + THOÁT
        right_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_buttons.grid(row=0, column=1, sticky="e")

        self.save_btn = ButtonTheme(right_buttons, text="LƯU", fg_color="#33F198", width=100, command=self.save_settings)
        self.save_btn.grid(row=0, column=0, padx=(0, 10))

        self.exit_btn = ButtonTheme(right_buttons, text="THOÁT", fg_color="#000F58", width=100, command=self.quit_settings)
        self.exit_btn.grid(row=0, column=1)

    def reset_settings(self):
        self.slider_accuracy.set_value(0.6)
        self.switch_realtime.set_value(True)
        self.switch_autosave.set_value(False)
        self.switch_sound.set_value(False)

    def save_settings(self):
        acc = self.slider_accuracy.get_value()
        real = self.switch_realtime.get_value()
        save = self.switch_autosave.get_value()
        sound = self.switch_sound.get_value()
        print(f"Saved! Accuracy: {acc}, Realtime: {real}, SaveFace: {save}, Sound: {sound}")

    def quit_settings(self):
        self.master.destroy()

    _window_instance = None

    @classmethod
    def show_window(cls, parent=None):
        if cls._window_instance is None or not cls._window_instance.winfo_exists():
            top = ctk.CTkToplevel()
            top.geometry("500x500")
            top.title("Cài đặt")
            top.configure(fg_color="white")

            if parent:
                top.transient(parent.winfo_toplevel())

            top.lift()
            top.focus_force()

            cls._window_instance = top

            frame = cls(master=top)
            frame.grid(row=0, column=0, sticky="nsew")
            top.grid_rowconfigure(0, weight=1)
            top.grid_columnconfigure(0, weight=1)

            def on_close():
                cls._window_instance.destroy()
                cls._window_instance = None

            top.protocol("WM_DELETE_WINDOW", on_close)
        else:
            cls._window_instance.focus_force()
