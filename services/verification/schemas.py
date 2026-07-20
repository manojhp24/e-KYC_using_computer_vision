from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VerificationResult:
    success: bool
    message: str
    ocr_data: dict[str, Any] | None = None
    face_match: bool | None = None

    user_exists: bool | None = None
    confidence: float | None = None
    user_id: int | None = None
