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
        self.results = {}   # cache kết quả cho mỗi track_id (live_prob)

    def submit(self, track_id, face_bgr):
        """
        Gửi yêu cầu suy luận chống giả mạo cho một track.
        """
        # Hủy bỏ các tác vụ đang chờ nếu có
        if track_id in self.futures and not self.futures[track_id].done():
            self.futures[track_id].cancel()
            
        # Gửi tác vụ mới
        self.futures[track_id] = self.executor.submit(self.infer_sync, track_id, face_bgr)

    def get_result(self, track_id):
        """
        Lấy kết quả (probability) cho track_id.
        Trả về None nếu chưa có.
        """
        if track_id in self.results:
            return self.results[track_id]

        future = self.futures.get(track_id)
        if future and future.done():
            track_id, prob = future.result()
            if prob is not None:
                self.results[track_id] = prob  # cache lại
            del self.futures[track_id]
            return prob
        return None

    def preprocess(self, image):
        """
        Tiền xử lý hình ảnh để chuẩn bị cho mô hình.
        """
        if image is None:
            return None

        img_resized = cv2.resize(image, (128, 128))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_float = img_rgb.astype(np.float32)
        img_normalized = img_float / 255.0
        img_tensor = np.transpose(img_normalized, (2, 0, 1))[np.newaxis, ...]
        return img_tensor

    def infer_sync(self, track_id, face_bgr):
        """
        Hàm thực hiện suy luận một cách đồng bộ.
        Trả về (track_id, live_prob) với live_prob ∈ [0,1].
        """
        if face_bgr is None:
            return (track_id, None)
        try:
            x = self.preprocess(face_bgr)
            if x is None:
                return (track_id, None)

            ort_inputs = {self.session.get_inputs()[0].name: x}
            ort_outs = self.session.run(None, ort_inputs)
            logits = np.asarray(ort_outs[0][0], dtype=np.float32)
            print(f"Logits cho track {track_id}: {logits}")

            # softmax để lấy xác suất
            exp = np.exp(logits - np.max(logits))
            probs = exp / exp.sum()

            # Giả sử index 0 = live, index 1 = fake
            live_prob = float(probs[0])
            print(f"Xác suất live cho track {track_id}: {live_prob:.4f}")

            return (track_id, live_prob)

        except Exception as e:
            print(f"Lỗi suy luận chống giả mạo cho track {track_id}: {e}")
            return (track_id, None)
