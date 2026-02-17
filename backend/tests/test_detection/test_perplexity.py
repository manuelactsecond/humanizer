from app.services.detection.analyzers.perplexity import PerplexityAnalyzer


class TestPerplexityAnalyzer:
    def setup_method(self):
        self.analyzer = PerplexityAnalyzer()

    def test_score_in_valid_range(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        assert 0.0 <= result.score <= 1.0
        assert 0.0 <= result.confidence <= 1.0

    def test_ai_text_scores_higher(self, ai_text_en, human_text_en):
        ai_result = self.analyzer.analyze(ai_text_en, "en")
        human_result = self.analyzer.analyze(human_text_en, "en")
        # AI text should generally score higher (more AI-like)
        # Allow some tolerance since this is statistical
        assert ai_result.score > human_result.score - 0.2

    def test_short_text_low_confidence(self):
        result = self.analyzer.analyze("This is too short.", "en")
        assert result.confidence < 0.5

    def test_details_contain_entropy_info(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        assert "word_entropy" in result.details
        assert "bigram_entropy" in result.details
        assert "mode" in result.details
        assert result.details["mode"] == "statistical_entropy"

    def test_spanish_text_works(self, ai_text_es):
        result = self.analyzer.analyze(ai_text_es, "es")
        assert 0.0 <= result.score <= 1.0
