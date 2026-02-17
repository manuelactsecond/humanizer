import logging

from app.services.humanization.transformers.base import BaseTransformer, TransformContext

logger = logging.getLogger(__name__)

_tool = None


def _get_tool(language: str):
    """Lazy-load LanguageTool to avoid startup overhead."""
    global _tool
    if _tool is None:
        try:
            import language_tool_python

            _tool = language_tool_python.LanguageTool(
                "es" if language == "es" else "en-US"
            )
        except Exception as e:
            logger.warning(f"Could not load LanguageTool: {e}")
            return None
    return _tool


class GrammarPolisher(BaseTransformer):
    """
    Final safety net: runs text through LanguageTool to catch any
    grammar errors introduced during humanization.
    Only applies high-confidence corrections (grammar and typos, not style).
    """

    # Categories to auto-correct
    ALLOWED_CATEGORIES = {
        "GRAMMAR",
        "TYPOS",
        "PUNCTUATION",
        "CASING",
    }

    # Categories to skip (style suggestions would undo humanization)
    SKIP_CATEGORIES = {
        "STYLE",
        "REDUNDANCY",
        "TYPOGRAPHY",
    }

    async def transform(self, text: str, context: TransformContext) -> str:
        tool = _get_tool(context.language)
        if tool is None:
            return text

        try:
            matches = tool.check(text)

            # Filter to only grammar/typo corrections
            corrections = [
                m
                for m in matches
                if m.category in self.ALLOWED_CATEGORIES
                and m.replacements
                and m.category not in self.SKIP_CATEGORIES
            ]

            if not corrections:
                return text

            # Apply corrections in reverse order to preserve offsets
            result = text
            for match in sorted(corrections, key=lambda m: m.offset, reverse=True):
                replacement = match.replacements[0]
                start = match.offset
                end = match.offset + match.errorLength
                result = result[:start] + replacement + result[end:]

            if corrections:
                context.changes.append(f"Fixed {len(corrections)} grammar/spelling issues")

            return result

        except Exception as e:
            logger.warning(f"LanguageTool error: {e}")
            return text
