import sys
from pathlib import Path

from services.face.detector import FaceDetector
from services.face.encoder import FaceEncoder

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:

    detector = FaceDetector()
    encoder = FaceEncoder()

    image_path = "uploads/live/ed8b1e2d-046e-46a2-8816-a2d2fe76ccfb.jpg"

    face = detector.detect_face(image_path)

    embedding = encoder.encode_face(face)

    print("\n========== Face Embedding ==========")
    print(f"Shape : {embedding.shape}")
    print(f"Type  : {type(embedding)}")
    print(f"Length: {len(embedding)}")

    print("\nFirst 10 values:")
    print(embedding[:10])


if __name__ == "__main__":
    main()
