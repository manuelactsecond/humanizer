import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.detection import DetectionResult


class DocumentCreate(BaseModel):
    text: str
    language: str = "en"


class DocumentResponse(BaseModel):
    id: uuid.UUID
    status: str
    language: str
    word_count: int
    detection_score: dict | None = None
    humanized_text: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobResponse(BaseModel):
    id: uuid.UUID
    job_type: str
    status: str
    progress: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
