import os
import cv2
import threading
import time
import numpy as np
import concurrent.futures
import torch
import shutil
import pygame
from ultralytics import YOLO
from insightface.app import FaceAnalysis

import core.database as Db
from app_face_recognition.liveness_antispoof import LivenessAntiSpoof


class FaceRecognitionModel:
    """
    Full FaceRecognitionModel integrated with LivenessAntiSpoof (probability-based).
    - process_frame(frame, ma_buoi_hoc=None, mode="multi_person")
      returns (annotated_frame, newly_recognized_list, total_recognized_count)
    """

    def __init__(
        self,
        sounds_path,
        model_path,
        liveness_model_path=None,
        device=None,
        similarity_threshold=0.5,
        frame_skip=5,
    ):
        self.model_path = model_path
        self.sounds_path = sounds_path
        self.device = device or ("cuda:0" if torch.cuda.is_available() else "cpu")
        self.similarity_threshold = float(similarity_threshold)
        self.frame_skip = int(frame_skip)

        # DB
        self.db = Db

        # models
        self._ensure_models()
        self.yolo = YOLO(os.path.join(self.model_path, "yolov8s.pt"))
        self.face_model = FaceAnalysis(
            name="buffalo_l",
            root=self.model_path,
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
        try:
            ctx_id = 0 if "cuda" in str(self.device) else -1
            self.face_model.prepare(ctx_id=ctx_id, det_size=(640, 640))
        except Exception:
            pass

        # liveness (optional)
        self.liveness = None
        if liveness_model_path:
            try:
                self.liveness = LivenessAntiSpoof(liveness_model_path, device=self.device)
            except Exception:
                self.liveness = None

        # known faces
        encs, ids = self.db.load_face_encodings()
        if isinstance(encs, list):
            encs = np.array(encs)
        if encs is None:
            encs = np.zeros((0, 512), dtype=np.float32)
            ids = []
        self.known_face_encodings = encs
        self.known_face_ids = ids

        # runtime state
        self.recognized_students = set()
        self.track_data = {}  # track_id -> info dict
        self.lock = threading.Lock()

        # executor
        self._create_executor()

        # sounds
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.sound_success = os.path.join(self.sounds_path, "success.wav")
        self.sound_fail = os.path.join(self.sounds_path, "fail.wav")

    # ---------------- helpers ----------------
    def _ensure_models(self):
        os.makedirs(self.model_path, exist_ok=True)
        yolo_path = os.path.join(self.model_path, "yolov8s.pt")
        if not os.path.exists(yolo_path):
            YOLO("yolov8s.pt")
            cache_dir = os.path.expanduser("~/.cache/torch/hub/ultralytics_yolov8")
            for root, _, files in os.walk(cache_dir):
                for f in files:
                    if f.endswith("yolov8s.pt"):
                        try:
                            shutil.copy(os.path.join(root, f), yolo_path)
                        except Exception:
                            pass
                        break

    def _create_executor(self):
        try:
            if getattr(self, "executor", None) is None or getattr(self.executor, "_shutdown", False):
                self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 2)
                self.processing_futures = {}
        except Exception:
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
            self.processing_futures = {}

    def _safe_play_sound(self, kind="success"):
        file = self.sound_success if kind == "success" else self.sound_fail
        try:
            if os.path.exists(file):
                threading.Thread(target=lambda: (pygame.mixer.music.load(file), pygame.mixer.music.play()), daemon=True).start()
        except Exception:
            pass

    def _find_best_match(self, embedding):
        if self.known_face_encodings.shape[0] == 0:
            return None, 0.0
        denom = (np.linalg.norm(self.known_face_encodings, axis=1) * (np.linalg.norm(embedding) + 1e-8)) + 1e-12
        sims = np.dot(self.known_face_encodings, embedding) / denom
        idx = int(np.argmax(sims))
        return self.known_face_ids[idx], float(sims[idx])

    def reload_known_faces(self):
        encs, ids = self.db.load_face_encodings()
        if isinstance(encs, list):
            encs = np.array(encs)
        if encs is None:
            encs = np.zeros((0, 512), dtype=np.float32)
            ids = []
        with self.lock:
            self.known_face_encodings = encs
            self.known_face_ids = ids

    # ---------------- lifecycle ----------------
    def stop(self):
        # cancel pending futures
        for f in list(getattr(self, "processing_futures", {}).values()):
            try:
                f.cancel()
            except Exception:
                pass

        # shutdown executor
        try:
            if getattr(self, "executor", None):
                self.executor.shutdown(wait=False)
        except Exception:
            pass

        with self.lock:
            self.track_data.clear()
            self.recognized_students.clear()
            self.processing_futures = {}

        # recreate executor for next start
        try:
            self._create_executor()
        except Exception:
            pass

    # ---------------- public ----------------
    def process_frame(self, frame, ma_buoi_hoc=None, mode="multi_person"):
        self._create_executor()
        if mode == "one_person":
            return self.process_frame_one_person(frame, ma_buoi_hoc)
        else:
            return self.process_frame_multi_person(frame, ma_buoi_hoc)

    def process_frame_one_person(self, frame, ma_buoi_hoc=None):
        return self._generic_process(frame, ma_buoi_hoc, single=True)

    def process_frame_multi_person(self, frame, ma_buoi_hoc=None):
        return self._generic_process(frame, ma_buoi_hoc, single=False)

    # ---------------- core pipeline ----------------
    def _generic_process(self, frame, ma_buoi_hoc, single=False):
        results = self.yolo.track(frame, classes=0, persist=True, verbose=False, device=self.device)
        boxes = results[0].boxes if results and results[0].boxes is not None else []

        # collect current ids
        current_ids = set()
        for b in boxes:
            if b.id is None:
                continue
            try:
                current_ids.add(int(b.id[0]))
            except Exception:
                pass

        # cleanup tracks left frame
        with self.lock:
            for tid in list(self.track_data.keys()):
                if tid not in current_ids:
                    fut = self.processing_futures.pop(tid, None)
                    if fut:
                        try:
                            fut.cancel()
                        except Exception:
                            pass
                    self.track_data.pop(tid, None)

        # select targets
        if single and boxes:
            largest = max(boxes, key=lambda b: ((b.xyxy[0][2] - b.xyxy[0][0]) * (b.xyxy[0][3] - b.xyxy[0][1])))
            target_boxes = [largest] if largest.id is not None else []
        else:
            target_boxes = [b for b in boxes if b.id is not None]

        h, w = frame.shape[:2]
        for b in target_boxes:
            try:
                tid = int(b.id[0])
            except Exception:
                continue
            xy = b.xyxy.cpu().numpy().astype(int)[0]
            x1, y1, x2, y2 = xy
            with self.lock:
                info = self.track_data.setdefault(
                    tid,
                    {"frame_count": 0, "label": "Detecting...", "face_bbox": None, "color": (255, 255, 0), "newly_recognized": False, "person_bbox": (x1, y1, x2, y2)},
                )
                info["person_bbox"] = (x1, y1, x2, y2)
                info["frame_count"] += 1
                submit_now = (info["frame_count"] % self.frame_skip == 0)

            if submit_now:
                cx1, cy1 = max(0, x1), max(0, y1)
                cx2, cy2 = min(w, x2), min(h, y2)
                crop = frame[cy1:cy2, cx1:cx2]
                if getattr(self, "executor", None) is not None:
                    fut = self.processing_futures.get(tid)
                    if fut is None or fut.done():
                        try:
                            self.processing_futures[tid] = self.executor.submit(self._recognize_worker, tid, crop.copy(), (cx1, cy1, cx2, cy2), ma_buoi_hoc, single)
                        except RuntimeError:
                            pass

        # collect finished futures
        for tid, fut in list(self.processing_futures.items()):
            if fut.done():
                try:
                    res = fut.result()
                    if res:
                        with self.lock:
                            self.track_data[tid].update(res)
                except Exception:
                    pass
                finally:
                    self.processing_futures.pop(tid, None)

        # draw frame: draw person box (no text) and draw face box + label only if available
        out = frame.copy()
        newly_ids = []
        with self.lock:
            for tid, info in self.track_data.items():
                px1, py1, px2, py2 = info.get("person_bbox", (0, 0, 0, 0))
                cv2.rectangle(out, (px1, py1), (px2, py2), (100, 100, 100), 1)
                label = info.get("label", "Detecting...")
                color = info.get("color", (255, 255, 0))
                fb = info.get("face_bbox")
                if fb:
                    fx1, fy1, fx2, fy2 = fb
                    cv2.rectangle(out, (fx1, fy1), (fx2, fy2), color, 2)
                    cv2.putText(out, label, (fx1, fy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                if info.get("newly_recognized"):
                    lbl = info.get("label", "")
                    if lbl.startswith("MSV:"):
                        try:
                            sid = int(lbl.split(":", 1)[1].strip())
                            newly_ids.append(sid)
                        except Exception:
                            pass
                    info["newly_recognized"] = False

        return out, newly_ids, len(self.recognized_students)

    # ---------------- recognition worker ----------------
    def _recognize_worker(self, track_id, person_crop, person_bbox_abs, ma_buoi_hoc, single_mode):
        try:
            faces = self.face_model.get(person_crop)
            if not faces:
                return {"label": "NoFace", "color": (128, 128, 128), "face_bbox": None}

            face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))

            fx1 = int(face.bbox[0]) + person_bbox_abs[0]
            fy1 = int(face.bbox[1]) + person_bbox_abs[1]
            fx2 = int(face.bbox[2]) + person_bbox_abs[0]
            fy2 = int(face.bbox[3]) + person_bbox_abs[1]

            bx1, by1, bx2, by2 = (
                max(0, int(face.bbox[0])),
                max(0, int(face.bbox[1])),
                min(person_crop.shape[1], int(face.bbox[2])),
                min(person_crop.shape[0], int(face.bbox[3])),
            )
            face_crop = person_crop[by1:by2, bx1:bx2]
            emb = face.embedding

            # liveness: submit and poll short times for probability
            live_prob = None
            if self.liveness:
                try:
                    self.liveness.submit(track_id, face_crop)
                    for _ in range(4):
                        res = self.liveness.get_result(track_id)
                        if res is not None:
                            live_prob = float(res)
                            break
                        time.sleep(0.03)
                except Exception:
                    live_prob = None

            # interpret probability
            is_live = None
            if live_prob is not None:
                if live_prob >= 0.60:
                    is_live = True
                elif live_prob <= 0.35:
                    is_live = False
                else:
                    is_live = None

            # recognition
            best_id, sim = self._find_best_match(emb)
            if best_id is not None and sim >= self.similarity_threshold:
                newly = False

                if (self.liveness is None) or (is_live is True):
                    with self.lock:
                        if best_id not in self.recognized_students:
                            self.recognized_students.add(best_id)
                            newly = True
                    try:
                        if ma_buoi_hoc is not None:
                            self.db.record_attendance(int(best_id), ma_buoi_hoc, "CM")
                    except Exception:
                        pass
                else:
                    if is_live is False:
                        return {"label": f"FAKE ({live_prob:.2f})", "color": (0, 0, 255), "face_bbox": (fx1, fy1, fx2, fy2)}
                    if is_live is None:
                        return {"label": f"UNCERTAIN ({(live_prob or 0):.2f})", "color": (0, 255, 255), "face_bbox": (fx1, fy1, fx2, fy2)}

                if newly and single_mode:
                    self._safe_play_sound("success")

                return {"label": f"MSV: {best_id}", "color": (0, 255, 0), "face_bbox": (fx1, fy1, fx2, fy2), "newly_recognized": newly}
            else:
                return {"label": "UNKNOWN", "color": (128, 0, 255), "face_bbox": (fx1, fy1, fx2, fy2)}
        except Exception:
            return {"label": "ERR", "color": (0, 0, 255), "face_bbox": None}

    # ---------------- training ----------------
    def train_face(self, student_id, frame_generator, mode="quick"):
        if getattr(self, "is_training_in_progress", False):
            yield -1, "training_in_progress"
            return
        self.is_training_in_progress = True
        try:
            needed = 50 if mode == "deep" else 10
            collected = []
            avatar = None
            i = 0
            for frame in frame_generator:
                if i >= needed:
                    break
                faces = self.face_model.get(frame)
                if faces and len(faces) == 1:
                    face = faces[0]
                    collected.append(face.embedding)
                    if avatar is None and i == needed // 2:
                        x1, y1, x2, y2 = face.bbox.astype(int)
                        x1, y1 = max(0, x1), max(0, y1)
                        x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
                        avatar = frame[y1:y2, x1:x2]
                    i += 1
                    yield i, needed
            if i < needed:
                yield -1, "not_enough_images"
                return
            mean_emb = np.mean(np.stack(collected, axis=0), axis=0)
            ok = False
            try:
                ok = self.db.save_face_data(int(student_id), mean_emb, avatar)
            except Exception:
                ok = False
            if ok:
                self.reload_known_faces()
                yield 100, "success"
            else:
                yield 100, "db_error"
        finally:
            self.is_training_in_progress = False
