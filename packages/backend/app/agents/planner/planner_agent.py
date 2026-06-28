"""
Planner Agent — Requirement analysis and blueprint generation.

Input:  User requirement (already decomposed and enriched)
Output: Requirement Blueprint with business rules, user goals, scope
"""
from app.agents.base.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    agent_type = "planner"

    def _agent_description(self) -> str:
        return """You are a senior Business Analyst and Product Strategist.
Your job is to analyze design requirements and produce a clear, structured blueprint
that all subsequent design agents will use as their foundation.
You extract business rules, user goals, success criteria, and scope boundaries."""

    def _output_requirements(self) -> str:
        return """Return a JSON object:
{
  "title": "Blueprint title",
  "executive_summary": "2-3 sentence summary",
  "user_personas": [
    {"name": "...", "role": "...", "goals": [...], "pain_points": [...]}
  ],
  "user_stories": [
    {"id": "US-001", "as_a": "...", "i_want": "...", "so_that": "...", "acceptance_criteria": [...]}
  ],
  "business_rules": ["rule 1", "rule 2", ...],
  "scope": {
    "in_scope": ["..."],
    "out_of_scope": ["..."]
  },
  "screens_needed": ["screen name 1", "screen name 2"],
  "key_flows": ["flow 1 description", "flow 2 description"],
  "compliance_requirements": ["WCAG 2.1 AA", "..."],
  "success_metrics": ["metric 1", "..."],
  "domain_specific_rules": ["domain rule 1", "..."]
}"""

    def build_user_message(self, instruction: str, context: dict) -> str:
        screens_hint = ""
        if context.get("existing_screens"):
            screens_hint = f"\nExisting screens to consider: {context['existing_screens']}"

        return f"""DESIGN REQUEST ANALYSIS:

Instruction: {instruction}
{screens_hint}

Previous Context:
{context.get("previous_output", "None — this is the first step.")}

Analyze this request thoroughly and produce a complete Requirement Blueprint.
Ground all decisions in the organizational knowledge provided in the system prompt."""
