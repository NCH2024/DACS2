import os
import cv2
import numpy as np
import threading
import pygame
from ultralytics import YOLO 
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model
from app_face_recognition.liveness_antispoof import LivenessAntiSpoof
import time
import shutil
import core.database as Db 
import torch
import concurrent.futures
import collections


class FaceRecognitionModel:
    def __init__(self, sounds_path, model_path):
        self.db = Db
        self.sounds_path = sounds_path
        self.model_path = model_path
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # Tải các mô hình cần thiết
        self.check_and_download_models()
        self.yolo_model = YOLO(os.path.join(self.model_path, "yolov8s.pt"))
        self.face_model = FaceAnalysis(
            name='buffalo_l',
            root=self.model_path,
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
        )
        self.face_model.prepare(ctx_id=0, det_size=(640, 640))
        self.liveness_model = LivenessAntiSpoof(
            model_path=os.path.join(self.model_path, "AntiSpoofing_bin_1.5_128 (2).onnx"),
            device=self.device
        )
        self.known_face_encodings, self.known_face_student_ids = Db.load_face_encodings()
        print(f"Đã tải {len(self.known_face_encodings)} embeddings từ CSDL.")

        # Khởi tạo các biến trạng thái
        self.recognized_students = set()
        self.track_data = {}  # Lưu trữ thông tin của từng track_id
        self.frame_count = 0

        # Âm thanh
        pygame.mixer.init()
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        self.sound_success = os.path.join(base_dir, "..", "resources", "sound", "success.wav")
        self.sound_fail = os.path.join(base_dir, "..", "resources", "sound", "fail.wav")

        # Executor cho xử lý đa luồng (InsightFace & AntiSpoof)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count())

    # ===========================
    # KIỂM TRA + TẢI MODEL
    # ===========================
    def check_and_download_models(self):
        os.makedirs(self.model_path, exist_ok=True)

        # =======================
        # 1. YOLOv8s
        # =======================
        yolo_path = os.path.join(self.model_path, "yolov8s.pt")
        if not os.path.exists(yolo_path):
            print("Không tìm thấy YOLOv8s, đang tải về...")
            YOLO("yolov8s.pt")  # Ultralytics sẽ tự tải xuống
            default_yolo = os.path.expanduser("~/.cache/torch/hub/ultralytics_yolov8")
            # copy file .pt về dự án
            for root, dirs, files in os.walk(default_yolo):
                for f in files:
                    if f.endswith("yolov8s.pt"):
                        shutil.copy(os.path.join(root, f), yolo_path)
                        print("Đã tải YOLOv8s cho ứng dụng")
                        break

        # =======================
        # 2. InsightFace buffalo_l
        # =======================
        insightface_dir = os.path.join(self.model_path, "buffalo_l")
        if not os.path.exists(insightface_dir):
            print("Không tìm thấy InsightFace, đang tải về...")
            try:
                # Lệnh này sẽ tải về ~/.insightface/models/buffalo_l
                _ = get_model("buffalo_l")
                default_dir = os.path.expanduser("~/.insightface/models/buffalo_l")
                
                # Sau đó sao chép từ cache vào thư mục của bạn
                if os.path.exists(default_dir):
                    shutil.copytree(default_dir, insightface_dir)
                    print("Đã tải InsightFace và sao chép thành công")
            except Exception as e:
                print(f"Lỗi khi tải InsightFace: {e}")
                print(f"Vui lòng tải thủ công và giải nén vào thư mục: {insightface_dir}")

        

    # ===========================
    # ÂM THANH
    # ===========================
    def play_sound(self, sound_type):
        sound_file = self.sound_success if sound_type == "success" else self.sound_fail
        threading.Thread(
            target=lambda: (pygame.mixer.music.load(sound_file), pygame.mixer.music.play()),
            daemon=True
        ).start()

    # ===========================
    # TÌM SINH VIÊN
    # ===========================
    def find_best_match(self, new_embedding):
        similarities = np.dot(self.known_face_encodings, new_embedding) / (
            np.linalg.norm(self.known_face_encodings, axis=1) * np.linalg.norm(new_embedding) + 1e-6
        )
        best_idx = np.argmax(similarities)
        return self.known_face_student_ids[best_idx], similarities[best_idx]


    def _update_track_info(self, track_id, info):
        # Hàm nội bộ để cập nhật trạng thái của một track
        self.track_data.setdefault(track_id, {}).update(info)

    def _process_one_person(self, frame, ma_buoi_hoc, so_sinh_vien_trong_lop):
        # Chế độ nhận dạng 1 người: chỉ xử lý người có bbox lớn nhất
        largest_box = None
        max_area = 0
        results = self.yolo_model.track(frame, classes=0, persist=True, verbose=False, device=self.device)
        if not results:
            return frame, [], so_sinh_vien_trong_lop, len(self.recognized_students)

        # Tìm box lớn nhất
        for box in results[0].boxes:
            if box.id is None: continue
            area = (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])
            if area > max_area:
                max_area = area
                largest_box = box

        if not largest_box:
            return frame, [], so_sinh_vien_trong_lop, len(self.recognized_students)

        # Xử lý riêng cho box lớn nhất
        track_id = int(largest_box.id[0])
        x1, y1, x2, y2 = largest_box.xyxy.cpu().numpy().astype(int)[0]
        
        _, recognized_students_frame = self._process_single_box(frame, x1, y1, x2, y2, track_id, ma_buoi_hoc)
        
        # Tạo bản sao của khung hình để vẽ
        processed_frame = frame.copy()
        
        # Vẽ thông tin của track đang được xử lý
        info = self.track_data.get(track_id)
        if info and info.get('face_bbox'):
            label = info.get('label', 'Processing...')
            color = info.get('color', (255, 255, 0))
            x_face, y_face, w_face, h_face = info['face_bbox']
            cv2.rectangle(processed_frame, (x_face, y_face), (w_face, h_face), color, 1)
            cv2.putText(processed_frame, label, (x_face, y_face - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        return processed_frame, recognized_students_frame, so_sinh_vien_trong_lop, len(self.recognized_students)

    def _process_multi_person(self, frame, ma_buoi_hoc, so_sinh_vien_trong_lop):
        # Chế độ nhận dạng nhiều người: xử lý tất cả mọi người được phát hiện
        recognized_students_frame = []
        
        results = self.yolo_model.track(frame, classes=0, persist=True, verbose=False, device=self.device)
        if not results:
            return frame, [], so_sinh_vien_trong_lop, len(self.recognized_students)

        current_track_ids = {int(box.id[0]) for result in results for box in result.boxes if box.id is not None}
        # Xóa tất cả các track ID không còn trong khung hình hiện tại để tránh "khung ma"
        expired_ids = [tid for tid in self.track_data if tid not in current_track_ids]
        for tid in expired_ids:
            del self.track_data[tid]
            
        for result in results:
            for box in result.boxes:
                if box.id is None: continue
                track_id = int(box.id[0])
                x1, y1, x2, y2 = box.xyxy.cpu().numpy().astype(int)[0]
                
                _, newly_recognized = self._process_single_box(frame, x1, y1, x2, y2, track_id, ma_buoi_hoc)
                recognized_students_frame.extend(newly_recognized)
        
        processed_frame = frame.copy()
        # Vẽ lên khung hình dựa trên dữ liệu đã được xử lý
        for track_id, info in self.track_data.items():
            if info.get('face_bbox'):
                label = info.get('label', 'Processing...')
                color = info.get('color', (255, 255, 0))
                x_face, y_face, w_face, h_face = info['face_bbox']
                cv2.rectangle(processed_frame, (x_face, y_face), (w_face, h_face), color, 1)
                cv2.putText(processed_frame, label, (x_face, y_face - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        return processed_frame, recognized_students_frame, so_sinh_vien_trong_lop, len(self.recognized_students)

    def _process_single_box(self, frame, x1, y1, x2, y2, track_id, ma_buoi_hoc):
        # Hàm phụ trợ để xử lý một hộp giới hạn duy nhất
        track_info = self.track_data.get(track_id, {})
        
        # Nếu track đã được xử lý xong (có nhãn cuối cùng), không cần làm gì thêm
        if track_info.get('finalized', False):
            return frame, [] # Không có sinh viên mới nào được nhận dạng

        # Bước 1: Lấy kết quả Liveness nếu có
        is_live = self.liveness_model.get_result(track_id)

        if is_live:
            tid, live_flag = is_live
            if live_flag is False:
                # Nếu là FAKE, cập nhật trạng thái và kết thúc
                self._update_track_info(tid, {'label': "FAKE", 'color': (0, 0, 255), 'finalized': True})
                return frame, []
            elif live_flag is True:
                # Nếu là REAL, tiến hành nhận dạng
                face = track_info.get('face_object')
                if face:
                    embedding = face.embedding
                    best_match_id, similarity = self.find_best_match(embedding)
                    
                    if similarity > 0.5:
                        label = f"MSV: {best_match_id}"
                        color = (0, 255, 0)
                        newly_recognized = []
                        if best_match_id not in self.recognized_students:
                            self.recognized_students.add(best_match_id)
                            self.db.record_attendance(best_match_id, ma_buoi_hoc, "CM")
                            newly_recognized = [best_match_id]
                        self._update_track_info(tid, {'label': label, 'color': color, 'finalized': True})
                        return frame, newly_recognized
                    else:
                        label = "Unknown person"
                        color = (128, 0, 255)
                        self._update_track_info(tid, {'label': label, 'color': color, 'finalized': True})
                        return frame, []
        
        # Bước 2: Nếu chưa có kết quả liveness hoặc chưa bắt đầu, thì tiến hành phát hiện khuôn mặt
        if not track_info.get('liveness_submitted'):
            person_crop = frame[y1:y2, x1:x2]
            faces = self.face_model.get(person_crop)
            
            if faces and len(faces) == 1:
                face = faces[0]
                face_crop = person_crop[int(face.bbox[1]):int(face.bbox[3]), int(face.bbox[0]):int(face.bbox[2])]
                face_bbox = (int(face.bbox[0]) + x1, int(face.bbox[1]) + y1, int(face.bbox[2]) + x1, int(face.bbox[3]) + y1)

                # Cập nhật thông tin và gửi đi kiểm tra liveness
                self._update_track_info(track_id, {
                    'face_bbox': face_bbox, 
                    'label': 'Processing...', 
                    'color': (255, 255, 0),
                    'liveness_submitted': True,
                    'face_object': face # Lưu lại đối tượng face để dùng sau
                })
                self.liveness_model.submit(track_id, face_crop)

        return frame, [] # Mặc định không có sinh viên mới

    def process_frame(self, frame, ma_buoi_hoc, so_sinh_vien_trong_lop, mode='multi_person'):
        self.frame_count += 1
        
        if mode == 'one_person':
            return self._process_one_person(frame, ma_buoi_hoc, so_sinh_vien_trong_lop)
        elif mode == 'multi_person':
            return self._process_multi_person(frame, ma_buoi_hoc, so_sinh_vien_trong_lop)
        else:
            raise ValueError("Chế độ không hợp lệ. Vui lòng chọn 'one_person' hoặc 'multi_person'.")

    # ===========================
    # TRAINING KHUÔN MẶT
    # ===========================
    def train_face(self, student_id, frame_generator, mode="quick"):
        """
        Đào tạo dữ liệu khuôn mặt cho một sinh viên.
        
        Args:
            student_id: Mã số sinh viên (int).
            frame_generator: Iterator cung cấp các khung hình từ camera.
            mode: "deep" (50 ảnh) hoặc "quick" (10 ảnh).
        """
        if getattr(self, "is_training_in_progress", False):
            print("Một tiến trình train đang chạy. Vui lòng thử lại sau.")
            return False, "training_in_progress"
        # if self.first_open:
        #     time.sleep(3)
        #     self.first_open = False

        self.is_training_in_progress = True
        num_images_needed = 50 if mode == "deep" else 10
        collected_embeddings = []
        avatar_frame = None
        count = 0

        try:
            for frame in frame_generator:
                if count >= num_images_needed:
                    break

                faces = self.face_model.get(frame)
                if faces and len(faces) == 1:
                    face = faces[0]
                    embedding = face.embedding
                    collected_embeddings.append(embedding)

                    # Chọn avatar ở giữa tiến trình
                    if avatar_frame is None and count == num_images_needed // 2:
                        x1, y1, x2, y2 = face.bbox.astype(int)
                        x1 = max(0, x1)
                        y1 = max(0, y1)
                        x2 = min(frame.shape[1], x2)
                        y2 = min(frame.shape[0], y2)
                        avatar_frame = frame[y1:y2, x1:x2]

                    count += 1
                    yield count, num_images_needed  # báo tiến độ về giao diện

        except Exception as e:
            print(f"❌ Lỗi trong quá trình training: {e}")
            self.is_training_in_progress = False
            yield -1, f"error: {e}"
            return

        self.is_training_in_progress = False

        if count >= num_images_needed and avatar_frame is not None:
            mean_embedding = np.mean(collected_embeddings, axis=0)

            success = self.save_face_data(int(student_id), mean_embedding, avatar_frame)

            if success:
                # Reload embeddings
                self.known_face_encodings, self.known_face_student_ids = Db.load_face_encodings()
                yield 100, "success"
            else:
                yield 100, "db_error"
        else:
            yield -1, "not_enough_images"
