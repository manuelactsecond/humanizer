"""
Perplexity / Predictability Analyzer.

Lightweight mode: Uses statistical entropy measures (character-level and word-level)
as a proxy for perplexity without requiring a large language model.

AI-generated text tends to have LOW entropy (predictable patterns).
Human text tends to have HIGHER entropy (more surprising).

When GPT-2 is available (Phase 2+), this switches to model-based perplexity
for higher accuracy.
"""

import math
import logging
import re
from collections import Counter

import numpy as np

from app.services.detection.analyzers.base import AnalyzerResult, BaseAnalyzer

logger = logging.getLogger(__name__)


class PerplexityAnalyzer(BaseAnalyzer):
    """
    Measures text predictability using statistical entropy.

    Combines multiple entropy signals:
    1. Word-level entropy (Shannon entropy of word distribution)
    2. Bigram entropy (predictability of word pairs)
    3. Character-level entropy
    4. Word rank entropy (how common the words are)

    AI text -> lower combined entropy -> higher score (more AI-like)
    Human text -> higher combined entropy -> lower score (more human-like)
    """

    def analyze(self, text: str, language: str) -> AnalyzerResult:
        words = re.findall(r"\b[a-záéíóúüñ']+\b", text.lower())

        if len(words) < 20:
            return AnalyzerResult(
                score=0.5, confidence=0.1, details={"error": "text_too_short"}
            )

        # 1. Word-level Shannon entropy
        word_entropy = self._word_entropy(words)

        # 2. Bigram entropy (transition predictability)
        bigram_entropy = self._bigram_entropy(words)

        # 3. Character-level entropy
        char_entropy = self._char_entropy(text)

        # 4. Word frequency uniformity (AI uses common words more uniformly)
        freq_uniformity = self._frequency_uniformity(words)

        # 5. Sentence-start entropy (AI is formulaic in how it begins sentences)
        sent_start_entropy = self._sentence_start_entropy(text)

        # Combine signals into a predictability score
        # Lower entropy values suggest more AI-like text
        # Normalize each to 0-1 where 1 = more AI-like

        # Word entropy: human text typically 8-11 bits, AI 6-9 bits
        word_score = max(0.0, min(1.0, (9.5 - word_entropy) / 3.5))

        # Bigram entropy: human typically 6-10, AI 4-7
        bigram_score = max(0.0, min(1.0, (7.5 - bigram_entropy) / 3.5))

        # Char entropy: human typically 4.2-4.8, AI 3.8-4.3
        char_score = max(0.0, min(1.0, (4.3 - char_entropy) / 0.6))

        # Frequency uniformity: higher = more AI-like (AI uses words more evenly)
        freq_score = max(0.0, min(1.0, freq_uniformity))

        # Sentence start entropy: human typically 3.5-5, AI 2-3.5
        sent_score = max(0.0, min(1.0, (3.5 - sent_start_entropy) / 2.0))

        # Weighted combination
        score = (
            word_score * 0.25
            + bigram_score * 0.25
            + char_score * 0.15
            + freq_score * 0.15
            + sent_score * 0.20
        )
        score = max(0.0, min(1.0, score))

        # Confidence scales with text length
        confidence = min(1.0, len(words) / 150.0)

        return AnalyzerResult(
            score=score,
            confidence=confidence,
            details={
                "mode": "statistical_entropy",
                "word_entropy": round(word_entropy, 4),
                "bigram_entropy": round(bigram_entropy, 4),
                "char_entropy": round(char_entropy, 4),
                "freq_uniformity": round(freq_uniformity, 4),
                "sent_start_entropy": round(sent_start_entropy, 4),
                "word_count": len(words),
                "sub_scores": {
                    "word": round(word_score, 4),
                    "bigram": round(bigram_score, 4),
                    "char": round(char_score, 4),
                    "freq": round(freq_score, 4),
                    "sent_start": round(sent_score, 4),
                },
            },
        )

    def _word_entropy(self, words: list[str]) -> float:
        """Shannon entropy of the word distribution."""
        counts = Counter(words)
        total = len(words)
        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def _bigram_entropy(self, words: list[str]) -> float:
        """Entropy of word bigrams - measures transition predictability."""
        if len(words) < 3:
            return 5.0  # neutral

        bigrams = [(words[i], words[i + 1]) for i in range(len(words) - 1)]
        counts = Counter(bigrams)
        total = len(bigrams)
        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def _char_entropy(self, text: str) -> float:
        """Character-level entropy."""
        text_clean = text.lower()
        counts = Counter(text_clean)
        total = len(text_clean)
        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def _frequency_uniformity(self, words: list[str]) -> float:
        """
        Measure how uniformly distributed word frequencies are.
        AI text tends to use words with more even frequency distribution.
        Returns 0-1 where higher = more uniform (more AI-like).
        """
        counts = Counter(words)
        if len(counts) < 5:
            return 0.5

        frequencies = sorted(counts.values(), reverse=True)
        freq_arr = np.array(frequencies, dtype=float)

        # Gini coefficient: 0 = perfectly uniform, 1 = maximally unequal
        # AI text has lower Gini (more uniform)
        n = len(freq_arr)
        mean_freq = float(np.mean(freq_arr))
        if mean_freq == 0:
            return 0.5

        # Calculate Gini
        diff_sum = sum(
            abs(freq_arr[i] - freq_arr[j]) for i in range(n) for j in range(i + 1, n)
        )
        gini = diff_sum / (n * n * mean_freq) if n > 1 else 0.5

        # Invert: low gini (uniform) = high score (AI-like)
        return max(0.0, min(1.0, 1.0 - gini))

    def _sentence_start_entropy(self, text: str) -> float:
        """Entropy of sentence-starting words. AI is repetitive in how it starts sentences."""
        # Split into sentences
        sentences = re.split(r"[.!?]+\s+", text)
        starters = []
        for sent in sentences:
            words = sent.strip().split()
            if words:
                starters.append(words[0].lower())

        if len(starters) < 3:
            return 3.5  # neutral

        counts = Counter(starters)
        total = len(starters)
        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
