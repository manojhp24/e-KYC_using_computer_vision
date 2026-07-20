from pathlib import Path

import numpy as np
from loguru import logger

from services.face.detector import FaceDetector
from services.face.encoder import FaceEncoder
from services.face.matcher import FaceMatcher


class FaceService:

    def __init__(self):
        self.detector = FaceDetector()
        self.encoder = FaceEncoder()
        self.matcher = FaceMatcher()

    def get_embedding(self, image_path: str | Path) -> np.ndarray:

        detection = self.detector.detect_face(image_path)

        embedding = self.encoder.encode_face(detection)

        return embedding

    def compare_embeddings(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> bool:

        is_match = self.matcher.comparea_face(embedding1, embedding2)

        return is_match

    def verify_faces(self, id_image: str | Path, live_image: str | Path) -> bool:

        id_embedding = self.get_embedding(image_path=id_image)

        live_embedding = self.get_embedding(image_path=live_image)

        is_match = self.compare_embeddings(
            embedding1=id_embedding, embedding2=live_embedding
        )

        return is_match
