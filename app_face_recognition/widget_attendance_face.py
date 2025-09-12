# FILE NAME: widget_attendance_face.py

import customtkinter as ctk
import cv2
from app_face_recognition.camera_setup import CameraManager
from app_face_recognition.widget_camera import WidgetCamera
from gui.utils import *
import datetime
from core.database import *

class WidgetAttendanceFace(ctk.CTkFrame):
    # Xóa _window_instance vì bạn không dùng Toplevel nữa
    # _window_instance = None

    def __init__(self, master=None, controller=None, username=None, ma_buoi_hoc=None, option_attendace=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.username = username
        self.ma_buoi_hoc = ma_buoi_hoc 
        self.option_attendace = option_attendace
        self.camera_manager = CameraManager()
        self.is_camera_open = False
        self.is_processing = False  # Trạng thái vòng lặp xử lý
        self.flip_view = False # Trạng thái lật camera
        
        # Lưu tham chiếu đến frame cha để có thể hủy nó nếu cần
        self.parent_frame = master

        self.widget_color = "#05243F"
        self.text_color = "#2DFCB0"
        self.text_color_w = "#FFFFFF"
        self.configure(fg_color=self.widget_color)

        # Lưới
        # Cột 0: 
        self.grid_columnconfigure(0, weight=0, minsize=500)
        # Cột 1: 
        self.grid_columnconfigure(1, weight=1)
        # Hàng 0: 
        self.grid_rowconfigure(0, weight=0)
        # Hàng 1: 
        self.grid_rowconfigure(1, weight=0, minsize=500)
        # Hàng 2: 
        self.grid_rowconfigure(2, weight=1)

        # Tiêu đề
        self.label_title = LabelCustom(
            self,
            text="ĐIỂM DANH",
            font_size=18,
            font_weight="bold",
            text_color=self.text_color_w
        )
        self.label_title.grid(row=0, column=0, pady=(10,10), padx=(10,0), sticky="nw")
        
        if self.option_attendace == "single":
            self.label_title.set_text(text="ĐIỂM DANH - Chế độ cá nhân")
        elif self.option_attendace == "all":
            self.label_title.set_text(text="ĐIỂM DANH - Chế độ chung")
        else:
            self.label_title.set_text(text="ĐIỂM DANH - Trang đang lỗi vui lòng không điểm danh")
        
        # Thêm nút Đóng để người dùng có thể thoát lớp phủ
        try:
            exit_img = Image.open("resources/images/cross.png")
            self.exit_img = ImageProcessor(exit_img).to_ctkimage()
        except FileNotFoundError:
            self.exit_img = None
        self.close_button = ButtonTheme(self,
                                        text="ESC", 
                                        command=self.on_close, 
                                        fg_color="transparent", 
                                        hover_color="#939393",
                                        font=("Bahnschrift", 18, "bold"),
                                        border_width=0,
                                        width=40,
                                        height=40,
                                        image=self.exit_img
                                        )
        self.close_button.grid(row=0, column=1, pady=10, padx=10, sticky="ne")
        
        # Khung chứa hình ảnh hiển thị từ camera
        self.camera_frame = ctk.CTkFrame(self, fg_color="#1B1B1B")
        self.camera_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.camera_frame.grid_columnconfigure(0, weight=1)
        self.camera_frame.grid_rowconfigure(0, weight=1)
        self.camera_frame.grid_propagate(False)
        
        # Khung chứa các chức năng dưới khung hiển thị hình ảnh
        self.option_frame = ctk.CTkFrame(self, fg_color=self.widget_color)
        self.option_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.option_frame.grid_columnconfigure(0, weight=0)
        self.option_frame.grid_rowconfigure((0,1), weight=0)

        # Khung hiển thị thông tin nhận dạng thời gian thực
        self.info_frame = ctk.CTkFrame(self, fg_color= self.widget_color, border_color=self.text_color, corner_radius=20, border_width=2)
        self.info_frame.grid(row=1, column=1, padx=15, pady=(0,15), rowspan=2, sticky="nsew")
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=0)
        self.info_frame.grid_rowconfigure(1, weight=1)
        
        # Phần nút chức năng và thành phần khung hiển thị
        # hiển thị nội dung khung Option
        self.tittle_option = LabelCustom(
            self.option_frame,
            text="Tùy chọn",
            font_size=16,
            font_weight="bold",
            text_color=self.text_color_w
        )
        self.tittle_option.grid(row=0, column=0, padx=(5,0), pady=(10,0), sticky="nw")

        self.switch_frame_option = ctk.CTkFrame(self.option_frame, 
                                                fg_color=self.widget_color, 
                                                corner_radius=10,
                                                border_color=self.text_color_w,
                                                border_width=2)
        self.switch_frame_option.grid(row=1, column=0, padx=10, pady=10, sticky="nsew") 
        self.switch_frame_option.grid_columnconfigure(0, weight=0)
        self.switch_frame_option.grid_rowconfigure(0, weight=0)

        self.switch_flipCamera = SwitchOption(
            self.switch_frame_option,
            text="Lật Camera (lật hình ảnh camera dành cho Camera selfie)",
            wraplenght=400,
            text_color=self.text_color_w,
            initial=False,
            font=("Bahnschrift", 14, "bold"),
            command=self.toggle_camera_flip
        )
        self.switch_flipCamera.grid(row=0, column=0, padx=10, pady=5, sticky="we")
        
        self.pause = ButtonTheme(
            self.option_frame,
            text="Tạm dừng",
            command=self.toggle_pause
        )
        self.pause.grid(row=2, column=0, padx=10, pady=10, sticky="we")
        
        # Hiển thị nội dung khung info
        self.tittle_info = LabelCustom(
            self.info_frame,
            text="Thông tin nhận diện",
            font_size=13,
            text_color=self.text_color_w
        )
        self.tittle_info.grid(row=0, column=0, padx=(10,0), pady=(10,0), sticky="nw")  
        
        self.info_content = ctk.CTkScrollableFrame(
            self.info_frame, 
            fg_color=self.widget_color, 
            corner_radius=20
        )
        self.info_content.grid(row=1, column=0, padx=5, pady=(10, 5), sticky="nsew")
         
        
        # Hiển thị hình ảnh camera
        self.camera_widget = WidgetCamera(master=self.camera_frame,
                                          camera_manager=self.camera_manager,
                                          open_as_toplevel=False,
                                          flip_camera=self.switch_flipCamera.get_value())
        self.camera_widget.grid(row=0, column=0, sticky="nsew")
        
        self.note_frame_camera = LabelCustom(
                    self.camera_frame,
                    text="*CAMERA đang được tạm dừng/tắt, Bạn có thể ấn nút bên dưới để tiếp tục!",
                    text_color="#B2B2B2",
                    font_size=13,
                    wraplength=500
                )
        
        self.toggle_camera() 

    #====CÁC HÀM CHỨC NĂNG====#
    def start_processing_loop(self):
        if not self.is_processing or not self.is_camera_open or self.ma_buoi_hoc is None:
            return

        frame = self.camera_manager.get_frame()
        if frame is None:
            self.after(20, self.start_processing_loop)
            return
        
        if self.option_attendace == "single":
            processed_frame, new_students, _, _ = self.controller.process_frame(frame, mode="one_person")
        else:   
            processed_frame, new_students, _, _ = self.controller.process_frame(frame, mode="multi_person")

        if processed_frame is not None:
            if self.flip_view:
                processed_frame = cv2.flip(processed_frame, 1)
            self.camera_widget.set_image(processed_frame)

        if new_students:
            for student_id in new_students:
                self.add_student_to_notification_list(student_id, self.ma_buoi_hoc)

        self.after(20, self.start_processing_loop)
        
    # THÊM HÀM MỚI: Cập nhật danh sách thông báo
    def add_student_to_notification_list(self, student_id, ma_buoi_hoc):
        # Lấy thông tin sinh viên từ CSDL
        record = get_attendace_success(student_id, ma_buoi_hoc)

        if not record:
            return

        student_info = "MSSV: " + str(student_id) + " - Name: " + record[0]
        datetime = record[1]
        avatar_blob = record[2]
        
        pil_image = None
        if avatar_blob:
            try:
                pil_image = Image.open(io.BytesIO(avatar_blob))
            except Exception as e:
                print(f"Lỗi mở ảnh blob của SV {student_id}: {e}")

        card = NotifyCard(
            self.info_content,
            title=student_info,
            text_btn="Đã điểm danh THÀNH CÔNG!",
            ngay_dang= datetime,
            image_pil=pil_image,
            content="",
            height=70,
            width=100
        )
        card.pack(fill="x", padx=5, pady=5)
        card.detail_btn.configure(fg_color="#C3FF00", text_color= "#AC0000")

    
    
    def toggle_camera_flip(self, is_checked=bool):
        self.flip_view = is_checked
        if is_checked:
            self.t = ToastNotification(self, "Đã bật tùy chọn chức năng lật ảnh", duration=2000)
        else:
            self.t = ToastNotification(self, "Đã tắt tùy chọn chức năng lật ảnh", duration=2000)
    
    def toggle_pause(self):
        self.toggle_camera()

    def on_close(self):
        if self.controller:
            try:
                self.controller.stop_attendance()
                self.controller.face_model.is_attendance_running = False
            except Exception:
                pass
        if self.camera_manager:
            self.camera_manager.release_camera()
        self.destroy()

        
        
    def toggle_camera(self):
        if not self.is_camera_open:
            if self.camera_manager.open_camera():
                self.is_camera_open = True
                self.pause.configure(text="Tạm dừng điểm danh")
                self.recreate_camera_widget()
                
                # Bắt đầu vòng lặp xử lý
                self.is_processing = True
                self.start_processing_loop()
            else:
                ToastNotification(master=self, message="Không thể mở camera...", type="error")
        else:
            self.is_camera_open = False
            self.is_processing = False # Dừng vòng lặp
            self.pause.configure(text="Tiếp tục điểm danh")
            self.camera_manager.release_camera()
            
            if self.camera_widget:
                self.camera_widget.destroy()
            
            self.note_frame_camera.grid(row=0, column=0, padx=20, pady=20, sticky="new")

    def recreate_camera_widget(self):
        """Hàm hủy widget camera cũ và tạo lại cái mới với tham số lật ảnh."""
        # Nếu widget camera đã tồn tại, hủy nó đi
        if self.camera_widget:
            self.camera_widget.destroy()
        self.is_processing = False
        # Lấy trạng thái mới nhất từ nút gạt và tạo widget mới
        self.camera_widget = WidgetCamera(master=self.camera_frame,
                                          camera_manager=self.camera_manager,
                                          open_as_toplevel=False,
                                          flip_camera=self.switch_flipCamera.get_value())
        self.camera_widget.grid(row=0, column=0, sticky="nsew")
