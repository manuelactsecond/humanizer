from fastapi import APIRouter, Depends

from app.core.dependencies import get_humanization_service
from app.schemas.humanization import HumanizationRequest, HumanizationResult
from app.services.humanization.service import HumanizationService

router = APIRouter(prefix="/api/v1/humanization", tags=["humanization"])


@router.post("/humanize", response_model=HumanizationResult)
async def humanize_text(
    request: HumanizationRequest,
    service: HumanizationService = Depends(get_humanization_service),
):
    """Humanize AI-generated text to make it appear more naturally written."""
    return await service.humanize(
        request.text, request.language, request.intensity
    )
