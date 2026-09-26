import cv2
import numpy as np

CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
FACE_CASCADE = cv2.CascadeClassifier(CASCADE)


def _read_image(uploaded_file):
    data = np.frombuffer(uploaded_file.read(), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return image


def extract_face_signature(uploaded_file):
    """Detect the largest face and return a compact normalized grayscale signature."""
    image = _read_image(uploaded_file)
    if image is None:
        raise ValueError("The uploaded image could not be read.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
    if len(faces) == 0:
        raise ValueError("No clear face was detected.")
    if len(faces) > 1:
        raise ValueError("Multiple faces were detected. Please use one face at a time.")

    x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
    pad_x, pad_y = int(w * 0.12), int(h * 0.12)
    x1, y1 = max(0, x - pad_x), max(0, y - pad_y)
    x2, y2 = min(gray.shape[1], x + w + pad_x), min(gray.shape[0], y + h + pad_y)
    face = gray[y1:y2, x1:x2]
    face = cv2.resize(face, (64, 64), interpolation=cv2.INTER_AREA)
    face = cv2.GaussianBlur(face, (3, 3), 0)
    # Normalize illumination so small lighting changes have less effect.
    face = cv2.normalize(face, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return face.flatten().tolist()


def compare_signatures(a, b):
    if not a or not b:
        return 0.0
    arr_a = np.asarray(a, dtype=np.float32)
    arr_b = np.asarray(b, dtype=np.float32)
    if arr_a.size != arr_b.size:
        return 0.0
    # Correlation-based similarity is converted to a 0-100 score.
    a_centered = arr_a - arr_a.mean()
    b_centered = arr_b - arr_b.mean()
    denom = np.linalg.norm(a_centered) * np.linalg.norm(b_centered)
    if denom == 0:
        return 0.0
    correlation = float(np.dot(a_centered, b_centered) / denom)
    return max(0.0, min(100.0, (correlation + 1.0) * 50.0))
