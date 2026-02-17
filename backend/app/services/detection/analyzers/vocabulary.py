import logging
import re

import numpy as np

from app.services.detection.analyzers.base import AnalyzerResult, BaseAnalyzer

logger = logging.getLogger(__name__)

# AI-typical words and phrases that LLMs overuse
AI_VOCABULARY_EN = {
    # High severity - very strong AI signals
    "delve", "tapestry", "multifaceted", "nuanced", "pivotal",
    "intricate", "elucidate", "illuminate", "profound", "testament",
    "beacon", "embody", "transcend", "revolutionize", "realm",
    "paradigm", "plethora", "myriad", "cacophony",
    # Medium severity - common AI patterns
    "furthermore", "moreover", "additionally", "notably",
    "comprehensive", "innovative", "transformative", "seamless",
    "landscape", "navigate", "leverage", "underscore", "foster",
    "vibrant", "robust", "holistic", "streamline", "synergy",
    "utilize", "facilitate", "endeavor", "commence",
    "Subsequently", "consequently", "nevertheless",
    "meticulous", "meticulously",
}

AI_VOCABULARY_ES = {
    # High severity
    "ámbito", "paradigma", "sinergia", "holístico",
    "trascender", "elucidar", "dilucidar",
    # Medium severity - formulaic discourse markers
    "cabe destacar", "es importante señalar", "en este sentido",
    "asimismo", "no obstante", "sin lugar a dudas",
    "resulta fundamental", "es menester", "en virtud de",
}

AI_PHRASES_EN = [
    "it is important to note",
    "it is worth noting",
    "in today's",
    "in the realm of",
    "shed light on",
    "plays a crucial role",
    "serves as a testament",
    "a rich tapestry",
    "it's important to note",
    "a multifaceted approach",
    "the landscape of",
    "navigate the complexities",
    "at its core",
    "a myriad of",
]

AI_PHRASES_ES = [
    "es importante destacar",
    "cabe señalar que",
    "en el ámbito de",
    "resulta fundamental",
    "en este contexto",
    "a lo largo de la historia",
    "desempeña un papel crucial",
    "en la actualidad",
]


class VocabularyAnalyzer(BaseAnalyzer):
    """
    Analyzes vocabulary richness and AI-typical word usage.

    AI text tends to:
    - Use a smaller effective vocabulary (lower type-token ratio)
    - Overuse certain "AI-favorite" words
    - Have fewer hapax legomena (words appearing exactly once)

    Score: 1 = AI-like (repetitive vocab, AI words present)
    """

    MATTR_WINDOW = 100  # Moving Average Type-Token Ratio window

    def analyze(self, text: str, language: str) -> AnalyzerResult:
        words = re.findall(r"\b[a-záéíóúüñ]+\b", text.lower())

        if len(words) < 20:
            return AnalyzerResult(score=0.5, confidence=0.1, details={"error": "too_few_words"})

        # 1. Moving Average Type-Token Ratio (MATTR)
        mattr = self._compute_mattr(words)

        # 2. AI vocabulary density
        ai_vocab = AI_VOCABULARY_EN if language == "en" else AI_VOCABULARY_ES
        ai_phrases = AI_PHRASES_EN if language == "en" else AI_PHRASES_ES

        text_lower = text.lower()
        ai_words_found = [w for w in ai_vocab if w.lower() in text_lower]
        ai_phrases_found = [p for p in ai_phrases if p in text_lower]

        total_ai_signals = len(ai_words_found) + len(ai_phrases_found) * 2
        ai_density = total_ai_signals / (len(words) / 100)  # per 100 words

        # 3. Hapax legomena ratio
        from collections import Counter
        word_counts = Counter(words)
        hapax = sum(1 for count in word_counts.values() if count == 1)
        hapax_ratio = hapax / len(word_counts) if word_counts else 0.5

        # Scoring components
        # MATTR: human text typically 0.7-0.9, AI text 0.6-0.75
        mattr_score = max(0.0, min(1.0, (0.85 - mattr) / 0.25))

        # AI density: 0 = no AI words, higher = more AI-like
        ai_density_score = max(0.0, min(1.0, ai_density / 3.0))

        # Hapax ratio: human text ~0.5-0.7, AI text ~0.3-0.5
        hapax_score = max(0.0, min(1.0, (0.55 - hapax_ratio) / 0.3))

        # Combined score
        score = (mattr_score * 0.35) + (ai_density_score * 0.40) + (hapax_score * 0.25)
        score = max(0.0, min(1.0, score))

        confidence = min(1.0, len(words) / 200.0)

        return AnalyzerResult(
            score=score,
            confidence=confidence,
            details={
                "word_count": len(words),
                "unique_words": len(word_counts),
                "mattr": round(mattr, 4),
                "ai_words_found": ai_words_found[:20],
                "ai_phrases_found": ai_phrases_found[:10],
                "ai_density_per_100": round(ai_density, 4),
                "hapax_ratio": round(hapax_ratio, 4),
                "mattr_score": round(mattr_score, 4),
                "ai_density_score": round(ai_density_score, 4),
                "hapax_score": round(hapax_score, 4),
            },
        )

    def _compute_mattr(self, words: list[str]) -> float:
        """Moving Average Type-Token Ratio - normalized for text length."""
        if len(words) <= self.MATTR_WINDOW:
            return len(set(words)) / len(words) if words else 0.5

        ttrs = []
        for i in range(len(words) - self.MATTR_WINDOW + 1):
            window = words[i : i + self.MATTR_WINDOW]
            ttrs.append(len(set(window)) / self.MATTR_WINDOW)

        return float(np.mean(ttrs))
