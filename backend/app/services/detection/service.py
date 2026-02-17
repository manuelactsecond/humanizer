import logging

from app.schemas.detection import DetectionResult, FeatureScores
from app.services.detection.analyzers.base import AnalyzerResult
from app.services.detection.analyzers.burstiness import BurstinessAnalyzer
from app.services.detection.analyzers.perplexity import PerplexityAnalyzer
from app.services.detection.analyzers.sentence_structure import SentenceStructureAnalyzer
from app.services.detection.analyzers.vocabulary import VocabularyAnalyzer

logger = logging.getLogger(__name__)


class DetectionService:
    """Orchestrates all detection analyzers and produces a combined AI detection score."""

    WEIGHTS = {
        "perplexity": 0.35,
        "burstiness": 0.25,
        "vocabulary_richness": 0.20,
        "sentence_variance": 0.20,
    }

    def __init__(self):
        self.perplexity_analyzer = PerplexityAnalyzer()
        self.burstiness_analyzer = BurstinessAnalyzer()
        self.vocabulary_analyzer = VocabularyAnalyzer()
        self.structure_analyzer = SentenceStructureAnalyzer()

    async def detect(self, text: str, language: str) -> DetectionResult:
        # Run all analyzers
        results: dict[str, AnalyzerResult] = {
            "perplexity": self.perplexity_analyzer.analyze(text, language),
            "burstiness": self.burstiness_analyzer.analyze(text, language),
            "vocabulary_richness": self.vocabulary_analyzer.analyze(text, language),
            "sentence_variance": self.structure_analyzer.analyze(text, language),
        }

        # Weighted average score
        total_weight = 0.0
        weighted_score = 0.0
        for key, result in results.items():
            w = self.WEIGHTS[key] * result.confidence
            weighted_score += result.score * w
            total_weight += w

        overall_score = weighted_score / total_weight if total_weight > 0 else 0.5
        overall_score = max(0.0, min(1.0, overall_score))

        # Overall confidence based on agreement between analyzers
        scores = [r.score for r in results.values()]
        score_std = (sum((s - overall_score) ** 2 for s in scores) / len(scores)) ** 0.5
        avg_confidence = sum(r.confidence for r in results.values()) / len(results)
        confidence = avg_confidence * max(0.5, 1.0 - score_std)

        # Verdict
        if overall_score < 0.35:
            verdict = "likely_human"
        elif overall_score > 0.65:
            verdict = "likely_ai"
        else:
            verdict = "mixed"

        # Generate explanation
        explanation = self._generate_explanation(results, overall_score, verdict, language)

        features = FeatureScores(
            perplexity=round(results["perplexity"].score, 4),
            burstiness=round(results["burstiness"].score, 4),
            vocabulary_richness=round(results["vocabulary_richness"].score, 4),
            sentence_variance=round(results["sentence_variance"].score, 4),
        )

        return DetectionResult(
            overall_score=round(overall_score, 4),
            confidence=round(confidence, 4),
            verdict=verdict,
            features=features,
            explanation=explanation,
        )

    def _generate_explanation(
        self,
        results: dict[str, AnalyzerResult],
        overall: float,
        verdict: str,
        language: str,
    ) -> str:
        parts = []

        if language == "es":
            verdict_text = {
                "likely_human": "probablemente escrito por un humano",
                "mixed": "una mezcla de escritura humana e IA",
                "likely_ai": "probablemente generado por IA",
            }
            parts.append(f"Este texto parece ser {verdict_text[verdict]} (puntuación: {overall:.0%}).")

            high_signals = []
            if results["perplexity"].score > 0.6:
                high_signals.append("el texto es muy predecible para modelos de lenguaje")
            if results["burstiness"].score > 0.6:
                high_signals.append("las frases tienen una longitud muy uniforme")
            if results["vocabulary_richness"].score > 0.6:
                ai_words = results["vocabulary_richness"].details.get("ai_words_found", [])
                if ai_words:
                    high_signals.append(f"contiene vocabulario típico de IA: {', '.join(ai_words[:5])}")
                else:
                    high_signals.append("el vocabulario es poco diverso")
            if results["sentence_variance"].score > 0.6:
                high_signals.append("la estructura de las frases es monótona")

            if high_signals:
                parts.append("Señales detectadas: " + "; ".join(high_signals) + ".")

            low_signals = []
            if results["perplexity"].score < 0.35:
                low_signals.append("el texto contiene elecciones de palabras inesperadas")
            if results["burstiness"].score < 0.35:
                low_signals.append("la longitud de las frases varía naturalmente")

            if low_signals:
                parts.append("Señales humanas: " + "; ".join(low_signals) + ".")
        else:
            verdict_text = {
                "likely_human": "likely written by a human",
                "mixed": "a mix of human and AI writing",
                "likely_ai": "likely AI-generated",
            }
            parts.append(f"This text appears to be {verdict_text[verdict]} (score: {overall:.0%}).")

            high_signals = []
            if results["perplexity"].score > 0.6:
                high_signals.append("the text is highly predictable to language models")
            if results["burstiness"].score > 0.6:
                high_signals.append("sentence lengths are very uniform")
            if results["vocabulary_richness"].score > 0.6:
                ai_words = results["vocabulary_richness"].details.get("ai_words_found", [])
                if ai_words:
                    high_signals.append(f"contains AI-typical vocabulary: {', '.join(ai_words[:5])}")
                else:
                    high_signals.append("vocabulary diversity is low")
            if results["sentence_variance"].score > 0.6:
                high_signals.append("sentence structure is monotonous")

            if high_signals:
                parts.append("Detected signals: " + "; ".join(high_signals) + ".")

            low_signals = []
            if results["perplexity"].score < 0.35:
                low_signals.append("the text contains unexpected word choices")
            if results["burstiness"].score < 0.35:
                low_signals.append("sentence lengths vary naturally")

            if low_signals:
                parts.append("Human signals: " + "; ".join(low_signals) + ".")

        return " ".join(parts)
