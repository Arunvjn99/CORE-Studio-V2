"""UX Agent v2 — Detailed user flows with interactions, states and micro-interactions."""
from app.agents.base import BaseDesignAgent
from app.llm.client import get_llm_client
from app.rag.retrievers import get_retriever
from typing import Any, Dict, List, Optional
from app.utils.logger import get_logger
import json

logger = get_logger(__name__)


class UXAgentV2(BaseDesignAgent):
    """Design detailed UX flows with interaction patterns."""

    name = "ux"

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("design_plan") or state.get("plan") or {}
        title = plan.get("name", "Design")
        screens = plan.get("screens", [])
        principles = plan.get("design_principles", [])

        retriever = get_retriever()
        patterns = await retriever.retrieve_patterns(title)

        screen_lines = "\n".join(
            f"- {s.get('id', i)}: {s.get('name', 'Screen')} — {s.get('purpose', '')}"
            for i, s in enumerate(screens[:5])
        )
        pattern_lines = "\n".join([str(p)[:100] for p in patterns[:3]]) or "Mobile-first, accessibility-first"
        principle_lines = ", ".join([p.get("principle", "") for p in principles[:3]]) or "Clarity, Efficiency, Accessibility"

        prompt = f"""You are a UX/interaction designer creating detailed user flows.

PROJECT: {title}
SCREENS FROM PLAN:
{screen_lines or "- screen-1: Welcome\n- screen-2: Main Task\n- screen-3: Confirmation"}

DESIGN PRINCIPLES: {principle_lines}

INTERACTION PATTERNS TO APPLY:
{pattern_lines}

Create a complete UX flow. Return ONLY valid JSON:
{{
  "ux_flow": {{
    "name": "{title} Flow",
    "screens": [
      {{
        "id": "screen-1",
        "name": "Welcome",
        "description": "First screen - set expectations",
        "layout": "vertical_center",
        "wireframe": {{
          "sections": [
            {{"type": "header", "content": "App name or brand"}},
            {{"type": "description", "content": "What the user will accomplish here"}},
            {{"type": "cta_button", "label": "Get Started", "action": "next"}},
            {{"type": "text", "content": "Already have an account? Sign in"}}
          ]
        }},
        "interactions": [
          {{"element": "Get Started", "action": "tap", "result": "Navigate to screen-2"}},
          {{"element": "Sign in", "action": "tap", "result": "Navigate to sign-in"}}
        ],
        "states": {{
          "default": "Ready for user",
          "loading": "Initial data loading"
        }},
        "accessibility": {{
          "landmarks": ["main"],
          "headings": ["h1"],
          "interactive": ["button", "link"]
        }}
      }},
      {{
        "id": "screen-2",
        "name": "Core Interaction",
        "description": "User performs the main task",
        "layout": "vertical_scrollable",
        "wireframe": {{
          "sections": [
            {{"type": "heading", "content": "Complete Your Information"}},
            {{"type": "form", "fields": [
              {{"label": "Primary Field",   "type": "text",     "required": true,  "validation": "Required"}},
              {{"label": "Secondary Field", "type": "textarea", "required": false, "validation": "Optional details"}}
            ]}},
            {{"type": "button_group", "buttons": [
              {{"label": "Back",   "style": "secondary"}},
              {{"label": "Submit", "style": "primary", "disabled_until": "form_valid"}}
            ]}}
          ]
        }},
        "interactions": [
          {{"element": "Primary Field", "action": "blur",    "result": "Validate — show checkmark or error"}},
          {{"element": "Submit",        "action": "tap",     "result": "Submit data, show loading, navigate to screen-3"}},
          {{"element": "Back",          "action": "tap",     "result": "Navigate to screen-1"}}
        ],
        "states": {{
          "empty":       "No fields filled",
          "partial":     "Some fields filled",
          "valid":       "All required fields valid",
          "submitting":  "Sending data",
          "error":       "Validation or server error"
        }},
        "error_handling": [
          {{"field": "Primary Field", "error": "Field required", "help_text": "This field cannot be empty"}}
        ],
        "accessibility": {{
          "landmarks":  ["main", "form"],
          "headings":   ["h1"],
          "labels":     ["Primary Field", "Secondary Field"],
          "required":   ["Primary Field"]
        }}
      }},
      {{
        "id": "screen-3",
        "name": "Confirmation",
        "description": "Confirm successful completion",
        "layout": "vertical_center",
        "wireframe": {{
          "sections": [
            {{"type": "success_message", "icon": "checkmark", "title": "Success!", "subtitle": "Your task is complete"}},
            {{"type": "card", "content": "Summary of what was completed"}},
            {{"type": "button_group", "buttons": [
              {{"label": "Done",        "style": "primary"}},
              {{"label": "View Details","style": "secondary"}}
            ]}}
          ]
        }},
        "interactions": [
          {{"element": "Done",         "action": "tap", "result": "Return to home"}},
          {{"element": "View Details", "action": "tap", "result": "Navigate to detail view"}}
        ],
        "states": {{
          "showing":      "Display confirmation",
          "auto_advance": "Auto-redirect after 3 s (optional)"
        }},
        "accessibility": {{
          "landmarks": ["main"],
          "headings":  ["h1"],
          "status":    "Success announced to screen reader"
        }}
      }}
    ],
    "user_flows": [
      {{
        "name":        "Happy Path",
        "steps":       ["screen-1", "screen-2 (valid)", "screen-3"],
        "description": "User completes all steps without errors"
      }},
      {{
        "name":        "Error Recovery",
        "steps":       ["screen-2 (error state)", "screen-2 (corrected)", "screen-3"],
        "description": "User makes a mistake, corrects, and submits"
      }}
    ],
    "micro_interactions": [
      {{"name": "Button Press",    "trigger": "Tap button",     "animation": "Scale to 0.95 then back", "duration": "150ms"}},
      {{"name": "Field Validation","trigger": "Blur input",     "animation": "Border colour + icon",    "duration": "200ms"}},
      {{"name": "Form Submit",     "trigger": "Submit tap",     "animation": "Button → spinner",        "duration": "300ms"}},
      {{"name": "Success Entry",   "trigger": "Screen-3 loads","animation": "Checkmark draw animation","duration": "600ms"}}
    ],
    "loading_patterns": [
      {{"state": "loading", "indicators": ["spinner"], "message": "Processing your request…"}},
      {{"state": "error",   "indicators": ["error_icon"], "message": "Something went wrong. Please try again."}}
    ]
  }}
}}

REQUIREMENTS:
- Every screen has wireframe sections AND interactions
- All error states defined
- Micro-interactions specified
- Accessibility notes per screen
- Only return JSON
"""

        llm = get_llm_client()
        response = await llm.chat(
            system="You are a UX designer. Return detailed, complete interaction flows as valid JSON only.",
            user=prompt,
        )

        flow = self._parse_response(response)
        if not flow:
            logger.warning(f"[{self.name}] LLM parse failed — using fallback UX")
            flow = self._fallback_ux(title)

        screen_count = len(flow.get("screens", []))
        logger.info(f"[{self.name}] UX flow created: {screen_count} screens")

        return {
            "ux_flow":   flow,   # canonical key
            "ux_design": flow,   # alias
            "stage": "ux_ready",
            "error": None,
        }

    # ── Parsers ───────────────────────────────────────────────────────────────

    def _parse_response(self, response: str) -> Optional[Dict]:
        try:
            text = response.strip()
            for prefix in ("```json", "```"):
                if text.startswith(prefix):
                    text = text[len(prefix):]
            if text.endswith("```"):
                text = text[:-3]

            data = json.loads(text.strip())
            flow = data.get("ux_flow") or data

            if len(flow.get("screens", [])) >= 2:
                return flow
            return None
        except Exception as e:
            logger.warning(f"[{self.name}] Parse error: {e}")
            return None

    def _fallback_ux(self, title: str) -> Dict:
        return {
            "name": f"{title} Flow",
            "screens": [
                {
                    "id": "screen-1", "name": "Welcome", "description": "Entry point",
                    "layout": "vertical_center",
                    "wireframe": {"sections": [
                        {"type": "header", "content": f"Welcome to {title}"},
                        {"type": "description", "content": "Get started below"},
                        {"type": "cta_button", "label": "Get Started"},
                    ]},
                    "interactions": [{"element": "Get Started", "action": "tap", "result": "Go to screen-2"}],
                    "states": {"default": "Ready"},
                    "accessibility": {"landmarks": ["main"], "headings": ["h1"]},
                },
                {
                    "id": "screen-2", "name": "Core Task", "description": "Main interaction",
                    "layout": "vertical",
                    "wireframe": {"sections": [
                        {"type": "heading", "content": "Enter Details"},
                        {"type": "form", "fields": [
                            {"label": "Name", "type": "text", "required": True},
                        ]},
                        {"type": "button_group", "buttons": [
                            {"label": "Back", "style": "secondary"},
                            {"label": "Submit", "style": "primary"},
                        ]},
                    ]},
                    "interactions": [{"element": "Submit", "action": "tap", "result": "Go to screen-3"}],
                    "states": {"empty": "No input", "valid": "Ready", "submitting": "Loading"},
                    "accessibility": {"landmarks": ["main", "form"], "headings": ["h1"]},
                },
                {
                    "id": "screen-3", "name": "Confirmation", "description": "Task complete",
                    "layout": "vertical_center",
                    "wireframe": {"sections": [
                        {"type": "success_message", "icon": "checkmark", "title": "Done!"},
                        {"type": "button_group", "buttons": [{"label": "Done", "style": "primary"}]},
                    ]},
                    "interactions": [{"element": "Done", "action": "tap", "result": "Return home"}],
                    "states": {"showing": "Visible"},
                    "accessibility": {"landmarks": ["main"], "status": "Success announced"},
                },
            ],
            "user_flows": [
                {"name": "Happy Path", "steps": ["screen-1", "screen-2", "screen-3"],
                 "description": "Successful completion"},
            ],
            "micro_interactions": [
                {"name": "Button Press", "trigger": "Tap", "animation": "Scale", "duration": "150ms"},
            ],
            "loading_patterns": [
                {"state": "loading", "indicators": ["spinner"], "message": "Processing…"},
            ],
        }
