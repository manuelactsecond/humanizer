from app.services.detection.analyzers.vocabulary import VocabularyAnalyzer


class TestVocabularyAnalyzer:
    def setup_method(self):
        self.analyzer = VocabularyAnalyzer()

    def test_score_in_valid_range(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        assert 0.0 <= result.score <= 1.0

    def test_detects_ai_vocabulary(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        ai_words = result.details.get("ai_words_found", [])
        # Our sample AI text contains many AI-typical words
        assert len(ai_words) > 3

    def test_human_text_fewer_ai_words(self, human_text_en):
        result = self.analyzer.analyze(human_text_en, "en")
        ai_words = result.details.get("ai_words_found", [])
        assert len(ai_words) < 3

    def test_ai_text_scores_higher(self, ai_text_en, human_text_en):
        ai_result = self.analyzer.analyze(ai_text_en, "en")
        human_result = self.analyzer.analyze(human_text_en, "en")
        assert ai_result.score > human_result.score

    def test_spanish_detection(self, ai_text_es):
        result = self.analyzer.analyze(ai_text_es, "es")
        ai_words = result.details.get("ai_words_found", [])
        assert len(ai_words) > 0
        assert 0.0 <= result.score <= 1.0

    def test_mattr_computed(self, ai_text_en):
        result = self.analyzer.analyze(ai_text_en, "en")
        assert "mattr" in result.details
        assert 0.0 < result.details["mattr"] < 1.0
