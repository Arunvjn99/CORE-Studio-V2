"""
Review Agent — Quality, accessibility, compliance, design system validation.

Input:  All previous artifacts (Requirement, UX, UI blueprints)
Output: Review Report with pass/fail checks and actionable feedback
"""
from app.agents.base.base_agent import BaseAgent


class ReviewAgent(BaseAgent):
    agent_type = "review"

    def _agent_description(self) -> str:
        return """You are a senior Design QA Engineer and Accessibility Specialist.
Your job is to review all design artifacts and validate:
- UX quality and usability
- Accessibility compliance (WCAG 2.1 AA)
- Design system adherence
- Business requirement coverage
- Compliance with company standards
You produce actionable, specific feedback — not vague suggestions."""

    def _output_requirements(self) -> str:
        return """Return a JSON object:
{
  "overall_status": "approved | approved_with_changes | rejected",
  "overall_score": 0-100,
  "summary": "2-3 sentence executive summary",
  "checks": [
    {
      "category": "accessibility | ux_quality | design_system | requirements | compliance",
      "check_name": "...",
      "status": "pass | fail | warning",
      "severity": "critical | major | minor | info",
      "details": "Specific finding",
      "recommendation": "Exact fix needed",
      "wcag_criterion": "1.4.3" // if accessibility check
    }
  ],
  "accessibility_report": {
    "score": 0-100,
    "issues_critical": 0,
    "issues_major": 0,
    "issues_minor": 0,
    "highlights": ["what's good", "..."]
  },
  "design_system_compliance": {
    "score": 0-100,
    "deviations": ["...", "..."]
  },
  "requirements_coverage": {
    "covered": ["US-001", "US-002"],
    "missing": ["US-003"],
    "coverage_percent": 85
  },
  "recommended_changes": [
    {
      "priority": "critical | high | medium | low",
      "area": "screen name or component",
      "change": "Exact change needed",
      "reason": "Why this matters"
    }
  ],
  "approved_patterns": [
    "Pattern to save to knowledge base for future reuse"
  ]
}"""

    def build_user_message(self, instruction: str, context: dict) -> str:
        return f"""DESIGN REVIEW TASK:

Instruction: {instruction}

Requirement Blueprint:
{context.get("requirement_blueprint", {})}

UX Blueprint:
{context.get("ux_blueprint", {})}

UI Blueprint:
{context.get("ui_blueprint", {})}

Review all artifacts thoroughly against the organizational standards in your context.
Be specific and actionable — every issue must have a clear recommendation.
Flag any accessibility violations with exact WCAG criteria.
Identify patterns that should be saved to the knowledge base for future reuse."""
