# FILE NAME: controller.py

import core.database as Db
from app_face_recognition.face_recognition_model import FaceRecognitionModel


class MainController:
    def __init__(self, model_path, sounds_path, liveness_model_path):
        self.db = Db
        self.face_model = FaceRecognitionModel(sounds_path=sounds_path, model_path=model_path, liveness_model_path=liveness_model_path)
        self.is_attendance_running = False
        self.current_ma_buoi_hoc = None
        self.total_students_in_class = 0

    # -----------------------------
    # Quản lý điểm danh
    # -----------------------------
    def start_attendance(self, ma_buoi_hoc, ma_lop):
        if self.is_attendance_running:
            return "Đã có một quá trình điểm danh đang chạy."

        self.is_attendance_running = True
        self.current_ma_buoi_hoc = ma_buoi_hoc
        self.face_model.recognized_students = set()
        self.face_model.track_data = {}

        self.total_students_in_class = self.db.get_total_students_by_class(ma_lop)
        return "Bắt đầu điểm danh."

    def stop_attendance(self):
        self.is_attendance_running = False
        self.current_ma_buoi_hoc = None
        self.face_model.stop()   
        return "⏹ Đã dừng điểm danh."

    # -----------------------------
    # Xử lý khung hình
    # -----------------------------
    def process_frame(self, frame, mode='multi_person'):
        if not self.is_attendance_running or self.face_model.executor is None:
            return frame, [], 0, 0
        
        if not self.is_attendance_running:
            return frame, [], 0, 0

        processed_frame, recognized, present_count = self.face_model.process_frame(
            frame,
            ma_buoi_hoc=self.current_ma_buoi_hoc,
            mode=mode
        )
        return processed_frame, recognized, self.total_students_in_class, present_count

    # -----------------------------
    # Training
    # -----------------------------
    def start_training(self, student_id, frame_generator, mode):
        return self.face_model.train_face(student_id, frame_generator, mode)

    # -----------------------------
    # Thông tin CSDL
    # -----------------------------
    def get_student_info(self, ma_sv):
        return self.db.get_student_by_id(ma_sv)

    def get_classes_of_lecturer(self, username):
        return self.db.get_classes_of_lecturer(username)
