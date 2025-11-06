
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from datetime import datetime, date
from PIL import Image
from io import BytesIO
from gui.base.base_frame import BaseFrame
from gui.base.base_datepicker import DatePicker
from gui.base.utils import *
import core.database as db
from mysql.connector import Error
import os

class AdminNotice(BaseFrame):
    def __init__(self, master=None, user=None, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.set_label_title("Dashboard > Trang Chủ > QUẢN LÝ THÔNG BÁO")

        # --- Trạng thái ---
        self.selected_notice_id = None
        self.current_image_pil = None
        self.current_image_blob = None
        self.image_preview_label = None
        self.current_ctk_image = None # <<< Thêm dòng này để giữ tham chiếu CTkImage

        try:
            db.connect_db()
            self.setup_ui()
            self._load_notice_data()
        except Error as e:
             messagebox.showerror("Lỗi kết nối CSDL", f"Không thể kết nối CSDL: {e}\nVui lòng kiểm tra cấu hình.")
             for child in self.winfo_children():
                try: child.configure(state="disabled")
                except tk.TclError: pass
        except Exception as e:
             messagebox.showerror("Lỗi khởi tạo", f"Lỗi không xác định: {e}")

    # ... (setup_ui, on_expand, _create_notice_table giữ nguyên) ...
    def setup_ui(self):
        # Frame chính chia làm 2 cột: Trái (Form), Phải (Bảng)
        self.content_frame.grid_columnconfigure(0, weight=1) # Cột form
        self.content_frame.grid_columnconfigure(1, weight=2) # Cột bảng (rộng hơn)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # --- Frame Trái (Form Nhập liệu) ---
        form_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        form_frame.grid(row=0, column=0, padx=(5,2), pady=5, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(1, weight=0) # Tiêu đề
        form_frame.grid_rowconfigure(3, weight=1) # Nội dung (co giãn chính)
        form_frame.grid_rowconfigure(5, weight=0) # Image preview (không co giãn nhiều)
        form_frame.grid_rowconfigure(7, weight=0) # Buttons

        ctk.CTkLabel(form_frame, text="Tạo/Chỉnh sửa Thông báo:", font=("Bahnschrift", 16, "bold")).grid(
            row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(form_frame, text="Tiêu đề:", font=("Bahnschrift", 13)).grid(
            row=1, column=0, padx=(10,2), pady=(5, 2), sticky="w")
        self.notice_title_entry = ctk.CTkEntry(form_frame, placeholder_text="Nhập tiêu đề thông báo...")
        self.notice_title_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(form_frame, text="Nội dung:", font=("Bahnschrift", 13)).grid(
            row=3, column=0, padx=(10,2), pady=(0, 2), sticky="nw") # nw để label ở trên
        self.notice_content_textbox = ctk.CTkTextbox(form_frame, height=200, font=("Bahnschrift", 13), wrap="word")
        self.notice_content_textbox.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

        ctk.CTkLabel(form_frame, text="Hình ảnh:", font=("Bahnschrift", 13)).grid(
            row=5, column=0, padx=(10,2), pady=(0, 2), sticky="nw")
        
        image_control_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        image_control_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        image_control_frame.grid_columnconfigure(1, weight=1) # Preview co giãn

        self.select_image_btn = ctk.CTkButton(image_control_frame, text="Chọn ảnh", width=100, command=self._select_image)
        self.select_image_btn.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nw")

        self.image_preview_label = ctk.CTkLabel(image_control_frame, text="Chưa có ảnh", fg_color="#EAEAEA", text_color="gray", height=150, corner_radius=5)
        self.image_preview_label.grid(row=0, column=1, pady=5, sticky="ew")

        self.remove_image_btn = ctk.CTkButton(image_control_frame, text="Xóa ảnh", width=80, fg_color="#f44336", hover_color="#da190b", command=self._remove_image)
        self.remove_image_btn.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="nw")
        
        btn_frame_notice = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame_notice.grid(row=7, column=0, columnspan=2, pady=10, padx=5, sticky="w")

        self.notice_add_btn = ctk.CTkButton(btn_frame_notice, text="Thêm", fg_color="#4CAF50", hover_color="#45A049", width=100, command=self._add_notice)
        self.notice_add_btn.pack(side="left", padx=5)
        self.notice_update_btn = ctk.CTkButton(btn_frame_notice, text="Cập nhật", fg_color="#2196F3", hover_color="#2f61d6b9", width=100, command=self._update_notice)
        self.notice_update_btn.pack(side="left", padx=5)
        self.notice_delete_btn = ctk.CTkButton(btn_frame_notice, text="Xóa", fg_color="#f44336", hover_color="#da190b", width=100, command=self._delete_notice)
        self.notice_delete_btn.pack(side="left", padx=5)
        self.notice_clear_btn = ctk.CTkButton(btn_frame_notice, text="Làm mới", fg_color="#607D8B", hover_color="#546E7A", width=100, command=self._clear_notice_form)
        self.notice_clear_btn.pack(side="left", padx=5)

        # --- Frame Phải (Bảng Hiển thị) ---
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.grid(row=0, column=1, padx=(2,5), pady=5, sticky="nsew")
        table_frame.grid_rowconfigure(1, weight=1) # Hàng bảng co giãn
        table_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(table_frame, text="Danh sách Thông báo:", font=("Bahnschrift", 16, "bold")).grid(
            row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self._create_notice_table(table_frame) # Gọi hàm tạo bảng

    def _create_notice_table(self, parent_frame):
        # (Giữ nguyên)
        table_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
        table_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        notice_cols = ("id", "tieu_de", "ngay_dang", "co_anh")
        self.notice_table = ttk.Treeview(table_container, columns=notice_cols, show="headings")
        self.notice_table.grid(row=0, column=0, sticky="nsew")
        self.notice_table.heading("id", text="ID"); self.notice_table.heading("tieu_de", text="Tiêu đề"); self.notice_table.heading("ngay_dang", text="Ngày đăng"); self.notice_table.heading("co_anh", text="Hình ảnh")
        self.notice_table.column("id", width=50, anchor="center", stretch=False); self.notice_table.column("tieu_de", width=300, anchor="w"); self.notice_table.column("ngay_dang", width=150, anchor="center"); self.notice_table.column("co_anh", width=80, anchor="center", stretch=False)
        notice_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.notice_table.yview); notice_scrollbar.grid(row=0, column=1, sticky="ns"); self.notice_table.configure(yscrollcommand=notice_scrollbar.set)
        self.notice_table.bind("<<TreeviewSelect>>", self._select_notice_tree)


    # ... (_load_notice_data, _clear_notice_table giữ nguyên) ...
    def _load_notice_data(self):
        """Tải dữ liệu thông báo lên Treeview."""
        self._clear_notice_table()
        try:
            self.notice_image_blobs = {} 
            notice_data = db.get_all_thongbao() 
            if notice_data:
                for notice in notice_data:
                    notice_id, tieu_de, noi_dung, ngay_dang_obj, image_blob = notice
                    ngay_dang_formatted = ngay_dang_obj.strftime('%d/%m/%Y %H:%M') if ngay_dang_obj else ''
                    co_anh_text = "[Ảnh]" if image_blob else ""
                    self.notice_image_blobs[notice_id] = {'blob': image_blob, 'content': noi_dung}
                    self.notice_table.insert("", "end", iid=notice_id, values=(notice_id, tieu_de, ngay_dang_formatted, co_anh_text))
        except Error as e: messagebox.showerror("Lỗi tải Thông báo", f"Lỗi CSDL: {e}", parent=self)
        except Exception as e: messagebox.showerror("Lỗi tải Thông báo", f"Lỗi không xác định: {e}", parent=self)

    def _clear_notice_table(self):
        """Xóa dữ liệu trong bảng thông báo."""
        for item in self.notice_table.get_children(): self.notice_table.delete(item)
        self.notice_image_blobs = {} 
        
    # --- THAY THẾ HÀM NÀY ---
    def _remove_image(self):
        """Xóa ảnh đang preview và đảm bảo cập nhật UI."""
        self.current_image_pil = None
        self.current_image_blob = None
        self.current_ctk_image = None # <<< Xóa tham chiếu CTkImage
        if self.image_preview_label and self.image_preview_label.winfo_exists():
            try:
                # Quan trọng: Configure trước khi gọi update_idletasks
                self.image_preview_label.configure(image=None, text="Chưa có ảnh")
                # Không cần gán self.image_preview_label.image = None nữa
                self.update_idletasks() # <<< Ép Tkinter cập nhật ngay
            except tk.TclError as e:
                 print(f"Lỗi khi cấu hình label trong _remove_image: {e}")

    # --- THAY THẾ HÀM NÀY ---
    def _display_image_preview(self, image_source):
        """Hiển thị ảnh (từ PIL hoặc BLOB) lên label preview."""
        if not hasattr(self, 'image_preview_label') or not self.image_preview_label or not self.image_preview_label.winfo_exists():
            print("Warning: image_preview_label không tồn tại hoặc chưa được khởi tạo.")
            return

        img_to_display_pil = None
        new_ctk_image = None # Tạo biến cục bộ cho CTkImage mới

        try:
            if isinstance(image_source, Image.Image):
                img_to_display_pil = image_source
            elif isinstance(image_source, bytes) and image_source:
                try:
                    img_to_display_pil = Image.open(BytesIO(image_source))
                except Exception as e:
                    print(f"Lỗi khi mở ảnh từ BLOB để preview: {e}. Hiển thị ảnh rỗng.")
                    img_to_display_pil = None # Đặt về None để không hiển thị ảnh lỗi
            else:
                self._remove_image()
                return

            if img_to_display_pil:
                preview_height = 150
                if img_to_display_pil.height == 0: raise ValueError("Chiều cao ảnh bằng 0.")
                ratio = preview_height / img_to_display_pil.height
                preview_width = int(img_to_display_pil.width * ratio)
                if preview_width <= 0: preview_width = 1

                img_copy = img_to_display_pil.copy()
                
                # Tạo CTkImage mới
                new_ctk_image = ImageProcessor(img_copy).resize(preview_width, preview_height).to_ctkimage()

                # <<< LƯU THAM CHIẾU VÀO self.current_ctk_image TRƯỚC >>>
                self.current_ctk_image = new_ctk_image 

                # Sau đó mới configure label
                self.image_preview_label.configure(image=self.current_ctk_image, text="")
                # Không cần gán self.image_preview_label.image nữa
                
                self.current_image_pil = img_to_display_pil # Lưu PIL gốc để convert lại nếu cần
            else:
                self._remove_image()

        except Exception as e:
             messagebox.showerror("Lỗi Hiển Thị Ảnh", f"Lỗi khi tạo ảnh preview: {e}", parent=self)
             self._remove_image()

    # ... (_select_notice_tree, _clear_notice_form, _select_image, _convert_pil_to_blob, _add_notice, _update_notice, _delete_notice giữ nguyên) ...
    def _select_notice_tree(self, event=None):
        """Hiển thị thông tin thông báo đã chọn lên form."""
        selected_item_id = self.notice_table.focus() 
        if not selected_item_id:
            self.selected_notice_id = None
            return

        try:
            self.selected_notice_id = int(selected_item_id)
            item_values = self.notice_table.item(selected_item_id, "values")
            tieu_de = item_values[1]
            cached_data = self.notice_image_blobs.get(self.selected_notice_id)
            noi_dung = cached_data['content'] if cached_data else ""
            image_blob = cached_data['blob'] if cached_data else None
            self.current_image_blob = image_blob 

            self.notice_title_entry.delete(0, "end"); self.notice_title_entry.insert(0, tieu_de)
            self.notice_content_textbox.delete("1.0", "end"); self.notice_content_textbox.insert("1.0", noi_dung)
            self._display_image_preview(image_blob) # <<< Gọi hàm đã sửa
            
        except (ValueError, IndexError, KeyError) as e:
            messagebox.showerror("Lỗi", f"Dữ liệu thông báo không hợp lệ: {e}", parent=self)
            self._clear_notice_form()
        except Exception as e:
            messagebox.showerror("Lỗi Hiển Thị Chi Tiết TB", f"Lỗi không xác định: {e}", parent=self)
            self._clear_notice_form()

    def _clear_notice_form(self):
        """Xóa trắng form quản lý thông báo."""
        self.selected_notice_id = None
        self.notice_title_entry.delete(0, "end")
        self.notice_content_textbox.delete("1.0", "end")
        self._remove_image() # <<< Gọi hàm _remove_image đã sửa
        
        if self.notice_table.focus():
            self.notice_table.selection_remove(self.notice_table.focus())

    def _select_image(self):
        """Mở dialog chọn file ảnh và hiển thị preview."""
        file_path = filedialog.askopenfilename(
            title="Chọn hình ảnh",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            try:
                self.current_image_pil = Image.open(file_path)
                self._display_image_preview(self.current_image_pil) # <<< Gọi hàm đã sửa
                self.current_image_blob = None 
            except Exception as e:
                messagebox.showerror("Lỗi Mở Ảnh", f"Không thể mở hoặc xử lý file ảnh:\n{e}", parent=self)
                self.current_image_pil = None
                self._remove_image() 

    def _convert_pil_to_blob(self, pil_image):
        """Chuyển đổi ảnh PIL sang dạng BLOB (bytes) để lưu vào DB."""
        if not pil_image: return None
        try:
            if pil_image.mode == 'RGBA': pil_image = pil_image.convert('RGB')
            img_byte_arr = BytesIO()
            # Ưu tiên PNG nếu ảnh có độ trong suốt (dù đã convert), nếu không thì JPG
            img_format = 'PNG' if 'A' in pil_image.mode else 'JPEG'
            pil_image.save(img_byte_arr, format=img_format, quality=85 if img_format=='JPEG' else None) 
            return img_byte_arr.getvalue()
        except Exception as e: print(f"Lỗi chuyển đổi PIL sang BLOB: {e}"); return None

    def _add_notice(self):
        # (Giữ nguyên)
        try:
            tieu_de = self.notice_title_entry.get().strip(); noi_dung = self.notice_content_textbox.get("1.0", "end-1c").strip()
            if not tieu_de or not noi_dung: messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Tiêu đề và Nội dung."); return
            image_blob = self._convert_pil_to_blob(self.current_image_pil)
            if db.add_thongbao(tieu_de, noi_dung, image_blob): 
                 messagebox.showinfo("Thành công", f"Thêm thông báo '{tieu_de}' thành công."); self._clear_notice_form(); self._load_notice_data()
            else: messagebox.showerror("Lỗi", "Thêm thông báo thất bại.")
        except Error as e: messagebox.showerror("Lỗi CSDL", f"Lỗi khi thêm thông báo: {e}", parent=self)
        except Exception as e: messagebox.showerror("Lỗi", f"Lỗi không xác định khi thêm thông báo: {e}", parent=self)

    def _update_notice(self):
        # (Giữ nguyên)
        if not self.selected_notice_id: messagebox.showwarning("Chưa chọn", "Vui lòng chọn thông báo từ bảng để cập nhật."); return
        try:
            notice_id = self.selected_notice_id; tieu_de = self.notice_title_entry.get().strip(); noi_dung = self.notice_content_textbox.get("1.0", "end-1c").strip()
            if not tieu_de or not noi_dung: messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Tiêu đề và Nội dung."); return
            final_image_blob = None
            if self.current_image_pil: final_image_blob = self._convert_pil_to_blob(self.current_image_pil)
            elif self.current_image_blob: final_image_blob = self.current_image_blob
            if db.update_thongbao(notice_id, tieu_de, noi_dung, final_image_blob): 
                 messagebox.showinfo("Thành công", f"Cập nhật thông báo (ID: {notice_id}) thành công."); self._clear_notice_form(); self._load_notice_data()
            else: messagebox.showerror("Lỗi", "Cập nhật thông báo thất bại.")
        except Error as e: messagebox.showerror("Lỗi CSDL", f"Lỗi khi cập nhật thông báo: {e}", parent=self)
        except Exception as e: messagebox.showerror("Lỗi", f"Lỗi không xác định khi cập nhật thông báo: {e}", parent=self)

    def _delete_notice(self):
        # (Giữ nguyên)
        if not self.selected_notice_id: messagebox.showwarning("Chưa chọn", "Vui lòng chọn thông báo từ bảng để xóa."); return
        notice_id = self.selected_notice_id; tieu_de = self.notice_title_entry.get() 
        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa thông báo:\n'{tieu_de}' (ID: {notice_id})?", icon='warning', parent=self):
            try:
                if db.delete_thongbao(notice_id): 
                    messagebox.showinfo("Thành công", f"Xóa thông báo (ID: {notice_id}) thành công."); self._clear_notice_form(); self._load_notice_data()
                else: messagebox.showerror("Lỗi", "Xóa thông báo thất bại.")
            except Error as e: messagebox.showerror("Lỗi CSDL", f"Lỗi khi xóa thông báo: {e}", parent=self)
            except Exception as e: messagebox.showerror("Lỗi", f"Lỗi không xác định khi xóa thông báo: {e}", parent=self)