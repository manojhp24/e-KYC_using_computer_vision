from services.face import detector
import sys
from services.face.detector import FaceDetector
from services.face.encoder import FaceEncoder
from services.face.matcher import FaceMatcher 
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(PROJECT_ROOT))


def main() -> None:

    detector = FaceDetector()
    encoder = FaceEncoder()

    # Id card
    id_image_path = "uploads/ids/cd9c104c-61bb-4b2b-ae32-0117e8811700.jpeg"

    id_face = detector.detect_face(image_path=id_image_path)

    id_embedding = encoder.encode_face(id_face)

    live_image_path = "uploads/live/a45b5298-edd7-44b9-8986-87536334822c.jpg"

    live_detection = detector.detect_face(live_image_path)

    live_embedding = encoder.encode_face(live_detection)

    matcher = FaceMatcher()

    distance = matcher.calculate_distance(embedding1=id_embedding,embedding2=live_embedding)

    print(f"Distance: {distance:.4f}")

    if distance <= 0.5:
        print("Same person")
    else:
        print("Not same person")

if __name__ == "__main__":
    main()