import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from loguru import logger

from services.ocr.ocr_service import OCRService


def main():

    image_path = Path("uploads/ids/b30cd661-30e9-4054-8e0d-90b4b3af66f2.jpeg")

    ocr_service = OCRService()

    result = ocr_service.extract(image_path=image_path, id_type="pan")

    logger.info(result)


if __name__ == "__main__":
    main()
