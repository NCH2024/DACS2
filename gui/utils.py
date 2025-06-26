from PIL import Image
import customtkinter as ctk
from PIL import Image
import os

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)

    def crop_to_aspect(self, target_width, target_height):
        orig_width, orig_height = self.image.size
        target_ratio = target_width / target_height
        orig_ratio = orig_width / orig_height

        if orig_ratio > target_ratio:
            # Cắt hai bên
            new_width = int(orig_height * target_ratio)
            left = (orig_width - new_width) // 2
            right = left + new_width
            top = 0
            bottom = orig_height
        else:
            # Cắt trên dưới
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