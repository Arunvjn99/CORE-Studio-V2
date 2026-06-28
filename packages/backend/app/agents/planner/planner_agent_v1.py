"""Planner Agent v2 — LLM-powered design plan with full reasoning."""
from app.agents.base import BaseDesignAgent
from app.llm.client import get_llm_client
from app.rag.retrievers import get_retriever
from typing import Any, Dict, List, Optional
from app.utils.logger import get_logger
import json

logger = get_logger(__name__)


class PlannerAgentV2(BaseDesignAgent):
    """Create detailed design plans with LLM reasoning."""

    name = "planner"

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        ticket = state.get("ticket", {})
        title = ticket.get("title", "Design")
        description = ticket.get("description", "")

        retriever = get_retriever()
        guidelines = await retriever.retrieve_guidelines(title)
        past_designs = await retriever.retrieve_past_designs(title)

        guidelines_text = "\n".join([str(g)[:150] for g in guidelines[:3]]) or "Standard design best practices"
        past_text = "\n".join([str(d)[:150] for d in past_designs[:2]]) or "No past designs available"

        prompt = f"""You are a senior product design strategist.

PROJECT: {title}
DESCRIPTION: {description}

INDUSTRY GUIDELINES:
{guidelines_text}

RELEVANT PAST DESIGNS:
{past_text}

Create a comprehensive design plan. Return ONLY valid JSON:

{{
  "design_plan": {{
    "name": "{title}",
    "description": "Concise overview of the design approach",
    "rationale": "Why this approach — what user problems it solves",
    "user_journey": {{
      "personas": [
        {{"name": "Primary User", "goals": ["goal 1", "goal 2"], "pain_points": ["pain 1", "pain 2"]}}
      ],
      "user_flow": "Step-by-step: 1 → 2 → 3",
      "key_moments": ["Moment 1", "Moment 2", "Moment 3"]
    }},
    "design_principles": [
      {{"principle": "Mobile-First", "rationale": "Most users on mobile", "implication": "Single-column layouts, thumb-zone CTAs"}},
      {{"principle": "Accessibility", "rationale": "Inclusive design", "implication": "WCAG 2.1 AA throughout"}},
      {{"principle": "Consistency", "rationale": "Build user trust", "implication": "Reuse design-system components"}}
    ],
    "screens": [
      {{
        "id": "screen-1",
        "name": "Entry Screen",
        "purpose": "Introduce user to the task and set expectations",
        "user_actions": ["Read headline", "Click CTA"],
        "key_elements": ["Hero headline", "Subtext", "Primary CTA button"],
        "success_criteria": "User understands purpose and clicks CTA"
      }},
      {{
        "id": "screen-2",
        "name": "Main Interaction Screen",
        "purpose": "Allow user to complete the core task",
        "user_actions": ["Fill fields", "Submit form"],
        "key_elements": ["Form fields", "Inline validation", "Submit button"],
        "success_criteria": "Form validates and data is submitted"
      }},
      {{
        "id": "screen-3",
        "name": "Confirmation Screen",
        "purpose": "Confirm successful completion and guide next steps",
        "user_actions": ["Read confirmation", "Take next action"],
        "key_elements": ["Success indicator", "Summary", "Next action CTA"],
        "success_criteria": "User feels confident the task is complete"
      }}
    ],
    "design_patterns": [
      {{"name": "Progressive Disclosure", "usage": "Multi-step forms", "rationale": "Reduces cognitive load"}},
      {{"name": "Inline Validation", "usage": "Form fields", "rationale": "Immediate feedback prevents errors"}},
      {{"name": "Clear CTA Hierarchy", "usage": "Every screen", "rationale": "One primary action per screen"}}
    ],
    "accessibility_requirements": [
      "Colour contrast ≥ 4.5:1 for normal text",
      "Touch targets minimum 48 × 48 px",
      "Full keyboard navigation",
      "Screen-reader compatible (ARIA labels + roles)",
      "Visible focus indicators",
      "Respects prefers-reduced-motion"
    ],
    "responsive_breakpoints": {{
      "mobile":  {{"width": 320, "max": 375, "layout": "single column, stacked"}},
      "tablet":  {{"width": 768, "max": 1024, "layout": "2-column"}},
      "desktop": {{"width": 1440, "max": 1920, "layout": "3+ column with sidebar"}}
    }},
    "timeline": {{
      "design_phase":   "2 weeks",
      "implementation": "4 weeks",
      "testing":        "1 week",
      "deployment":     "1 week"
    }},
    "success_metrics": [
      {{"metric": "Task Completion Rate",  "target": "85%",    "measurement": "Analytics funnel"}},
      {{"metric": "Accessibility Score",   "target": "95/100", "measurement": "Automated audit"}},
      {{"metric": "Time on Task",          "target": "< 3 min","measurement": "Session recording"}}
    ]
  }}
}}

SELF-CHECK before responding:
- User journey covers the full flow?
- At least 3 screens with specific purposes?
- Design principles grounded in context?
- Accessibility requirements listed explicitly?
- Success metrics measurable?
Only return JSON.
"""

        llm = get_llm_client()
        response = await llm.chat(
            system="You are a senior design strategist. Provide detailed reasoning. Return ONLY valid JSON.",
            user=prompt,
        )

        plan = self._parse_plan(response)
        if not plan:
            logger.warning(f"[{self.name}] LLM parse failed — using fallback plan")
            plan = self._fallback_plan(title, description)

        screen_count = len(plan.get("screens", []))
        logger.info(f"[{self.name}] Plan created: '{plan.get('name')}' with {screen_count} screens")

        return {
            "plan": plan,               # canonical key for status endpoint
            "design_plan": plan,        # alias read by downstream agents
            "stage": "planning",
            "error": None,
        }

    # ── Parsers ───────────────────────────────────────────────────────────────

    def _parse_plan(self, response: str) -> Optional[Dict]:
        try:
            text = response.strip()
            for prefix in ("```json", "```"):
                if text.startswith(prefix):
                    text = text[len(prefix):]
            if text.endswith("```"):
                text = text[:-3]

            data = json.loads(text.strip())
            plan = data.get("design_plan") or data  # handle both wrapped and bare

            required = ["name", "description", "screens", "design_principles", "accessibility_requirements"]
            if all(k in plan for k in required) and len(plan.get("screens", [])) >= 2:
                return plan
            return None
        except Exception as e:
            logger.warning(f"[{self.name}] Parse error: {e}")
            return None

    def _fallback_plan(self, title: str, description: str) -> Dict:
        return {
            "name": title,
            "description": f"Design plan for {title}" + (f": {description[:80]}" if description else ""),
            "rationale": "Fallback plan — LLM result was not parseable",
            "user_journey": {
                "personas": [{"name": "User", "goals": ["Complete task"], "pain_points": ["Unclear process"]}],
                "user_flow": "Start → Input → Confirm → Done",
                "key_moments": ["First impression", "Decision point", "Completion"],
            },
            "design_principles": [
                {"principle": "Clarity",       "rationale": "Users need guidance",  "implication": "Simple, intuitive layout"},
                {"principle": "Efficiency",    "rationale": "Users value time",     "implication": "Minimal steps to goal"},
                {"principle": "Accessibility", "rationale": "Inclusive by default", "implication": "WCAG 2.1 AA compliance"},
            ],
            "screens": [
                {
                    "id": "screen-1", "name": "Welcome Screen",
                    "purpose": "Introduce user and set expectations",
                    "user_actions": ["Read headline", "Click CTA"],
                    "key_elements": ["Title", "Description", "Primary CTA"],
                    "success_criteria": "User understands purpose and proceeds",
                },
                {
                    "id": "screen-2", "name": "Main Screen",
                    "purpose": "Core task completion",
                    "user_actions": ["Input data", "Submit"],
                    "key_elements": ["Form fields", "Submit button"],
                    "success_criteria": "Task completed successfully",
                },
                {
                    "id": "screen-3", "name": "Success Screen",
                    "purpose": "Confirm completion and guide next steps",
                    "user_actions": ["View confirmation", "Take next action"],
                    "key_elements": ["Success badge", "Summary", "Next CTA"],
                    "success_criteria": "User sees confirmation",
                },
            ],
            "design_patterns": [
                {"name": "Progressive Disclosure", "usage": "Forms", "rationale": "Reduce cognitive load"},
                {"name": "Inline Validation",      "usage": "Inputs", "rationale": "Immediate feedback"},
            ],
            "accessibility_requirements": [
                "Colour contrast ≥ 4.5:1",
                "Touch targets ≥ 48 × 48 px",
                "Keyboard navigation",
                "Screen-reader support",
                "Visible focus indicators",
            ],
            "responsive_breakpoints": {
                "mobile":  {"width": 320, "max": 375, "layout": "single column"},
                "tablet":  {"width": 768, "max": 1024, "layout": "2-column"},
                "desktop": {"width": 1440, "max": 1920, "layout": "3+ column"},
            },
            "timeline": {"design_phase": "2 weeks", "implementation": "4 weeks", "testing": "1 week"},
            "success_metrics": [
                {"metric": "Completion Rate",   "target": "85%",    "measurement": "Analytics"},
                {"metric": "Accessibility Score","target": "95/100", "measurement": "Audit"},
            ],
        }
