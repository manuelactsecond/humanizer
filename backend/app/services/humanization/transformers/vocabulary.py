import json
import logging
import os
import random
import re

from app.services.humanization.transformers.base import BaseTransformer, TransformContext

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _load_replacements(language: str) -> dict:
    filename = f"{language}_replacements.json"
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Replacement file not found: {filepath}")
        return {}


class VocabularyTransformer(BaseTransformer):
    """
    Post-processing step: replaces any remaining AI-typical vocabulary
    that the LLM might have left in the text.
    """

    def __init__(self):
        self._replacements: dict[str, dict] = {}

    def _get_replacements(self, language: str) -> dict:
        if language not in self._replacements:
            self._replacements[language] = _load_replacements(language)
        return self._replacements[language]

    async def transform(self, text: str, context: TransformContext) -> str:
        replacements = self._get_replacements(context.language)
        if not replacements:
            return text

        changes_made = 0
        result = text

        # Determine replacement threshold based on intensity
        severity_threshold = {
            "light": "high",
            "medium": "medium",
            "aggressive": "low",
        }[context.intensity]

        severity_order = ["high", "medium", "low"]
        threshold_idx = severity_order.index(severity_threshold)

        for word, data in replacements.items():
            word_severity = data.get("severity", "medium")
            word_idx = severity_order.index(word_severity)

            if word_idx > threshold_idx:
                continue

            alts = data.get("replacements", [])
            if not alts:
                continue

            # Case-insensitive word boundary replacement
            pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
            matches = pattern.findall(result)

            if matches:
                for match in matches:
                    replacement = random.choice(alts)
                    # Preserve original capitalization
                    if match[0].isupper():
                        replacement = replacement[0].upper() + replacement[1:]
                    result = result.replace(match, replacement, 1)
                    changes_made += 1

        if changes_made:
            context.changes.append(f"Replaced {changes_made} AI-typical words/phrases")

        return result
