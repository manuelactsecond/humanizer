import logging

import anthropic

from app.core.config import get_settings
from app.services.humanization.transformers.base import BaseTransformer, TransformContext

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_EN = """You are an expert text editor specializing in making AI-generated text sound naturally human-written.

Your task: Rewrite the provided text so it reads as if written by a real human. You must preserve the original meaning, facts, and intent completely.

Rules for humanization:
1. VARY SENTENCE LENGTH: Mix short punchy sentences (5-8 words) with longer complex ones (20-35 words). Never have more than 2 sentences of similar length in a row.
2. USE CONTRACTIONS NATURALLY: Replace "do not" with "don't", "it is" with "it's", "cannot" with "can't", etc. Humans use contractions frequently in all but the most formal writing.
3. AVOID AI-TYPICAL VOCABULARY: Never use these words: delve, tapestry, multifaceted, nuanced, pivotal, intricate, elucidate, illuminate, profound, testament, beacon, embody, transcend, revolutionize, realm, paradigm, plethora, myriad, cacophony, furthermore, moreover, additionally, notably, comprehensive, innovative, transformative, seamless, landscape, navigate, leverage, underscore, foster, vibrant, robust, holistic, streamline, synergy, utilize, facilitate, endeavor, commence. Use simpler, more natural alternatives.
4. VARY SENTENCE OPENERS: Don't start consecutive sentences the same way. Mix up how sentences begin - use questions, fragments, subordinate clauses, adverbs, etc.
5. ADD NATURAL FLOW: Include occasional hedging ("sort of", "kind of", "I think", "honestly"), discourse markers ("well", "look", "so"), and conversational connectors.
6. VARY PARAGRAPH LENGTH: Mix short 1-2 sentence paragraphs with longer 4-5 sentence ones.
7. BE SPECIFIC: Where possible, add concrete details instead of vague generalities.
8. MAINTAIN TONE: Keep the same level of formality as the original, just make it sound more natural.

CRITICAL: Output ONLY the rewritten text. No explanations, no comments, no meta-text."""

SYSTEM_PROMPT_ES = """Eres un editor de texto experto especializado en hacer que textos generados por IA suenen como si los hubiera escrito una persona real.

Tu tarea: Reescribir el texto proporcionado para que suene natural, como escrito por un humano. Debes preservar el significado, los hechos y la intención original completamente.

Reglas de humanización (ESPAÑOL DE ESPAÑA):
1. VARÍA LA LONGITUD DE LAS FRASES: Mezcla frases cortas y directas (5-8 palabras) con otras más largas y complejas (20-35 palabras). Nunca pongas más de 2 frases seguidas de longitud similar.
2. USA VOSOTROS: En contextos informales, usa "vosotros" en lugar de "ustedes". Ejemplo: "podéis ver", "tenéis que", "os digo".
3. EVITA VOCABULARIO TÍPICO DE IA: Nunca uses: ámbito, paradigma, sinergia, holístico, trascender, elucidar, dilucidar, cabe destacar, es importante señalar, en este sentido, asimismo, no obstante, sin lugar a dudas, resulta fundamental, es menester, en virtud de. Usa alternativas más naturales y coloquiales.
4. VARÍA LOS INICIOS DE FRASE: No empieces frases consecutivas de la misma manera. Mezcla preguntas, fragmentos, cláusulas subordinadas, adverbios, etc.
5. FLUJO NATURAL: Incluye marcadores conversacionales naturales del español de España: "bueno", "pues", "vamos", "o sea", "a ver", "es que", "hombre", "oye", cuando el registro lo permita.
6. USA EL PRETÉRITO PERFECTO COMPUESTO: Para acciones recientes, usa "he ido" en lugar de "fui" (uso peninsular).
7. VARÍA LA LONGITUD DE LOS PÁRRAFOS: Mezcla párrafos cortos de 1-2 frases con otros más largos de 4-5.
8. SÉ ESPECÍFICO: Donde sea posible, añade detalles concretos en lugar de generalidades vagas.
9. MANTÉN EL TONO: Conserva el mismo nivel de formalidad que el original, solo hazlo sonar más natural.

CRÍTICO: Devuelve SOLO el texto reescrito. Sin explicaciones, sin comentarios, sin meta-texto."""

INTENSITY_INSTRUCTIONS = {
    "light": "\n\nINTENSITY: LIGHT. Make minimal changes - just fix the most obvious AI patterns. Keep the text very close to the original structure.",
    "medium": "\n\nINTENSITY: MEDIUM. Rewrite naturally while keeping the same structure and flow. Change vocabulary and sentence patterns but maintain the overall organization.",
    "aggressive": "\n\nINTENSITY: AGGRESSIVE. Substantially rewrite the text. Change structure, reorder points, vary the approach significantly. The meaning must remain the same but the writing should feel completely different.",
}

INTENSITY_INSTRUCTIONS_ES = {
    "light": "\n\nINTENSIDAD: LIGERA. Haz cambios mínimos - solo corrige los patrones de IA más obvios. Mantén el texto muy cercano a la estructura original.",
    "medium": "\n\nINTENSIDAD: MEDIA. Reescribe de forma natural manteniendo la misma estructura y flujo. Cambia vocabulario y patrones de frases pero mantén la organización general.",
    "aggressive": "\n\nINTENSIDAD: AGRESIVA. Reescribe sustancialmente el texto. Cambia la estructura, reordena puntos, varía el enfoque significativamente. El significado debe ser el mismo pero la escritura debe sentirse completamente diferente.",
}


class LLMHumanizer(BaseTransformer):
    """
    Uses Claude API to intelligently humanize text based on an analysis report.
    """

    def __init__(self):
        settings = get_settings()
        self.client = None
        if settings.anthropic_api_key:
            self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-sonnet-4-5-20250929"

    async def transform(self, text: str, context: TransformContext) -> str:
        if not self.client:
            logger.warning("No Anthropic API key configured, skipping LLM humanization")
            context.changes.append("LLM humanization skipped (no API key)")
            return text

        system_prompt = SYSTEM_PROMPT_ES if context.language == "es" else SYSTEM_PROMPT_EN
        intensity_instr = (
            INTENSITY_INSTRUCTIONS_ES if context.language == "es" else INTENSITY_INSTRUCTIONS
        )
        system_prompt += intensity_instr[context.intensity]

        # Add analysis report to user message if available
        analysis_note = ""
        if hasattr(context, "analysis_report") and context.analysis_report:
            report = context.analysis_report
            if report.get("summary"):
                analysis_note = f"\n\n[ANALYSIS NOTE: {report['summary']}]\n\n"

        user_message = f"{analysis_note}Rewrite this text:\n\n{text}"

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=len(text.split()) * 3,  # Allow some expansion
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )

            humanized = response.content[0].text.strip()
            context.changes.append(f"LLM humanization applied (intensity: {context.intensity})")
            return humanized

        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            context.changes.append(f"LLM humanization failed: {e}")
            return text
