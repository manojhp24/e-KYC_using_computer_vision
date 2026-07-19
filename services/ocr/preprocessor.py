from pathlib import Path

import cv2

from loguru import logger

class OCRPreprocessor:

    def __init__(self,width: int = 1200):
        self.width = width 

    def preprocess(self,image_path:str | Path):

        img_path = Path(image_path)

        image = cv2.imread(str(img_path))

        if image is None:
            logger.error(f"Unable to read image: {img_path}")
            raise FileNotFoundError(f"Image not Found:{image_path}")

        
        logger.info("Image processing completed.")

        return image

    
    def _resize(self,image):

        height, width = image.shape[:2]

        if width < self.width:
            return

        scale = self.width / width 

        new_width = int(width * scale)

        new_height = int(height * scale)

        resized = cv2.resize(
            image,
            (new_width,new_height),
            interpolation=cv2.INTER_CUBIC
        )

        return resized