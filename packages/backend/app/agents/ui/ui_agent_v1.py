"""UI Agent v2 — builds UI using design-system components + LLM colour/type decisions."""
from app.agents.base import BaseDesignAgent
from app.llm.client import get_llm_client
from app.design_system.builder import UIBuilder
from app.design_system.tokens import DESIGN_TOKENS
from app.rag.retrievers import get_retriever
from typing import Any, Dict, List, Optional
from app.utils.logger import get_logger
import json

logger = get_logger(__name__)


class UIAgentV2(BaseDesignAgent):
    """Design complete UI using design-system components."""

    name = "ui"

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("design_plan") or state.get("plan") or {}
        ux   = state.get("ux_design")  or state.get("ux_flow") or {}
        title = plan.get("name", "Design")

        retriever = get_retriever()
        patterns = await retriever.retrieve_patterns(title)
        pattern_text = "\n".join([str(p)[:80] for p in patterns[:2]]) or "Modern clean design"

        ux_screens = ux.get("screens", [])
        screen_names = [s.get("name", "Screen") for s in ux_screens[:4]]

        # Ask LLM for colour + typography customisation for this project
        colour_prompt = f"""You are a visual/UI designer.

PROJECT: {title}
UX SCREENS: {', '.join(screen_names) or 'Welcome, Form, Confirmation'}
DESIGN PATTERNS: {pattern_text}

Customise the colour palette and typography for this specific project. Return ONLY valid JSON:
{{
  "colours": {{
    "primary":      "#007AFF",
    "secondary":    "#34C759",
    "background":   "#FFFFFF",
    "surface":      "#F5F5F5",
    "text_primary": "#000000",
    "text_secondary":"#666666",
    "border":       "#E5E5EA",
    "error":        "#FF3B30",
    "success":      "#34C759"
  }},
  "typography": {{
    "font_family": "SF Pro Display, -apple-system, sans-serif",
    "heading_size": 28,
    "body_size": 16,
    "font_scale": "compact"
  }},
  "tone": "professional | playful | minimal | bold"
}}
Only return JSON.
"""

        llm = get_llm_client()
        colour_raw = await llm.chat(
            system="You are a visual designer. Return ONLY valid JSON for colour and typography.",
            user=colour_prompt,
        )
        theme = self._parse_theme(colour_raw)

        builder = UIBuilder()
        screens: List[Dict] = []

        for ux_screen in ux_screens[:5]:
            wf = ux_screen.get("wireframe") or {}
            sections = wf.get("sections") or []
            elements = builder.elements_from_wireframe_sections(sections)
            if not elements:
                # fallback minimal screen
                elements = [
                    builder.create_heading(ux_screen.get("name", "Screen"), level=1),
                    builder.create_button("Continue", "primary"),
                ]
            screen = builder.create_screen(
                name=ux_screen.get("name", "Screen"),
                elements=elements,
                description=ux_screen.get("description", ""),
                background=theme.get("colours", {}).get("background", "#FFFFFF"),
            )
            screens.append(screen)

        # If no UX screens provided, build default 3 screens
        if not screens:
            screens = self._default_screens(title, builder, theme)

        # Merge project theme into design tokens
        merged_tokens = json.loads(json.dumps(DESIGN_TOKENS))  # deep copy
        project_colours = theme.get("colours", {})
        if project_colours:
            merged_tokens["colors"].update(project_colours)
        if theme.get("typography", {}).get("font_family"):
            merged_tokens["typography"]["font_family"] = theme["typography"]["font_family"]

        # Build component-level token map for ui_deliverable
        cs = merged_tokens["colors"]
        token_map: Dict[str, str] = {f"color-{k}": v for k, v in cs.items()}
        for k, v in merged_tokens.get("spacing", {}).items():
            token_map[f"spacing-{k}"] = str(v)
        token_map["font-family"] = merged_tokens["typography"].get("font_family", "SF Pro Display")

        component_names = list(set(
            el.get("type", "unknown")
            for screen in screens
            for el in screen.get("elements", [])
        ))

        ui_data = {
            "name":             f"{title} Design System",
            "tone":             theme.get("tone", "professional"),
            "design_tokens":    merged_tokens,
            "project_colours":  project_colours,
            "components":       builder.components,
            "screens":          screens,
            "responsive_breakpoints": merged_tokens.get("breakpoints", {}),
            "accessibility": {
                "wcag_level":          "AA",
                "minimum_touch_target": 48,
                "keyboard_support":     True,
                "focus_visible":        True,
            },
        }

        ui_deliverable = {
            "figma_file_id":      None,
            "components_created": component_names,
            "tokens_applied":     token_map,
            "design_decisions":   f"{title} — tone: {theme.get('tone', 'professional')}, {len(screens)} screens",
        }

        logger.info(
            f"[{self.name}] UI design created: {len(screens)} screens, "
            f"{len(component_names)} component types, tone={theme.get('tone', '?')}"
        )

        return {
            "ui_deliverable": ui_deliverable,   # canonical key for status endpoint
            "ui_design":      ui_data,          # full spec for chat canvas + plugin
            "stage": "ui_ready",
            "error": None,
        }

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _parse_theme(self, response: str) -> Dict:
        try:
            text = response.strip()
            for prefix in ("```json", "```"):
                if text.startswith(prefix):
                    text = text[len(prefix):]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text.strip())
        except Exception as e:
            logger.warning(f"[{self.name}] Theme parse failed: {e} — using defaults")
            return {}

    def _default_screens(self, title: str, builder: UIBuilder, theme: Dict) -> List[Dict]:
        bg = theme.get("colours", {}).get("background", "#FFFFFF")
        return [
            builder.create_screen(
                "Welcome Screen",
                [
                    builder.create_heading(f"Welcome to {title}", level=1),
                    builder.create_text("Get started below", "body_md"),
                    builder.create_button("Get Started", "primary"),
                ],
                background=bg,
            ),
            builder.create_screen(
                "Form Screen",
                [
                    builder.create_heading("Enter Details", level=2),
                    builder.create_input("Name", "text", required=True),
                    builder.create_input("Description", "textarea"),
                    builder.create_button("Back",   "secondary"),
                    builder.create_button("Submit", "primary"),
                ],
                background=bg,
            ),
            builder.create_screen(
                "Confirmation Screen",
                [
                    builder.create_badge("✓ Success", "success"),
                    builder.create_heading("All done!", level=1),
                    builder.create_text("Your request was submitted successfully.", "body_md"),
                    builder.create_button("Done", "primary"),
                ],
                background=bg,
            ),
        ]
