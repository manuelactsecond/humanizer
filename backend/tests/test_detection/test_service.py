import pytest
from app.services.detection.service import DetectionService


class TestDetectionService:
    def setup_method(self):
        self.service = DetectionService()

    @pytest.mark.asyncio
    async def test_detect_returns_valid_result(self, ai_text_en):
        result = await self.service.detect(ai_text_en, "en")
        assert 0.0 <= result.overall_score <= 1.0
        assert 0.0 <= result.confidence <= 1.0
        assert result.verdict in ("likely_human", "mixed", "likely_ai")
        assert result.explanation

    @pytest.mark.asyncio
    async def test_ai_text_detected(self, ai_text_en):
        result = await self.service.detect(ai_text_en, "en")
        # AI text should score above 0.4 at minimum
        assert result.overall_score > 0.4

    @pytest.mark.asyncio
    async def test_human_text_lower_score(self, human_text_en):
        result = await self.service.detect(human_text_en, "en")
        # Human text should score below 0.6
        assert result.overall_score < 0.6

    @pytest.mark.asyncio
    async def test_features_populated(self, ai_text_en):
        result = await self.service.detect(ai_text_en, "en")
        assert 0.0 <= result.features.perplexity <= 1.0
        assert 0.0 <= result.features.burstiness <= 1.0
        assert 0.0 <= result.features.vocabulary_richness <= 1.0
        assert 0.0 <= result.features.sentence_variance <= 1.0

    @pytest.mark.asyncio
    async def test_spanish_detection(self, ai_text_es):
        result = await self.service.detect(ai_text_es, "es")
        assert result.verdict in ("likely_human", "mixed", "likely_ai")
        assert result.overall_score > 0.3
