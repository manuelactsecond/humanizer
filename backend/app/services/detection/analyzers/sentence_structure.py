import logging
from collections import Counter

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
try:
    nltk.data.find("taggers/averaged_perceptron_tagger_eng")
except LookupError:
    nltk.download("averaged_perceptron_tagger_eng", quiet=True)


class SentenceStructureAnalyzer(BaseAnalyzer):
    """
    Analyzes structural monotony in text.

    AI text tends to have:
    - Uniform sentence lengths
    - Repetitive sentence openers (same POS patterns at sentence start)
    - Low diversity in syntactic structures

    High monotony -> high score (AI-like)
    """

    def analyze(self, text: str, language: str) -> AnalyzerResult:
        lang = "spanish" if language == "es" else "english"
        sentences = sent_tokenize(text, language=lang)
        sentences = [s for s in sentences if len(s.strip()) > 3]

        if len(sentences) < 5:
            return AnalyzerResult(score=0.5, confidence=0.1, details={"error": "too_few_sentences"})

        # 1. Sentence opener diversity using POS tags
        openers = []
        for sent in sentences:
            words = word_tokenize(sent)
            alpha_words = [w for w in words if w.isalpha()]
            if len(alpha_words) >= 2:
                tagged = nltk.pos_tag(alpha_words[:2])
                opener = "_".join(tag for _, tag in tagged)
                openers.append(opener)

        opener_counter = Counter(openers)
        n_unique_openers = len(opener_counter)
        n_sentences = len(openers)
        opener_diversity = n_unique_openers / n_sentences if n_sentences > 0 else 0.5

        # 2. Consecutive same-opener sequences (monotony indicator)
        max_consecutive = 1
        current_run = 1
        for i in range(1, len(openers)):
            if openers[i] == openers[i - 1]:
                current_run += 1
                max_consecutive = max(max_consecutive, current_run)
            else:
                current_run = 1

        # 3. Paragraph length variance (split by double newlines)
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if len(paragraphs) > 1:
            para_lengths = [len(p.split()) for p in paragraphs]
            para_mean = float(np.mean(para_lengths))
            para_cv = float(np.std(para_lengths) / para_mean) if para_mean > 0 else 0.0
        else:
            para_cv = 0.5  # Neutral if single paragraph

        # 4. Sentence length standard deviation (normalized)
        sent_lengths = [len(word_tokenize(s)) for s in sentences]
        sent_std = float(np.std(sent_lengths))
        sent_mean = float(np.mean(sent_lengths))
        sent_cv = sent_std / sent_mean if sent_mean > 0 else 0.0

        # Scoring
        opener_score = max(0.0, min(1.0, (0.65 - opener_diversity) / 0.35))
        consecutive_score = max(0.0, min(1.0, (max_consecutive - 1) / 4.0))
        para_score = max(0.0, min(1.0, (0.4 - para_cv) / 0.35))
        sent_cv_score = max(0.0, min(1.0, (0.5 - sent_cv) / 0.35))

        score = (
            opener_score * 0.35
            + consecutive_score * 0.20
            + para_score * 0.20
            + sent_cv_score * 0.25
        )
        score = max(0.0, min(1.0, score))

        confidence = min(1.0, len(sentences) / 15.0)

        return AnalyzerResult(
            score=score,
            confidence=confidence,
            details={
                "sentence_count": len(sentences),
                "unique_openers": n_unique_openers,
                "opener_diversity": round(opener_diversity, 4),
                "max_consecutive_same_opener": max_consecutive,
                "top_openers": dict(opener_counter.most_common(5)),
                "paragraph_count": len(paragraphs),
                "paragraph_length_cv": round(para_cv, 4),
                "sentence_length_cv": round(sent_cv, 4),
                "opener_score": round(opener_score, 4),
                "consecutive_score": round(consecutive_score, 4),
            },
        )
