from services.ocr.parser.pan_parser import PANParser


class OCRPostProcessor:

    def __init__(self):
        self.parsers = {
            "pan":PANParser()
        }

    def postprocess(self,id_type:str,ocr_output:list[str]) -> dict:

        parser = self.parsers.get(id_type.lower())

        if parser is None:
            raise ValueError(f"Unsupported document type: {id_type}")

        
        return parser.parse(ocr_output)
        