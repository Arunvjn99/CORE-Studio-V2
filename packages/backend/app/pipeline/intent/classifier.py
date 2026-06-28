"""
Intent Classifier — Step 1 of the Prompt Pipeline.

Analyzes the raw user prompt and determines:
- What type of design work is being requested
- The domain context
- The complexity level
- What starting point and work mode to use

Never sends the raw prompt directly to the main agents.
"""
from typing import Literal
from pydantic import BaseModel
import anthropic

from app.core.config import settings


class IntentResult(BaseModel):
    intent_type: Literal[
        "create_design",
        "create_flow",
        "create_wireframe",
        "create_hifi",
        "create_component",
        "improve_existing",
        "recreate_from_screenshot",
        "recreate_from_figma",
        "create_design_system",
        "general_design",
    ]
    domain: str  # retirement, loan, insurance, etc.
    work_mode: Literal["create", "improve", "recreate"]
    starting_point: Literal["project", "requirement", "user_flow", "existing_screen"]
    complexity_score: int  # 1-10
    key_entities: list[str]  # extracted nouns/concepts
    design_goals: list[str]  # what success looks like
    constraints: list[str]  # identified constraints
    confidence: float  # 0.0-1.0


INTENT_CLASSIFICATION_PROMPT = """You are an expert design intent classifier for an AI design platform.

Analyze the user's design request and extract structured intent.

User Request: {prompt}
Starting Point: {starting_point}
Work Mode: {work_mode}

Return a JSON object with:
- intent_type: one of [create_design, create_flow, create_wireframe, create_hifi, create_component, improve_existing, recreate_from_screenshot, recreate_from_figma, create_design_system, general_design]
- domain: the business domain (retirement, loan, insurance, healthcare, banking, ecommerce, or "general")
- work_mode: create | improve | recreate
- starting_point: project | requirement | user_flow | existing_screen
- complexity_score: 1-10 (1=simple single component, 10=full product design system)
- key_entities: list of key UI components, pages, or concepts mentioned
- design_goals: list of what the design must achieve (user outcomes)
- constraints: list of constraints, rules, or limitations mentioned
- confidence: 0.0-1.0 how confident you are in this classification

Complexity guide:
1-3: Single component, simple screen
4-6: Multi-screen flow, moderate complexity
7-9: Full feature, multiple flows, complex requirements
10: Full product design system, entire platform

Be precise. Only return valid JSON, no explanation."""


async def classify_intent(
    prompt: str,
    starting_point: str = "requirement",
    work_mode: str = "create",
) -> IntentResult:
    """Classify user intent using Claude Haiku (fast, cheap)."""
    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    message = await client.messages.create(
        model=settings.DEFAULT_FAST_MODEL,  # Always Haiku for classification
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": INTENT_CLASSIFICATION_PROMPT.format(
                prompt=prompt,
                starting_point=starting_point,
                work_mode=work_mode,
            )
        }]
    )

    import json
    raw = message.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    data = json.loads(raw)
    return IntentResult(**data)
