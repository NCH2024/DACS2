import customtkinter as ctk


class WidgetCamera(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        
        
 # ==== CHẾ ĐỘ HIỂN THỊ DẠNG CỬA SỔ ====
    _window_instance = None

    @classmethod
    def show_window(cls, parent=None, username=None):
        if cls._window_instance is None or not cls._window_instance.winfo_exists():
            top = ctk.CTkToplevel()
            top.geometry("950x600")
            top.title("CAMERA - Điểm danh")
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