

from pathlib import Path
from loguru import logger
from services.ocr.preprocessor import OCRPreprocessor
from services.ocr.ocr_engine import OCREngine
from services.ocr.postprocessor import OCRPostProcessor


class OCRService:

    def __init__(self):
        self.preprocessor = OCRPreprocessor()
        self.orc_engine = OCREngine()
        self.postprocessor = OCRPostProcessor()

    def extract(self, image_path: str | Path, id_type: str) -> dict:
        
        logger.info("Starting OCR pipeline...")

        processed_image = self.preprocessor.preprocess(image_path)

        raw_text = self.orc_engine.extract_text(processed_image)

        extracted_data = self.postprocessor.postprocess(id_type,raw_text)

        logger.success("OCR pipeline completed successfully.")

        return extracted_data