from typing import List

import easyocr
from loguru import logger


class OCREngine:

    def __init__(self, languages: List[str] | None = None):

        if languages is None:
            languages = ["en"]

        logger.info("Loading Easy OCR Model")
        self.reader = easyocr.Reader(languages)
        logger.info("EasyOCR model loaded successfully.")

    def extract_text(self, image):

        logger.info("Running OCR...")

        results = self.reader.readtext(image)

        extracted_text = []

        for _, text, _ in results:
            extracted_text.append(text.strip())

        logger.info(f"Detected {len(extracted_text)} text regions.")

        return extracted_text
