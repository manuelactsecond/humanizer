from pydantic import BaseModel, Field

from app.schemas.detection import DetectionResult


class HumanizationRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=500_000)
    language: str = Field(default="en", pattern=r"^(en|es)$")
    intensity: str = Field(default="medium", pattern=r"^(light|medium|aggressive)$")


class HumanizationResult(BaseModel):
    original_text: str
    humanized_text: str
    changes_summary: list[str]
    detection_before: DetectionResult
    detection_after: DetectionResult
    word_count_original: int
    word_count_humanized: int
