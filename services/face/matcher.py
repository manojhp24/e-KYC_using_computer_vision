import numpy as np
from loguru import logger


class FaceMatcher:

    DEFAULT_THRESHOLD = 0.6

    def calculate_distance(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> float:

        distance = np.linalg.norm(embedding1 - embedding2)

        return float(distance)

    def comparea_face(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
        threshold: float | None = None,
    ) -> bool:

        if threshold is None:
            threshold = self.DEFAULT_THRESHOLD

        distance = self.calculate_distance(embedding1, embedding2)

        logger.info(f"Face dist:{distance}")

        is_match = distance <= threshold

        return is_match
