
from services.face.schemas import FaceDetectionResult
import face_recognition
from loguru import logger
import numpy as np


class FaceEncoder:

    def encode_face(self,detection:FaceDetectionResult) -> np.ndarray:

        encodings = face_recognition.face_encodings(detection.image,known_face_locations=[detection.face_location])

        if not encodings:
            raise ValueError("Unable to generate face embeddings")
        
        embedding = encodings[0]

        return embedding

    