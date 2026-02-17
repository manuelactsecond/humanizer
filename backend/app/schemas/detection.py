from pydantic import BaseModel, Field


class DetectionRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=500_000)
    language: str = Field(default="en", pattern=r"^(en|es)$")


class FeatureScores(BaseModel):
    perplexity: float = Field(..., ge=0, le=1)
    burstiness: float = Field(..., ge=0, le=1)
    vocabulary_richness: float = Field(..., ge=0, le=1)
    sentence_variance: float = Field(..., ge=0, le=1)


class DetectionResult(BaseModel):
    overall_score: float = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0, le=1)
    verdict: str
    features: FeatureScores
    explanation: str
