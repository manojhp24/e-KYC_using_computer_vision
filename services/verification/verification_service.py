from pathlib import Path

from loguru import logger

from services.face.face_service import FaceService
from services.ocr.ocr_service import OCRService
from services.verification.schemas import VerificationResult


class VerificationService:

    def __init__(self) -> None:
        self.face_service = FaceService()
        self.ocr_service = OCRService()

    def verify_user(
        self,
        id_image_path: str | Path,
        live_image_path: str | Path,
        id_type: str,
        liveness_passed: bool,
    ) -> VerificationResult:

        logger.info("Starting user verification...")

        if not liveness_passed:

            logger.warning("Liveness verification failed.")

            return VerificationResult(
                success=False, message="Face verification failed."
            )

        logger.success("Liveness verification passed.")

        logger.info("Extracting information from ID card")

        ocr_data = self.ocr_service.extract(image_path=id_image_path, id_type=id_type)

        logger.success("OCR extraction completed.")

        logger.info("Face verification started.")

        face_match = self.face_service.verify_faces(
            id_image=id_image_path, live_image=live_image_path
        )

        logger.success("Face verification completed.")

        return VerificationResult(
            success=True,
            message="User verified successfully.",
            ocr_data=ocr_data,
            face_match=face_match,
        )
