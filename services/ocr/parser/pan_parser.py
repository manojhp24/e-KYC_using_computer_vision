import re
from typing import List


class PANParser:

    PAN_PATTERN = r"[A-Z]{5}[0-9]{4}[A-z]"
    DOB_PATTERN = r"\d{2}/\d{2}/\d{4}"

    def clean_text(self, ocr_output: List[str]) -> List[str]:

        return [text.strip() for text in ocr_output if text.strip()]

    def correct_pan_text(self, text: str) -> str:

        text = text.upper().replace(" ", "")

        if len(text) != 10:
            return text

        chars = list(text)

        digit_map = {"O": "0", "I": "1", "Z": "2", "S": "5", "B": "8"}

        letter_map = {"0": "O", "1": "I", "2": "Z", "5": "S", "8": "B"}

        for i in range(5, 9):
            chars[i] = digit_map.get(chars[i], chars[i])

        for i in [0, 1, 2, 3, 4, 9]:
            chars[i] = letter_map.get(chars[i], chars[i])

        return "".join(chars)

    def extract_pan_text(self, cleaned_text: List[str]) -> str | None:

        for text in cleaned_text:

            corrected = self.correct_pan_text(text)

            match = re.search(self.PAN_PATTERN, corrected)

            if match:
                return match.group()

        return None

    def extract_name(self, cleaned_text: List[str]) -> str | None:

        for i, text in enumerate(cleaned_text):
            if "NAME" in text.upper() and "FATHER" not in text.upper():

                if i + 1 < len(cleaned_text):
                    return cleaned_text[i + 1]

        return None

    def extract_father_name(self, cleaned_text: List[str]) -> str | None:

        for i, text in enumerate(cleaned_text):
            if "FATHER" in text.upper():

                if i + 1 < len(cleaned_text):
                    return cleaned_text[i + 1]
        return None

    def extract_dob(self, cleaned_text: List[str]) -> str | None:

        for text in cleaned_text:

            match = re.search(self.DOB_PATTERN, text)

            if match:
                return match.group()
        return None

    def parse(self, ocr_output: List[str]) -> dict:

        cleaned_text = self.clean_text(ocr_output)

        pan_id_data = {
            "id_type": "PAN",
            "id_number": self.extract_pan_text(cleaned_text),
            "name": self.extract_name(cleaned_text),
            "gender": None,
            "address": None,
            "father_name": self.extract_father_name(cleaned_text),
            "date_of_birth": self.extract_dob(cleaned_text),
        }

        return pan_id_data
