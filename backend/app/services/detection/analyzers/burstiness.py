import logging

import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

from app.services.detection.analyzers.base import AnalyzerResult, BaseAnalyzer

logger = logging.getLogger(__name__)

# Ensure NLTK data is available
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)


class BurstinessAnalyzer(BaseAnalyzer):
    """
    Measures variation in sentence length and complexity (burstiness).

    Human writing naturally varies: short punchy sentences mixed with long complex ones.
    AI tends to produce uniform sentence lengths and complexity.

    Low burstiness (uniform) -> high score (AI-like)
    High burstiness (varied) -> low score (human-like)
    """

    def analyze(self, text: str, language: str) -> AnalyzerResult:
        lang = "spanish" if language == "es" else "english"
        sentences = sent_tokenize(text, language=lang)
        sentences = [s for s in sentences if len(s.strip()) > 0]

        if len(sentences) < 3:
            return AnalyzerResult(score=0.5, confidence=0.1, details={"error": "too_few_sentences"})

        # Sentence lengths in words
        lengths = [len(word_tokenize(s)) for s in sentences]
        lengths_arr = np.array(lengths, dtype=float)

        # Coefficient of variation of sentence lengths
        mean_len = float(np.mean(lengths_arr))
        std_len = float(np.std(lengths_arr))
        cv = std_len / mean_len if mean_len > 0 else 0.0

        # Vocabulary complexity per sentence (unique words / total words ratio)
        complexities = []
        for sent in sentences:
            words = [w.lower() for w in word_tokenize(sent) if w.isalpha()]
            if len(words) > 0:
                complexity = len(set(words)) / len(words)
                complexities.append(complexity)

        complexity_arr = np.array(complexities) if complexities else np.array([0.5])
        complexity_variance = float(np.std(complexity_arr))

        # Combined burstiness: higher = more human-like
        burstiness = (cv * 0.7) + (complexity_variance * 0.3)

        # Normalize to 0-1 score where 1 = AI-like (low burstiness)
        # Empirical: CV < 0.3 is very uniform (AI-like), CV > 0.7 is very varied (human-like)
        score = max(0.0, min(1.0, 1.0 - (burstiness / 0.8)))

        confidence = min(1.0, len(sentences) / 10.0)

        return AnalyzerResult(
            score=score,
            confidence=confidence,
            details={
                "sentence_count": len(sentences),
                "sentence_lengths": lengths[:50],
                "mean_length": round(mean_len, 2),
                "std_length": round(std_len, 2),
                "length_cv": round(cv, 4),
                "complexity_variance": round(complexity_variance, 4),
                "burstiness_raw": round(burstiness, 4),
            },
        )
