import cv2
import face_recognition
import mediapipe as mp
import numpy as np
import os
import json
import threading
import time
from datetime import datetime

# ── PATHS ────────────────────────────────────────────────────
USERS_DIR = os.path.expanduser("~/.voris/users")
UNKNOWN_DIR = os.path.expanduser("~/.voris/logs/security/unknown_faces")

def ensure_dirs():
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(UNKNOWN_DIR, exist_ok=True)

# ── FACE DATABASE ─────────────────────────────────────────────
def load_known_faces():
    ensure_dirs()
    known_encodings = []
    known_names = []
    known_levels = []
    for fname in os.listdir(USERS_DIR):
        if fname.endswith(".json"):
            path = os.path.join(USERS_DIR, fname)
            with open(path, "r") as f:
                user = json.load(f)
            if "encodings" in user and user["encodings"]:
                for enc in user["encodings"]:
                    known_encodings.append(np.array(enc))
                    known_names.append(user["name"])
                    known_levels.append(user.get("level", 3))
    return known_encodings, known_names, known_levels

def save_user(name, level, encodings):
    ensure_dirs()
    slug = name.lower().replace(" ", "_")
    path = os.path.join(USERS_DIR, f"{slug}.json")
    user = {
        "name": name,
        "level": level,
        "encodings": [e.tolist() for e in encodings],
        "enrolled": datetime.now().isoformat()
    }
    with open(path, "w") as f:
        json.dump(user, f, indent=2)
    return f"User {name} enrolled at level {level}."

def delete_user(name):
    slug = name.lower().replace(" ", "_")
    path = os.path.join(USERS_DIR, f"{slug}.json")
    if os.path.exists(path):
        os.remove(path)
        return f"User {name} removed."
    return f"User {name} not found."

def list_users():
    ensure_dirs()
    users = []
    for fname in os.listdir(USERS_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(USERS_DIR, fname), "r") as f:
                u = json.load(f)
            users.append(f"{u['name']} (Level {u.get('level', 3)})")
    return users if users else ["No users enrolled."]

# ── FACE ENROLLMENT ───────────────────────────────────────────
def enroll_user(name, level=3, camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return None, "Camera not available."
    encodings = []
    angles = ["straight", "slight left", "slight right"]
    print(f"Enrolling {name}. Will capture 3 angles.")
    for i, angle in enumerate(angles):
        print(f"Look {angle} and press SPACE to capture...")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow(f"Enroll - {angle}", frame)
            key = cv2.waitKey(1)
            if key == 32:  # SPACE
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                faces = face_recognition.face_encodings(rgb)
                if faces:
                    encodings.append(faces[0])
                    print(f"Captured angle {i+1}/3")
                    break
                else:
                    print("No face detected. Try again.")
            elif key == 27:  # ESC
                cap.release()
                cv2.destroyAllWindows()
                return None, "Enrollment cancelled."
    cap.release()
    cv2.destroyAllWindows()
    if len(encodings) == 3:
        result = save_user(name, level, encodings)
        return encodings, result
    return None, "Enrollment incomplete."

# ── FACE VERIFICATION ─────────────────────────────────────────
def verify_face(camera_index=0, timeout=15):
    known_encodings, known_names, known_levels = load_known_faces()
    if not known_encodings:
        return None, 0, "No users enrolled."
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return None, 0, "Camera not available."
    start = time.time()
    result_name = None
    result_level = 0
    while time.time() - start < timeout:
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)
        for encoding in encodings:
            distances = face_recognition.face_distance(known_encodings, encoding)
            best_idx = np.argmin(distances)
            if distances[best_idx] < 0.5:
                result_name = known_names[best_idx]
                result_level = known_levels[best_idx]
                cap.release()
                return result_name, result_level, f"Verified: {result_name}"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unknown_path = os.path.join(UNKNOWN_DIR, f"unknown_{timestamp}.jpg")
                cv2.imwrite(unknown_path, frame)
                cap.release()
                return None, 0, f"Unknown face detected. Photo saved."
    cap.release()
    return None, 0, "No face detected."

# ── OBJECT DETECTION WITH MEDIAPIPE ──────────────────────────
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection
mp_pose = mp.solutions.pose

def detect_objects_from_camera(camera_index=0, duration=3):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return "Camera not available."
    detections = []
    face_det = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
    start = time.time()
    while time.time() - start < duration:
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_det.process(rgb)
        if results.detections:
            detections.append(f"{len(results.detections)} face(s) detected")
    cap.release()
    face_det.close()
    if detections:
        return " | ".join(set(detections))
    return "Nothing detected."

def is_camera_available(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    available = cap.isOpened()
    cap.release()
    return available

# ── CONTINUOUS BACKGROUND MONITORING ─────────────────────────
monitoring = False
monitor_callback = None

def start_monitoring(callback=None, camera_index=0, interval=30):
    global monitoring, monitor_callback
    monitoring = True
    monitor_callback = callback
    def run():
        known_encodings, known_names, known_levels = load_known_faces()
        while monitoring:
            try:
                cap = cv2.VideoCapture(camera_index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        locations = face_recognition.face_locations(rgb)
                        encodings = face_recognition.face_encodings(rgb, locations)
                        for encoding in encodings:
                            if known_encodings:
                                distances = face_recognition.face_distance(known_encodings, encoding)
                                best_idx = np.argmin(distances)
                                if distances[best_idx] > 0.5:
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    unknown_path = os.path.join(UNKNOWN_DIR, f"unknown_{timestamp}.jpg")
                                    cv2.imwrite(unknown_path, frame)
                                    if monitor_callback:
                                        monitor_callback("unknown_face", unknown_path)
                cap.release()
            except:
                pass
            time.sleep(interval)
    t = threading.Thread(target=run, daemon=True)
    t.start()

def stop_monitoring():
    global monitoring
    monitoring = False