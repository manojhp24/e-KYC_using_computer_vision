import face_recognition
from loguru import logger
import numpy as np
from pathlib import Path
from services.face.schemas import FaceDetectionResult


class FaceDetector:

    MIN_FACE_COUNT = 1
    MAX_FACE_COUNT = 1

    def detect_face(self,image_path: str | Path) -> FaceDetectionResult:
        
        image_path = Path(image_path)

        image = face_recognition.load_image_file(image_path)

        if image is None:
            raise FileNotFoundError(f"Unable to load image: {image_path}")

        face_locations = face_recognition.face_locations(image)

        self._validate_face_count(face_locations)


        face = self._crop_face(image,face_locations[0])

        result =  FaceDetectionResult(
            image=image,
            face_location=face_locations[0],
            cropped_face=face
        )

        return result

    def _crop_face(self,image:np.ndarray,face_location:tuple[int,int,int,int]) -> np.ndarray:

        top, right, bottom, left = face_location
        

        face = image[top:bottom,left:right]
        
        return face

    def _validate_face_count(self,face_locations:list[tuple[int,int,int,int]]) -> None:
        if len(face_locations) < self.MIN_FACE_COUNT:
            raise ValueError("Face not detected.")
            
        if len(face_locations) > self.MIN_FACE_COUNT:
            raise ValueError("Multiple face detected.")

