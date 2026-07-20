from pathlib import Path
import cv2
import sys
from services.face.detector import FaceDetector

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def main() -> None:
    detector = FaceDetector()

    image_path = "uploads/ids/0ac3c64e-8a81-40cc-9d25-c370d36417cf.jpeg"  # Change this to your test image

    detection = detector.detect_face(image_path)

    print(f"Face Shape: {detection.cropped_face.shape}")

    cv2.imshow("Detected Face", cv2.cvtColor(detection.cropped_face, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()