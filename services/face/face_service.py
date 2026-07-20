from loguru import logger
import numpy as np
from pathlib import Path
from services.face.matcher import FaceMatcher
from services.face.encoder import FaceEncoder
from services.face.detector import FaceDetector
class FaceService:

    def __init__(self):
        self.detector = FaceDetector()
        self.encoder = FaceEncoder()
        self.matcher = FaceMatcher()

    def get_embedding(self,image_path: str | Path) -> np.ndarray:
        logger.info(f"Generating Face Embedding for: {image_path}")

        detection = self.detector.detect_face(image_path)

        embedding = self.encoder.encode_face(detection)

        logger.success("Face Embedding generated successfully")


        return embedding

    def compare_embeddings(self,embedding1:np.ndarray,embedding2:np.ndarray) -> bool:

        logger.info("Comparing facial embeddings....")

        is_match = self.matcher.comparea_face(embedding1,embedding2)

        logger.success(f"Face comparision completed. Match: {is_match}")

        return is_match

    def verify_faces(self,id_image: str | Path, live_image: str | Path) -> bool:

        logger.info("Starting face verification....")

        id_embedding = self.get_embedding(image_path=id_image)

        live_embedding = self.get_embedding(image_path=live_image)

        is_match = self.compare_embeddings(embedding1=id_embedding,embedding2=live_embedding)

        logger.success(f"Face verification completed. Match:{is_match}")

        return is_match