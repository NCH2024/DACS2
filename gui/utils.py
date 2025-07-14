from PIL import Image
import customtkinter as ctk
from PIL import Image
import os
from io import BytesIO
import threading

class ImageProcessor:
    def __init__(self, image_input):
        if isinstance(image_input, Image.Image):
            self.image = image_input
        elif isinstance(image_input, bytes):
            self.image = Image.open(BytesIO(image_input))
        else:
            self.image = Image.open(image_input)

    def crop_to_aspect(self, target_width, target_height):
        orig_width, orig_height = self.image.size
        target_ratio = target_width / target_height
        orig_ratio = orig_width / orig_height

        if orig_ratio > target_ratio:
            new_width = int(orig_height * target_ratio)
            left = (orig_width - new_width) // 2
            right = left + new_width
            top = 0
            bottom = orig_height
        else:
            new_height = int(orig_width / target_ratio)
            top = (orig_height - new_height) // 2
            bottom = top + new_height
            left = 0
            right = orig_width

        self.image = self.image.crop((left, top, right, bottom))
        return self

    def resize(self, width, height):
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.ANTIALIAS
        self.image = self.image.resize((width, height), resample)
        return self

    def to_ctkimage(self, size=None):
        if size:
            return ctk.CTkImage(light_image=self.image, size=size)
        return ctk.CTkImage(light_image=self.image)

    def to_photoimage(self):
        from PIL import ImageTk
        return ImageTk.PhotoImage(self.image)

    def save(self, path):
        self.image.save(path)

    def get_pil_image(self):
        return self.image


class ImageSlideshow(ctk.CTkFrame):
    def __init__(self, master, image_folder, size=(500, 300), delay=2000, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.size = size
        self.delay = delay  # milliseconds giữa các slide
        self.images = self.load_images(image_folder)
        self.index = 0

        self.label = ctk.CTkLabel(self, image=self.images[self.index], text="")
        self.label.pack(expand=True, fill="both")

        # Nút điều khiển (nếu muốn)
        prev_btn = ctk.CTkButton(self, text="<",
                                 width=30, 
                                 height=30,
                                 bg_color="white", 
                                 font=("Bahnschrift", 30), 
                                 corner_radius=50,  
                                 command=self.prev_image)
        next_btn = ctk.CTkButton(self, text=">", 
                                 width=30, 
                                 height=30, 
                                 bg_color="white",
                                 font=("Bahnschrift", 30), 
                                 corner_radius=50, 
                                 command=self.next_image)
        prev_btn.place(relx=0.05, rely=0.9, anchor="center")
        next_btn.place(relx=0.95, rely=0.9, anchor="center")

        self.play_slideshow()

    def load_images(self, folder):
        image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        images = []
        for fname in sorted(image_files):
            path = os.path.join(folder, fname)
            img = Image.open(path).resize(self.size)
            ctkimg = ctk.CTkImage(light_image=img, size=self.size)
            images.append(ctkimg)
        return images

    def show_image(self, idx):
        self.label.configure(image=self.images[idx])

    def next_image(self):
        self.index = (self.index + 1) % len(self.images)
        self.show_image(self.index)

    def prev_image(self):
        self.index = (self.index - 1) % len(self.images)
        self.show_image(self.index)

    def play_slideshow(self):
        self.next_image()
        self.after(self.delay, self.play_slideshow)
        
        
class WigdetFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        width=None,
        height=None,
        radius=20,
        widget_color="#2DFCB0",
        row=0,
        column=0,
        rowspan=1,
        columnspan=1,
        sticky="n",  # mặc định canh trên
        padx=10,
        pady=10,
        grid_propagate=True,
        **kwargs
    ):
        super().__init__(master, width=width, height=height, corner_radius=radius, fg_color=widget_color, **kwargs)

        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=padx, pady=pady)
        self.grid_propagate(grid_propagate) 

class ButtonTheme(ctk.CTkButton):
    def __init__(
        self,
        master,
        text,
        font=("Bahnschrift", 16, "normal"),
        fg_color="green",
        hover_color="darkblue",
        border_color="white",
        border_width=2,
        height=40,
        width=200,
        command=None,
        **kwargs
    ):
        super().__init__(
            master=master,
            text=text,
            font=font,
            fg_color=fg_color,
            hover_color=hover_color,
            border_color=border_color,
            border_width=border_width,
            height=height,
            width=width,
            command=command,
            **kwargs
        )

class ComboboxTheme(ctk.CTkComboBox):
    def __init__(
        self,
        master,
        values=[],
        command=None,
        font=("Bahnschrift", 16, "normal"),
        fg_color="white",
        border_color="#022965",
        border_width=1,
        button_color="#007F3A",
        button_hover_color="#005C2D",
        dropdown_font=("Bahnschrift", 14),
        text_color="black",
        **kwargs
    ):
        super().__init__(
            master=master,
            values=values,
            font=font,
            fg_color=fg_color,
            border_color=border_color,
            border_width=border_width,
            button_color=button_color,
            button_hover_color=button_hover_color,
            dropdown_font=dropdown_font,
            text_color=text_color,
            command=command,
            **kwargs
        )

class LabelCustom(ctk.CTkFrame):
    def __init__(
        self,
        master,
        text,
        value=None,
        text_color="#00224E",
        value_color="#0412A9",
        font_family="Bahnschrift",
        font_size=16,
        font_weight="bold",
        value_weight="normal",
        wraplength=300,
        row_pad_y=2,
        pack_pady=1,
        pack_padx=25,
        pack_anchor="w",
        fg_color="#2DFCB0", 
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        label_font = (font_family, font_size, font_weight)
        value_font = (font_family, font_size, value_weight)

        # Label bên trái
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=label_font,
            text_color=text_color,
            wraplength=wraplength,
            fg_color="transparent",
            anchor="w"
        )
        self.label.grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=row_pad_y)

        # Nếu có giá trị thì tạo label bên phải
        if value:
            self.value = ctk.CTkLabel(
                self,
                text=value,
                font=value_font,
                text_color=value_color,
                wraplength=wraplength,
                fg_color="transparent",
                justify="left",
                anchor="w"
            )
            self.value.grid(row=0, column=1, sticky="nw", pady=row_pad_y)

        # Gói gọn nguyên frame ra ngoài
        self.pack(pady=pack_pady, padx=pack_padx, anchor=pack_anchor)

class CustomTable(ctk.CTkFrame):
    def __init__(self, master, columns, data, 
                 header_color="#013A63", row_color="#E8F8F5",
                 header_text_color="white", row_text_color="black",
                 column_widths=None,
                 scroll=True,
                 table_width=None, table_height=None,
                 highlight_columns=None, highlight_color="#FFF2B2",
                 **kwargs):

        super().__init__(master, fg_color="transparent", **kwargs)

        # ... (giữ nguyên các thuộc tính khởi tạo) ...
        self.columns = columns
        self.data = data
        self.header_color = header_color
        self.row_color = row_color
        self.header_text_color = header_text_color
        self.row_text_color = row_text_color
        self.column_widths = column_widths
        self.scroll = scroll
        self.table_width = table_width
        self.table_height = table_height
        self.highlight_columns = highlight_columns or []
        self.highlight_color = highlight_color
        
        self.container = None
        self._data_widgets = [] # THAY ĐỔI: Lưu trữ các widget của hàng dữ liệu

        self.after(1, self._init_render) # Sử dụng after(1) để đảm bảo render

    def _init_render(self):
        self.update_idletasks()
        
        # --- Thiết lập container (ScrollableFrame hoặc Frame thường) ---
        if self.scroll:
            if self.container is None:
                self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
                self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
                self.grid_rowconfigure(0, weight=1)
                self.grid_columnconfigure(0, weight=1)
                self.container = self.scrollable_frame
        else:
            self.container = self

        # --- Tách biệt việc tạo bảng ---
        self._create_header()
        self._create_data_rows()

    def _create_header(self):
        """HÀM MỚI: Chỉ tạo header, chạy một lần duy nhất."""
        if not self.column_widths:
            self.update_idletasks()
            num_cols = len(self.columns)
            current_container_width = self.container.winfo_width()
            col_width = int(current_container_width / num_cols) if current_container_width > 1 else 100
            self.column_widths = [col_width] * num_cols

        for i, width in enumerate(self.column_widths):
            self.container.grid_columnconfigure(i, minsize=width)

        for col_index, col_name in enumerate(self.columns):
            label = ctk.CTkLabel(
                self.container, text=col_name,
                font=("Bahnschrift", 14, "bold"),
                text_color=self.header_text_color,
                fg_color=self.header_color,
                height=30,
                anchor="center"
            )
            label.grid(row=0, column=col_index, padx=1, pady=1, sticky="nsew")

    def _clear_data_rows(self):
        """HÀM MỚI: Chỉ xóa các widget của hàng dữ liệu."""
        for row_widgets in self._data_widgets:
            for widget in row_widgets:
                widget.destroy()
        self._data_widgets = []

    def _create_data_rows(self):
        """HÀM MỚI: Chỉ tạo các hàng dữ liệu."""
        for row_index, row_data in enumerate(self.data, start=1):
            row_widgets = []
            for col_index, cell in enumerate(row_data):
                bg_color = self.highlight_color if col_index in self.highlight_columns else self.row_color
                display_text = str(cell) if cell is not None else "-"
                
                label = ctk.CTkLabel(
                    self.container, text=display_text,
                    font=("Bahnschrift", 13),
                    text_color=self.row_text_color,
                    fg_color=bg_color,
                    height=28,
                    anchor="w"
                )
                label.grid(row=row_index, column=col_index, padx=1, pady=1, sticky="nsew")
                row_widgets.append(label)
            self._data_widgets.append(row_widgets)

    def update_data(self, new_data):
        """HÀM CẬP NHẬT ĐÃ TỐI ƯU HÓA."""
        self.data = new_data
        
        # Chỉ xóa các hàng dữ liệu cũ, giữ lại header
        self._clear_data_rows()
        
        # Tạo các hàng dữ liệu mới
        if self.container and self.container.winfo_exists():
            self._create_data_rows()
                
class NotifyCard(ctk.CTkFrame):
    def __init__(self, master, title, content, ngay_dang, image_pil, on_click=None, **kwargs):
        super().__init__(master, fg_color="white", corner_radius=15, **kwargs)

        if image_pil:
            img = ImageProcessor(image_pil).crop_to_aspect(4, 3).to_ctkimage(size=(250, 150))
        else:
            img = None

        self.image_label = ctk.CTkLabel(self, image=img, text="", width=200, height=150, corner_radius=0)
        self.image_label.image = img
        self.image_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0)

        self.title_label = ctk.CTkLabel(self, text=title, font=("Bahnschrift", 16, "bold"), text_color="#FF2020", wraplength=370)
        self.title_label.grid(row=0, column=1, sticky="w", padx=20, pady=(10, 0))

        self.date_label = ctk.CTkLabel(self, text=ngay_dang.strftime("%d/%m/%Y %H:%M"), font=("Bahnschrift", 12), text_color="#3E3E3E")
        self.date_label.grid(row=1, column=1, sticky="w", padx=20, pady=2)

        self.detail_btn = ctk.CTkButton(self, text="Xem chi tiết", command=on_click)
        self.detail_btn.grid(row=2, column=1, sticky="w", padx=20, pady=(5, 5))



class NotifyList(ctk.CTkFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", width=680, height=600)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for tb in data:
            thongbao_id, title, content, ngay_dang, image_pil = tb
            card = NotifyCard(scroll_frame, title=title, content=content, ngay_dang=ngay_dang, image_pil=image_pil,
                              on_click=lambda c=content, t=title: self.show_detail(t, c))
            card.pack(fill="x", padx=5, pady=5)
            
    def show_detail(self, title, content):
        top = ctk.CTkToplevel(self)
        top.geometry("600x600")
        top.title(title)
        top.lift() 
        top.focus_force()
        top.attributes("-topmost", True)

        ctk.CTkLabel(top, text=title, font=("Bahnschrift", 16, "bold"), wraplength=300).pack(pady=10)
        ctk.CTkLabel(top, text=content, font=("Bahnschrift", 14), wraplength=450, justify="left").pack(pady=10)
        
class SliderWithLabel(ctk.CTkFrame):
    def __init__(self, master, label_text, from_=0, to=1, initial=0.5, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.label = ctk.CTkLabel(self, text=label_text, text_color="#060056", font=("Bahnschrift", 14))
        self.label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 0))

        # Các label 0 và 1 ở hai đầu
        self.min_label = ctk.CTkLabel(self, text=str(from_), font=("Bahnschrift", 13), text_color="green")
        self.min_label.grid(row=1, column=0, sticky="w", padx=(10, 5))

        # Slider chính
        self.slider = ctk.CTkSlider(
            self,
            from_=from_,
            to=to,
            number_of_steps=100,
            command=self.update_label,
            height=15,
            progress_color="#007BC7",
            button_color="#00358B",
            button_hover_color="#002448"
        )
        self.slider.set(initial)
        self.slider.grid(row=1, column=1, sticky="ew", padx=5)

        self.max_label = ctk.CTkLabel(self, text=str(to), font=("Bahnschrift", 13), text_color="green")
        self.max_label.grid(row=1, column=2, sticky="e", padx=(5, 10))

        # Label hiển thị giá trị hiện tại
        self.value_label = ctk.CTkLabel(self, text=str(initial), text_color="green", font=("Bahnschrift", 13, "bold"))
        self.value_label.grid(row=2, column=0, columnspan=3, pady=(2, 10))

        self.grid_columnconfigure(1, weight=1)

        self.command = command

    def update_label(self, value):
        self.value_label.configure(text=f"{value:.2f}")
        if self.command:
            self.command(value)

    def get_value(self):
        return self.slider.get()

    def set_value(self, value):
        self.slider.set(value)

class SwitchOption(ctk.CTkFrame):
    def __init__(self, master, text, initial=True, command=None, wraplenght=500, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.label = ctk.CTkLabel(self, text=text, text_color="#310148", font=("Bahnschrift", 14), wraplength=wraplenght, anchor="w", justify="left")
        self.label.pack(side="left", padx=(10, 5), pady=5)

        self.switch = ctk.CTkSwitch(self, text="BẬT" if initial else "TẮT", progress_color="#00D084")
        self.switch.select() if initial else self.switch.deselect()
        self.switch.pack(side="right", padx=10)

        def on_toggle():
            self.switch.configure(text="BẬT" if self.switch.get() else "TẮT")
            if command:
                command(self.switch.get())

        self.switch.configure(command=on_toggle)

    def get_value(self):
        return self.switch.get()

    def set_value(self, value: bool):
        if value:
            self.switch.select()
        else:
            self.switch.deselect()
        self.switch.configure(text="BẬT" if value else "TẮT")

