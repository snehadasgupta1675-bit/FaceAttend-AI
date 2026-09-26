import cv2
import numpy as np

CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
FACE_CASCADE = cv2.CascadeClassifier(CASCADE)


def _read_image(uploaded_file):
    data = np.frombuffer(uploaded_file.read(), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return image


def _detect_faces(gray):
    # Try normal detection first.
    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.08,
        minNeighbors=4,
        minSize=(50, 50)
    )

    if len(faces) > 0:
        return faces

    # Try a slightly different image if the first detection fails.
    adjusted = cv2.equalizeHist(gray)

    faces = FACE_CASCADE.detectMultiScale(
        adjusted,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(40, 40)
    )

    return faces


def extract_face_signature(uploaded_file):
    """Detect one face and return a compact normalized grayscale signature."""

    image = _read_image(uploaded_file)

    if image is None:
        raise ValueError("The camera image could not be read.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = _detect_faces(gray)

    if len(faces) == 0:
        raise ValueError(
            "No clear face was detected. Please move closer, face the camera directly, "
            "and make sure your face has enough light."
        )

    if len(faces) > 1:
        # Use the largest face instead of rejecting the frame.
        # This makes the system more practical for a normal camera.
        faces = sorted(
            faces,
            key=lambda box: box[2] * box[3],
            reverse=True
        )

    x, y, w, h = faces[0]

    # Add a little surrounding area.
    pad_x = int(w * 0.15)
    pad_y = int(h * 0.15)

    x1 = max(0, x - pad_x)
    y1 = max(0, y - pad_y)
    x2 = min(gray.shape[1], x + w + pad_x)
    y2 = min(gray.shape[0], y + h + pad_y)

    face = gray[y1:y2, x1:x2]

    if face.size == 0:
        raise ValueError("The detected face could not be processed.")

    face = cv2.resize(
        face,
        (64, 64),
        interpolation=cv2.INTER_AREA
    )

    face = cv2.GaussianBlur(face, (3, 3), 0)

    # Normalize lighting.
    face = cv2.normalize(
        face,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    ).astype(np.uint8)

    return face.flatten().tolist()


def compare_signatures(a, b):
    if not a or not b:
        return 0.0

    arr_a = np.asarray(a, dtype=np.float32)
    arr_b = np.asarray(b, dtype=np.float32)

    if arr_a.size != arr_b.size:
        return 0.0

    a_centered = arr_a - arr_a.mean()
    b_centered = arr_b - arr_b.mean()

    denom = (
        np.linalg.norm(a_centered)
        * np.linalg.norm(b_centered)
    )

    if denom == 0:
        return 0.0

    correlation = float(
        np.dot(a_centered, b_centered) / denom
    )

    return max(
        0.0,
        min(100.0, (correlation + 1.0) * 50.0)
    )