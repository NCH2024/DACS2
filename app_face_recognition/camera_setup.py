# app_face_recognition/camera_setup.py
import cv2
# type: ignore
from pygrabber.dshow_graph import FilterGraph # type: ignore


class CameraManager:
    def __init__(self, camera_id=0):
        """
        Khởi tạo CameraManager với ID camera mặc định là 0.
        """
        self.camera_id = camera_id
        self.camera = None
        self.is_opened = False

    def open_camera(self):
        """
        Mở camera và kiểm tra kết nối.
        """
        try:
            self.camera = cv2.VideoCapture(self.camera_id)
            if not self.camera.isOpened():
                raise Exception(f"Không thể mở camera với ID {self.camera_id}")
            self.is_opened = True
            return True
        except Exception as e:
            print(f"Lỗi khi mở camera: {e}")
            self.is_opened = False
            return False

    def get_frame(self):
        """
        Đọc một khung hình từ camera.
        """
        if not self.is_opened:
            print("Camera chưa được mở.")
            return None
        ret, frame = self.camera.read()
        if not ret:
            print("Không thể đọc khung hình từ camera.")
            return None
        return frame

    def get_camera_info(self):
        """
        Lấy thông tin cơ bản của camera (nếu có).
        """
        if not self.is_opened:
            print("Camera chưa được mở.")
            return None
        try:
            # Lấy các thuộc tính cơ bản
            width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.camera.get(cv2.CAP_PROP_FPS)
            return {
                "id": self.camera_id,
                "resolution": (width, height),
                "fps": fps
            }
        except Exception as e:
            print(f"Lỗi khi lấy thông tin camera: {e}")
            return None

    def release_camera(self):
        """
        Giải phóng camera khi không còn sử dụng.
        """
        if self.camera and self.is_opened:
            self.camera.release()
            self.is_opened = False
            print("Camera đã được giải phóng.")
            
    @staticmethod
    def list_available_cameras():
        """
        Trả về danh sách các tuple (id, name) của các camera đang kết nối với máy tính (Windows only).
        """
        try:
            graph = FilterGraph()
            camera_names = graph.get_input_devices()
            return [(i, name) for i, name in enumerate(camera_names)]
        except Exception as e:
            print(f"Không thể lấy danh sách camera: {e}")
            return []


    def __enter__(self):
        """
        Hỗ trợ sử dụng CameraHandler trong khối 'with'.
        """
        self.open_camera()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Tự động giải phóng camera khi ra khỏi khối 'with'.
        """
        self.release_camera()

# Example usage
if __name__ == '__main__':
    with CameraManager(camera_id=0) as cam_handler:
        cameras = CameraManager.list_available_cameras()
        if cameras:
            print("Danh sách camera đang kết nối:")
            for i, name in enumerate(cameras):
                print(f"{i}: {name}")
        else:
            print("Không tìm thấy camera nào cả 😢")
        if cam_handler.is_opened:
            info = cam_handler.get_camera_info()
            print(f"Thông tin camera: {info}")
            while True:
                frame = cam_handler.get_frame()
                if frame is None:
                    break
                cv2.imshow("Camera Stream", frame)
                
                # Nhấn phím 'q' để thoát
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cv2.destroyAllWindows()
        else:
            print("Không thể mở camera.")

