from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VerificationResult:
    success: bool
    message: str
    user_exists: bool = False
    ocr_data: dict[str, Any] | None = None
    face_match: bool | None = None
