from fastapi import APIRouter, Depends

from app.core.dependencies import get_detection_service
from app.schemas.detection import DetectionRequest, DetectionResult
from app.services.detection.service import DetectionService

router = APIRouter(prefix="/api/v1/detection", tags=["detection"])


@router.post("/analyze", response_model=DetectionResult)
async def analyze_text(
    request: DetectionRequest,
    service: DetectionService = Depends(get_detection_service),
):
    """Analyze text for AI-generated content indicators."""
    return await service.detect(request.text, request.language)
