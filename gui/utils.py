from PIL import Image
import customtkinter as ctk
from PIL import Image
import os
from io import BytesIO

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
    def __init__(self, master, image_folder, size=(500, 300), delay=3000, *args, **kwargs):
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

import customtkinter as ctk

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

        self.columns = columns
        self.data = data
        self.header_color = header_color
        self.row_color = row_color
        self.header_text_color = header_text_color
        self.row_text_color = row_text_color
        self.column_widths = column_widths
        self.scroll = scroll
        self.table_width = table_width or self.winfo_width() or 600
        self.table_height = table_height
        self.highlight_columns = highlight_columns or []  # Danh sách chỉ số cột cần tô màu
        self.highlight_color = highlight_color

        self.after(100, self._init_render)

    def _init_render(self):
        self.update_idletasks()

        if self.scroll:
            self.scrollable_frame = ctk.CTkScrollableFrame(
                self, fg_color="transparent"
            )
            self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            self.scrollable_frame.grid_rowconfigure(0, weight=1)
            self.scrollable_frame.grid_columnconfigure(0, weight=1)

            self.container = self.scrollable_frame
        else:
            self.container = self
            self.configure(width=self.table_width, height=self.table_height)

        self._create_table()

    def _create_table(self):
        num_cols = len(self.columns)

        if not self.column_widths:
            col_width = int(self.table_width / num_cols)
            self.column_widths = [col_width] * num_cols

        # Header
        for col_index, col_name in enumerate(self.columns):
            label = ctk.CTkLabel(
                self.container, text=col_name,
                font=("Bahnschrift", 14, "bold"),
                text_color=self.header_text_color,
                fg_color=self.header_color,
                width=self.column_widths[col_index],
                height=30,
                anchor="center"
            )
            label.grid(row=0, column=col_index, padx=1, pady=1, sticky="nsew")

        # Dữ liệu
        for row_index, row_data in enumerate(self.data, start=1):
            for col_index, cell in enumerate(row_data):
                bg_color = self.highlight_color if col_index in self.highlight_columns else self.row_color
                label = ctk.CTkLabel(
                    self.container, text=str(cell),
                    font=("Bahnschrift", 13),
                    text_color=self.row_text_color,
                    fg_color=bg_color,
                    width=self.column_widths[col_index],
                    height=28,
                    anchor="w"
                )
                label.grid(row=row_index, column=col_index, padx=1, pady=1, sticky="nsew")

        if not self.scroll:
            for i in range(len(self.columns)):
                self.container.grid_columnconfigure(i, weight=1)


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
        

