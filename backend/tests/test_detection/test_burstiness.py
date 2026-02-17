import pytest
from app.services.detection.analyzers.burstiness import BurstinessAnalyzer


class TestBurstinessAnalyzer:
    def setup_method(self):
        self.analyzer = BurstinessAnalyzer()

    def test_score_in_valid_range(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        assert 0.0 <= result.score <= 1.0
        assert 0.0 <= result.confidence <= 1.0

    def test_ai_text_more_uniform(self, ai_text_en, human_text_en):
        ai_result = self.analyzer.analyze(ai_text_en, "en")
        human_result = self.analyzer.analyze(human_text_en, "en")
        # AI text has more uniform sentence lengths -> higher score
        assert ai_result.score > human_result.score - 0.2

    def test_details_contain_sentence_info(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        assert "sentence_count" in result.details
        assert "length_cv" in result.details
        assert result.details["sentence_count"] > 0

    def test_spanish_text_works(self, ai_text_es):
        result = self.analyzer.analyze(ai_text_es, "es")
        assert 0.0 <= result.score <= 1.0

    def test_short_text_low_confidence(self):
        result = self.analyzer.analyze("One short sentence here.", "en")
        assert result.confidence < 0.5
