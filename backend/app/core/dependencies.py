from functools import lru_cache

from app.services.detection.service import DetectionService
from app.services.humanization.service import HumanizationService


@lru_cache
def get_detection_service() -> DetectionService:
    return DetectionService()


@lru_cache
def get_humanization_service() -> HumanizationService:
    return HumanizationService()
