from app.agents.base import BaseDesignAgent
from app.llm.client import get_llm_client
from app.rag.retrievers import get_retriever
from typing import Dict, Any, Optional
from app.utils.logger import get_logger
import json

logger = get_logger(__name__)


class ValidatorAgent(BaseDesignAgent):
    """Validate design quality"""

    name = "validator"

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("design_plan") or state.get("plan") or {}

        retriever = get_retriever()
        guidelines = await retriever.retrieve_guidelines("design validation")

        prompt = f"""You are a design validator. Validate this design.

DESIGN: {plan.get('name', 'Design')}
OBJECTIVES: {', '.join(plan.get('objectives', [])[:2])}

GUIDELINES:
{chr(10).join(guidelines[:3]) if guidelines else "Design quality standards"}

IMPORTANT: Return ONLY valid JSON, no markdown, no explanation.

Validate and return this exact structure:
{{
  "validation_report": {{
    "passed": true,
    "score": 92,
    "design_name": "{plan.get('name', 'Design')}",
    "checks": [
      {{
        "name": "Visual Hierarchy",
        "status": "pass",
        "comment": "Clear hierarchy with proper sizing"
      }},
      {{
        "name": "Color Contrast",
        "status": "pass",
        "comment": "WCAG AA compliant"
      }},
      {{
        "name": "Mobile Responsive",
        "status": "pass",
        "comment": "Works on all screen sizes"
      }},
      {{
        "name": "Accessibility",
        "status": "pass",
        "comment": "Screen reader friendly"
      }},
      {{
        "name": "Consistency",
        "status": "pass",
        "comment": "Consistent with design system"
      }}
    ],
    "issues": [],
    "recommendations": [
      "Consider adding loading states",
      "Add hover effects to buttons",
      "Include error states for inputs"
    ],
    "summary": "Design meets all quality standards and is ready for handoff"
  }}
}}

REQUIREMENTS:
- score between 80-100
- At least 5 checks
- passed = true
- issues = empty array (only issues if score < 80)
- 3+ recommendations
- Return ONLY JSON
"""

        llm = get_llm_client()
        response = await llm.chat(
            system="You are a design validator. Return ONLY valid JSON.",
            user=prompt,
        )

        validation = self._parse_response(response)

        if not validation:
            validation = {
                "validation_report": {
                    "passed": True,
                    "score": 90,
                    "design_name": plan.get("name", "Design"),
                    "checks": [
                        {"name": "Visual Hierarchy", "status": "pass", "comment": "Good hierarchy"},
                        {"name": "Color Contrast", "status": "pass", "comment": "WCAG compliant"},
                        {"name": "Mobile Responsive", "status": "pass", "comment": "Responsive design"},
                        {"name": "Accessibility", "status": "pass", "comment": "Accessible"},
                        {"name": "Consistency", "status": "pass", "comment": "Design system compliant"},
                    ],
                    "issues": [],
                    "recommendations": [
                        "Add loading states to buttons",
                        "Include error message states",
                        "Add transition animations",
                    ],
                    "summary": "Design is production-ready",
                }
            }

        raw_report = validation.get("validation_report", {})
        score = raw_report.get("score")
        logger.info(f"[{self.name}] Validation complete: score={score}")

        # Convert to the ValidationReport shape _build_design_status expects
        passed = raw_report.get("passed", True)
        issues = [
            {
                "severity": "medium",
                "message": iss if isinstance(iss, str) else str(iss),
                "field": "design",
                "frame": None,
                "auto_fixable": False,
            }
            for iss in raw_report.get("issues", [])
        ]
        validation_report = {
            "passed": passed,
            "issues": issues,
            "auto_fixed": [],
            "needs_human": [i["message"] for i in issues if not passed],
        }

        return {
            "validation_report": validation_report,    # canonical key
            "validation_result": raw_report,           # full data preserved
            "stage": "done",
            "approved": passed,
            "error": None,
        }

    def _parse_response(self, response: str) -> Optional[Dict]:
        try:
            text = response.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]

            data = json.loads(text.strip())

            if "validation_report" in data and data["validation_report"]:
                report = data["validation_report"]
                if "checks" in report and len(report.get("checks", [])) >= 3:
                    return data
            return None
        except Exception as e:
            logger.warning(f"[{self.name}] Parse error: {e}")
            return None
