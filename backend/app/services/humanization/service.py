import logging

from app.schemas.humanization import HumanizationResult
from app.services.detection.service import DetectionService
from app.services.humanization.transformers.analysis import AnalysisPreprocessor
from app.services.humanization.transformers.base import TransformContext
from app.services.humanization.transformers.grammar import GrammarPolisher
from app.services.humanization.transformers.llm_humanizer import LLMHumanizer
from app.services.humanization.transformers.vocabulary import VocabularyTransformer

logger = logging.getLogger(__name__)


class HumanizationService:
    """
    Orchestrates the full humanization pipeline:
    1. Detect AI score BEFORE
    2. Analyze text for AI patterns
    3. LLM humanization (Claude API)
    4. Vocabulary cleanup (catch remaining AI words)
    5. Grammar polish (LanguageTool)
    6. Detect AI score AFTER
    7. Return comparison
    """

    def __init__(self):
        self.detector = DetectionService()
        self.analyzer = AnalysisPreprocessor()
        self.llm_humanizer = LLMHumanizer()
        self.vocab_transformer = VocabularyTransformer()
        self.grammar_polisher = GrammarPolisher()

    async def humanize(
        self, text: str, language: str, intensity: str
    ) -> HumanizationResult:
        # 1. Detection BEFORE
        detection_before = await self.detector.detect(text, language)

        # 2. Analyze for AI patterns
        analysis_report = self.analyzer.analyze(text, language)

        # 3. Create transform context
        context = TransformContext(
            language=language,
            intensity=intensity,
        )
        # Attach analysis report for LLM humanizer
        context.analysis_report = analysis_report  # type: ignore[attr-defined]

        # 4. Run transformation pipeline
        current_text = text

        # Step 1: LLM Humanization (main engine)
        current_text = await self.llm_humanizer.transform(current_text, context)

        # Step 2: Vocabulary cleanup (catch remaining AI words)
        current_text = await self.vocab_transformer.transform(current_text, context)

        # Step 3: Grammar polish
        current_text = await self.grammar_polisher.transform(current_text, context)

        # 5. Detection AFTER
        detection_after = await self.detector.detect(current_text, language)

        # 6. Build result
        return HumanizationResult(
            original_text=text,
            humanized_text=current_text,
            changes_summary=context.changes,
            detection_before=detection_before,
            detection_after=detection_after,
            word_count_original=len(text.split()),
            word_count_humanized=len(current_text.split()),
        )
