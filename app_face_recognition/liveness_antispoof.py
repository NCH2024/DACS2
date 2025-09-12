import numpy as np
import cv2
import onnxruntime as ort
from concurrent.futures import ThreadPoolExecutor
import torch
import os


class LivenessAntiSpoof:
    def __init__(self, model_path, device="cpu"):
        self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.executor = ThreadPoolExecutor(max_workers=torch.cuda.device_count() * 2 or os.cpu_count())
        self.futures = {}
        self.results = {}   # cache kết quả cho mỗi track_id

    def submit(self, track_id, face_bgr):
        """
        Gửi yêu cầu suy luận chống giả mạo cho một luồng xử lý.
        """
        # Hủy bỏ các tác vụ đang chờ nếu có
        if track_id in self.futures and not self.futures[track_id].done():
            self.futures[track_id].cancel()
            
        # Gửi tác vụ mới với cả track_id và face_bgr
        # Đây là dòng cần được sửa đổi
        self.futures[track_id] = self.executor.submit(self.infer_sync, track_id, face_bgr)


    def get_result(self, track_id):
        # Ưu tiên trả về kết quả cache nếu có
        if track_id in self.results:
            return self.results[track_id]

        future = self.futures.get(track_id)
        if future and future.done():
            result = future.result()
            self.results[track_id] = result  # cache lại
            del self.futures[track_id]       # giải phóng future
            return result
        return None

    def preprocess(self, image):
        """
        Tiền xử lý hình ảnh để chuẩn bị cho mô hình.
        Args:
            image (np.array): Hình ảnh khuôn mặt dưới dạng mảng NumPy (BGR).
        Returns:
            np.array: Tensor hình ảnh đã được chuẩn bị cho mô hình.
        """
        # Resize ảnh về kích thước mà mô hình của bạn mong đợi (ví dụ: 128x128)
        if image is None: 
            return None

        img_resized = cv2.resize(image, (128, 128))
        
        # Chuyển đổi từ BGR sang RGB
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Chuyển đổi sang float32
        img_float = img_rgb.astype(np.float32)
        
        # Chuẩn hóa giá trị pixel (từ 0-255 về 0-1)
        img_normalized = img_float / 255.0
        
        # Chuyển đổi định dạng từ HWC (Height, Width, Channel) sang CHW (Channel, Height, Width)
        # và thêm một chiều batch (1, C, H, W)
        img_tensor = np.transpose(img_normalized, (2, 0, 1))[np.newaxis, ...]
        
        return img_tensor

    def infer_sync(self, track_id, face_bgr):
        """
        Hàm thực hiện suy luận một cách đồng bộ.
        """
        if face_bgr is None:
            return (track_id, None)
        try:
            x = self.preprocess(face_bgr)
            ort_inputs = {self.session.get_inputs()[0].name: x}
            ort_outs = self.session.run(None, ort_inputs)
            logits = ort_outs[0][0]

            label = int(np.argmax(logits))
            print(f"Kết quả suy luận cho track {track_id}: {label}")
            if label == 0:
                return (track_id, True)
            elif label == 1:
                return (track_id, False)
            else: 
                return (track_id, None)


        except Exception as e:
            print(f"Lỗi suy luận chống giả mạo cho track {track_id}: {e}")
            return False


