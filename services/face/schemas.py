from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FaceDetectionResult:
    image: np.ndarray
    face_location: tuple[int, int, int, int]
    cropped_face: np.ndarray
