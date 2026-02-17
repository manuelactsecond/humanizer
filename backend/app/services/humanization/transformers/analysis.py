import re
import logging

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

from app.services.detection.analyzers.vocabulary import (
    AI_PHRASES_EN,
    AI_PHRASES_ES,
    AI_VOCABULARY_EN,
    AI_VOCABULARY_ES,
)

logger = logging.getLogger(__name__)

# Ensure NLTK data is available
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)


class AnalysisPreprocessor:
    """
    Analyzes text to identify AI-generated patterns.
    Produces a structured report for the LLM humanizer.
    """

    def analyze(self, text: str, language: str) -> dict:
        lang = "spanish" if language == "es" else "english"

        report = {
            "language": language,
            "ai_words_found": [],
            "ai_phrases_found": [],
            "monotonous_sections": [],
            "uniform_sentence_groups": [],
            "low_contraction_rate": False,
            "summary": "",
        }

        # 1. Find AI vocabulary
        text_lower = text.lower()
        ai_vocab = AI_VOCABULARY_EN if language == "en" else AI_VOCABULARY_ES
        ai_phrases = AI_PHRASES_EN if language == "en" else AI_PHRASES_ES

        report["ai_words_found"] = [w for w in ai_vocab if w.lower() in text_lower]
        report["ai_phrases_found"] = [p for p in ai_phrases if p in text_lower]

        # 2. Find monotonous sentence groups (3+ consecutive similar-length sentences)
        sentences = sent_tokenize(text, language=lang)
        sent_lengths = [len(word_tokenize(s)) for s in sentences]

        for i in range(len(sent_lengths) - 2):
            group = sent_lengths[i : i + 3]
            mean = sum(group) / len(group)
            if mean > 0 and all(abs(l - mean) / mean < 0.2 for l in group):
                report["uniform_sentence_groups"].append({
                    "start_sentence": i,
                    "count": 3,
                    "avg_length": round(mean, 1),
                })

        # 3. Check contraction rate (English only)
        if language == "en":
            contractions = len(re.findall(
                r"\b(i'm|i've|i'll|i'd|we're|we've|we'll|we'd|"
                r"they're|they've|they'll|they'd|you're|you've|you'll|you'd|"
                r"he's|she's|it's|that's|there's|here's|who's|what's|"
                r"can't|won't|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|"
                r"hasn't|haven't|hadn't|couldn't|wouldn't|shouldn't|"
                r"let's|ain't)\b",
                text_lower,
            ))
            words = len(re.findall(r"\b\w+\b", text))
            contraction_rate = contractions / (words / 100) if words > 0 else 0
            report["low_contraction_rate"] = contraction_rate < 0.5

        # 4. Build summary
        issues = []
        if report["ai_words_found"]:
            issues.append(f"AI-typical words found: {', '.join(report['ai_words_found'][:10])}")
        if report["ai_phrases_found"]:
            issues.append(f"AI-typical phrases found: {', '.join(report['ai_phrases_found'][:5])}")
        if report["uniform_sentence_groups"]:
            issues.append(f"{len(report['uniform_sentence_groups'])} groups of uniform-length sentences")
        if report["low_contraction_rate"] and language == "en":
            issues.append("Very low contraction rate (typical of AI)")

        report["summary"] = "; ".join(issues) if issues else "No strong AI signals detected"

        return report
