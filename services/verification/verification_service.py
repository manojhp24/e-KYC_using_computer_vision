from pathlib import Path

from loguru import logger

from database.database import SessionLocal
from database.repository import UserRepository
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
        db = SessionLocal()
        try:
            repository = UserRepository(db)
            logger.info("Starting user verification...")

            if not liveness_passed:

                logger.warning("Liveness verification failed.")

                return VerificationResult(
                    success=False, message="Liveness verification failed."
                )

            logger.success("Liveness verification passed.")

            logger.info("Extracting information from ID card")

            ocr_data = self.ocr_service.extract(
                image_path=id_image_path, id_type=id_type
            )

            logger.success("OCR extraction completed.")

            logger.info("Checking the User")

            id_number = ocr_data["id_number"]

            if repository.user_exists(id_number=id_number):
                logger.warning(f"User with ID '{id_number}' already exists")

                return VerificationResult(
                    success=False, message="User Already Exists", user_exists=True
                )

            logger.info("Face verification started.")

            face_match = self.face_service.verify_faces(
                id_image=id_image_path, live_image=live_image_path
            )

            if not face_match:
                logger.warning("Face verification failed.")

                return VerificationResult(
                    success=False, message="Face verification failed."
                )

            logger.success("Face verification completed.")

            embedding = self.face_service.get_embedding(id_image_path)

            print(ocr_data)

            repository.create_user(
                name=ocr_data["name"],
                id_number=ocr_data["id_number"],
                id_type=ocr_data["id_type"],
                date_of_birth=ocr_data["date_of_birth"],
                gender=ocr_data["gender"],
                address=ocr_data["address"],
                face_embedding=embedding,
            )

            logger.success("User registered successfully.")

            return VerificationResult(
                success=True,
                message="User registered successfully.",
                user_exists=False,
                ocr_data=ocr_data,
                face_match=face_match,
            )

        except:

            logger.exception("User verification failed.")

            return VerificationResult(
                success=False,
                message="An unexpected error occurred during verification.",
            )

        finally:
            db.close()
