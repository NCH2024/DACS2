import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

class BaseView(ctk.CTkFrame):
    def __init__(self, master, 
                 enable_fullscreen_control=True, 
                 message_exit=True, 
                 disable_resize=True,
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.pack(expand=True, fill="both")
        self._fg_color="#05243F",
       


        if enable_fullscreen_control:
            self.DisableFullscreen()
        if message_exit:
            self.master.protocol("WM_DELETE_WINDOW", self.ExitWindow)
        if disable_resize:
            self.master.resizable(False, False)
        


    def LabelFont(self, master, text, font=("Bahnschrift", 20, "bold"), justify="center", **kwargs):
        """Tạo một nhãn với phông chữ tùy chỉnh."""
        return ctk.CTkLabel(master, textvariable=text, font=font, justify=justify, **kwargs)
    
    def ButtonTheme(self, master, text, font=("Bahnschrift", 18, "bold"), fg_color="green", hover_color="darkblue", border_color="white", border_width=2, command=None, **kwargs):
        """Tạo mẫu nút"""
        return ctk.CTkButton(master=master, text=text, font=font, fg_color=fg_color, hover_color=hover_color, border_color=border_color, border_width=border_width, command=command, **kwargs)

    def DisableFullscreen(self):
        """Vô hiệu hóa chế độ toàn màn hình"""
        self.master.resizable(False, False)
        self.master.bind("<F11>", lambda event: self.DisableFullscreen())
        
    def ExitWindow(self):
        """Đóng cửa sổ ứng dụng."""
        answer = messagebox.askokcancel("Thông Báo!", "Bạn có chắc chắn muốn thoát ứng dụng không?")
        if answer:
            self.master.quit()
        else:
            pass 
        
    def show_message(self, title, message):
        """Hiển thị thông báo."""
        messagebox.showinfo(title, message)


if __name__ == "__main__":

    root = ctk.CTk()
    root.title("Base View Example")
    root.geometry("800x600")
    home = BaseView(master=root)
    

    root.mainloop()