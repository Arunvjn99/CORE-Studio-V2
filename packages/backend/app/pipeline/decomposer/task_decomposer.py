"""
Task Decomposer — Step 2 of the Prompt Pipeline.

Takes the classified intent and breaks it into atomic sub-tasks
that each agent will execute. Ensures agents never get a vague
monolithic prompt — they always get precise, scoped instructions.
"""
from typing import Literal
from pydantic import BaseModel
import anthropic
import json

from app.core.config import settings
from app.pipeline.intent.classifier import IntentResult


class SubTask(BaseModel):
    id: str
    agent: Literal["planner", "ux", "ui", "review"]
    title: str
    instruction: str  # Precise instruction for this agent
    depends_on: list[str]  # IDs of sub-tasks that must complete first
    output_type: str  # What artifact this produces
    requires_approval: bool  # Whether this needs human approval before next step
    priority: int  # 1=highest


class DecomposedPlan(BaseModel):
    workflow_title: str
    sub_tasks: list[SubTask]
    estimated_total_complexity: int
    knowledge_domains_needed: list[str]
    design_system_guidance: str


DECOMPOSE_PROMPT = """You are a design workflow orchestrator for an AI design platform.

Given the analyzed intent, decompose the work into precise agent sub-tasks.

Intent Analysis:
{intent_json}

Original Prompt: {original_prompt}

Rules:
1. Always start with the Planner agent for requirements analysis
2. UX agent handles flows, information architecture, wireframes
3. UI agent handles visual design, component styling, hi-fi screens
4. Review agent validates accessibility, compliance, design system adherence
5. Each sub-task must have a precise, self-contained instruction
6. Approval gates (requires_approval=true) must be placed after major deliverables
7. Sub-tasks for later agents must reference outputs from earlier agents

Return JSON with:
{{
  "workflow_title": "descriptive title for this workflow run",
  "sub_tasks": [
    {{
      "id": "task_1",
      "agent": "planner",
      "title": "...",
      "instruction": "Precise instruction the agent must follow...",
      "depends_on": [],
      "output_type": "requirement_blueprint",
      "requires_approval": false,
      "priority": 1
    }},
    ...
  ],
  "estimated_total_complexity": 1-10,
  "knowledge_domains_needed": ["retirement", "ux-standards"],
  "design_system_guidance": "Use Linear design system principles for clean, minimal UI"
}}

Always end with a Review agent task that validates everything.
Only return valid JSON."""


async def decompose_tasks(
    intent: IntentResult,
    original_prompt: str,
) -> DecomposedPlan:
    """Decompose intent into agent sub-tasks."""
    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    # Use Sonnet for decomposition — needs to reason but not at full Opus level
    model = settings.DEFAULT_STANDARD_MODEL

    message = await client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": DECOMPOSE_PROMPT.format(
                intent_json=intent.model_dump_json(indent=2),
                original_prompt=original_prompt,
            )
        }]
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)
    return DecomposedPlan(**data)
