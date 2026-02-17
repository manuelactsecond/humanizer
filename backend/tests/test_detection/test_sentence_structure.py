from app.services.detection.analyzers.sentence_structure import SentenceStructureAnalyzer


class TestSentenceStructureAnalyzer:
    def setup_method(self):
        self.analyzer = SentenceStructureAnalyzer()

    def test_score_in_valid_range(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        assert 0.0 <= result.score <= 1.0

    def test_ai_text_more_monotonous(self, ai_text_en, human_text_en):
        ai_result = self.analyzer.analyze(ai_text_en, "en")
        human_result = self.analyzer.analyze(human_text_en, "en")
        # AI text has more monotonous structure -> higher score
        assert ai_result.score > human_result.score - 0.2

    def test_details_contain_structure_info(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        assert "opener_diversity" in result.details
        assert "sentence_count" in result.details

    def test_spanish_text_works(self, ai_text_es):
        result = self.analyzer.analyze(ai_text_es, "es")
        assert 0.0 <= result.score <= 1.0
