"""
Base Agent — all design agents inherit from this.

Provides:
- Structured prompt construction (never raw user input)
- Model selection via router
- Streaming output support
- Context injection from enricher
- Token counting and cost tracking
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator
from datetime import datetime, timezone
import time
import structlog
import anthropic

from app.core.config import settings
from app.pipeline.router.model_router import select_model, ModelSelection
from app.pipeline.enricher.context_enricher import EnrichedContext

logger = structlog.get_logger()


class AgentResult:
    def __init__(self, output: dict, model_selection: ModelSelection, tokens_used: int, duration_ms: int):
        self.output = output
        self.model_selection = model_selection
        self.tokens_used = tokens_used
        self.duration_ms = duration_ms
        self.success = True
        self.error: str | None = None


class BaseAgent(ABC):
    agent_type: str = "base"

    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    def build_system_prompt(self, context: EnrichedContext, design_system_guidance: str = "") -> str:
        """Build a structured system prompt — never pass raw user input directly."""
        from app.design_system.tokens import DESIGN_TOKENS
        import json

        colors = DESIGN_TOKENS["colors"]
        token_summary = {
            "colors": {
                "brand":    {"primary": colors["primary"], "primary_hover": colors["primary_hover"], "primary_light": colors["primary_light"]},
                "surfaces": {"background": colors["background"], "surface": colors["surface"], "surface_subtle": colors["surface_subtle"], "surface_muted": colors["surface_muted"], "surface_overlay": colors["surface_overlay"]},
                "text":     {"primary": colors["text_primary"], "secondary": colors["text_secondary"], "tertiary": colors["text_tertiary"], "soft": colors["text_soft"], "faint": colors["text_faint"]},
                "borders":  {"default": colors["border"], "strong": colors["border_strong"], "soft": colors["border_soft"]},
                "status": {
                    "success": colors["success"], "success_light": colors["success_light"], "success_border": colors["success_border"],
                    "warning": colors["warning"], "warning_light": colors["warning_light"],
                    "danger":  colors["danger"],  "danger_light":  colors["danger_light"],
                    "info":    colors["info"],     "info_light":    colors["info_light"],
                },
                "interaction": {"focus_ring": colors["focus_ring"], "overlay_scrim": colors["overlay_scrim"]},
            },
            "typography": {k: v for k, v in DESIGN_TOKENS["typography"].items() if k != "ui_sizes"},
            "spacing": DESIGN_TOKENS["spacing"],
            "radius": DESIGN_TOKENS["radius"],
            "shadows": DESIGN_TOKENS["shadows"],
            "motion": DESIGN_TOKENS["motion"],
            "layout_canvases": DESIGN_TOKENS.get("layout_canvases", {}),
            "component_rules": DESIGN_TOKENS.get("component_rules", {}),
        }

        return f"""You are the {self.agent_type.upper()} agent in CORE Studio, an AI-powered design platform.

{self._agent_description()}

ORGANIZATIONAL KNOWLEDGE CONTEXT:
{context.context_summary}

DESIGN SYSTEM TOKENS (use exactly — do not invent new values):
{json.dumps(token_summary, indent=2)}

{f"ADDITIONAL DESIGN SYSTEM GUIDANCE:{chr(10)}{design_system_guidance}" if design_system_guidance else ""}

OUTPUT REQUIREMENTS:
{self._output_requirements()}

RULES:
- Always ground output in the organizational knowledge provided
- Use ONLY the token values above — never invent hex values outside these tokens
- Follow accessibility standards (WCAG 2.1 AA minimum — 4.5:1 contrast for body text)
- Apply motion tokens for transitions: use motion.interaction for interactive elements, motion.transform for layout shifts
- Be specific — no generic placeholder content, no "Lorem ipsum", no "Heading here"
- Structure output as valid JSON matching the expected schema exactly
- Never mention AI or that you are generating this content
- Never add explanatory prose outside the JSON structure"""

    @abstractmethod
    def _agent_description(self) -> str:
        """What this agent does."""
        pass

    @abstractmethod
    def _output_requirements(self) -> str:
        """What format/structure the output must follow."""
        pass

    @abstractmethod
    def build_user_message(self, instruction: str, context: dict) -> str:
        """Build the structured user message for this specific invocation."""
        pass

    async def execute(
        self,
        instruction: str,
        context: EnrichedContext,
        complexity_score: int,
        extra_context: dict | None = None,
        design_system_guidance: str = "",
    ) -> AgentResult:
        """Execute the agent with dynamic model selection."""
        start = time.time()

        model_selection = select_model(
            complexity_score=complexity_score,
            agent_type=self.agent_type,
        )

        system_prompt = self.build_system_prompt(context, design_system_guidance)
        user_message = self.build_user_message(instruction, extra_context or {})

        logger.info("agent_executing",
            agent=self.agent_type,
            model=model_selection.model_name,
            complexity=complexity_score,
        )

        message = await self.client.messages.create(
            model=model_selection.model_name,
            max_tokens=8192,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        duration_ms = int((time.time() - start) * 1000)
        tokens_used = message.usage.input_tokens + message.usage.output_tokens
        raw_output = message.content[0].text

        output = self._parse_output(raw_output)

        return AgentResult(
            output=output,
            model_selection=model_selection,
            tokens_used=tokens_used,
            duration_ms=duration_ms,
        )

    async def stream_execute(
        self,
        instruction: str,
        context: EnrichedContext,
        complexity_score: int,
        extra_context: dict | None = None,
        design_system_guidance: str = "",
    ) -> AsyncGenerator[str, None]:
        """Stream agent output token by token for real-time UI updates."""
        model_selection = select_model(
            complexity_score=complexity_score,
            agent_type=self.agent_type,
        )

        system_prompt = self.build_system_prompt(context, design_system_guidance)
        user_message = self.build_user_message(instruction, extra_context or {})

        async with self.client.messages.stream(
            model=model_selection.model_name,
            max_tokens=8192,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        ) as stream:
            async for text in stream.text_stream:
                yield text

    def _parse_output(self, raw: str) -> dict:
        """Parse agent output — extract JSON if present, else wrap in content field."""
        import json
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"content": raw, "raw": True}
