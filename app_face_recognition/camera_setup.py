# app_face_recognition/camera_setup.py
import cv2
from pygrabber.dshow_graph import FilterGraph 
import time

class CameraManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CameraManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, camera_id=0):
        if not self._initialized:
            self.camera_id = camera_id
            self.camera = None
            self.is_opened = False
            self.capture_thread = None
            self._initialized = True

    def open_camera(self):
        try:
            if not self.is_opened:
                self.camera = cv2.VideoCapture(self.camera_id)
                if not self.camera.isOpened():
                    raise Exception(f"Không thể mở camera với ID {self.camera_id}")
                self.is_opened = True
                print("Camera đã được mở thành công.")
            return True
        except Exception as e:
            print(f"Lỗi khi mở camera: {e}")
            self.is_opened = False
            return False

    def get_frame(self):
        if not self.is_opened or self.camera is None:
            return None
        ret, frame = self.camera.read()
        if not ret:
            # Camera có thể bị ngắt kết nối
            print("Không thể đọc khung hình, camera có thể đã bị ngắt kết nối.")
            self.release_camera()
            return None
        return frame
    
    def get_frame_as_generator(self):
        """
        Tạo một generator để lấy từng khung hình.
        """
        while self.is_opened:
            frame = self.get_frame()
            if frame is None:
                break
            yield frame

    def release_camera(self):
        if self.is_opened and self.camera:
            self.camera.release()
            self.is_opened = False
            self.camera = None
            print("Camera đã được giải phóng.")

    @staticmethod
    def list_available_cameras():
        try:
            graph = FilterGraph()
            camera_names = graph.get_input_devices()
            return [(i, name) for i, name in enumerate(camera_names)]
        except Exception as e:
            print(f"Không thể lấy danh sách camera: {e}")
            return []