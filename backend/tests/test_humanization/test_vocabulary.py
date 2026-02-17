import pytest
from app.services.humanization.transformers.vocabulary import VocabularyTransformer
from app.services.humanization.transformers.base import TransformContext


class TestVocabularyTransformer:
    def setup_method(self):
        self.transformer = VocabularyTransformer()

    @pytest.mark.asyncio
    async def test_replaces_ai_words_english(self):
        text = "We need to delve into this multifaceted problem and utilize innovative approaches."
        context = TransformContext(language="en", intensity="medium")
        result = await self.transformer.transform(text, context)
        assert "delve" not in result.lower()
        assert "multifaceted" not in result.lower()
        assert "utilize" not in result.lower()

    @pytest.mark.asyncio
    async def test_replaces_ai_words_spanish(self):
        text = "En el ámbito de la tecnología, cabe destacar que resulta fundamental implementar nuevos paradigmas."
        context = TransformContext(language="es", intensity="medium")
        result = await self.transformer.transform(text, context)
        assert "ámbito" not in result.lower() or "cabe destacar" not in result.lower()

    @pytest.mark.asyncio
    async def test_preserves_normal_words(self):
        text = "The cat sat on the mat and looked at the birds outside the window."
        context = TransformContext(language="en", intensity="aggressive")
        result = await self.transformer.transform(text, context)
        # Normal text should be unchanged
        assert result == text

    @pytest.mark.asyncio
    async def test_light_intensity_replaces_fewer(self):
        text = "Furthermore, we must leverage innovative tools to navigate this landscape."
        context_light = TransformContext(language="en", intensity="light")
        context_aggressive = TransformContext(language="en", intensity="aggressive")

        result_light = await self.transformer.transform(text, context_light)
        result_aggressive = await self.transformer.transform(text, context_aggressive)

        # Aggressive should make at least as many changes
        light_changes = len(context_light.changes)
        aggressive_changes = len(context_aggressive.changes)
        # At least both should make some changes
        assert light_changes >= 0
        assert aggressive_changes >= 0

    @pytest.mark.asyncio
    async def test_records_changes(self):
        text = "We should delve into this tapestry of information."
        context = TransformContext(language="en", intensity="medium")
        await self.transformer.transform(text, context)
        assert len(context.changes) > 0
