from dataclasses import dataclass, asdict
import json
import os

# Đường dẫn file config
CONFIG_PATH = "config.json"

@dataclass
class LoginInfo:
    username: str = None    
    password: str = None

@dataclass
class CameraConfig:
    selected_camera_id: int = None

@dataclass
class AppConfig:
    login_info: LoginInfo
    camera_config: CameraConfig

# Hàm chuyển từ dict -> dataclass
def dict_to_config(data: dict) -> AppConfig:
    return AppConfig(
        login_info=LoginInfo(**data.get("login_info", {})),
        camera_config=CameraConfig(**data.get("camera_config", {}))
    )

# Hàm load config từ file JSON
def load_config() -> AppConfig:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                config = dict_to_config(data)

                if config.login_info.username is None or config.login_info.password is None:
                    config.login_info = LoginInfo()

                return config
        except Exception as e:
            print(f"Lỗi khi load config: {e}")
    return AppConfig(login_info=LoginInfo(), camera_config=CameraConfig())


# Hàm lưu config ra file JSON
def save_config(config: AppConfig):
    with open(CONFIG_PATH, "w") as f:
        json.dump(asdict(config), f, indent=4)