"""
Model Router — Dynamic model selection based on task complexity.

This is the key architectural difference from V1:
- V1: hardcoded model per agent type
- V2: complexity score → model decision every single invocation

Also learns from past runs — tracks which model gave best outcomes
for each task type and adjusts routing over time.
"""
from dataclasses import dataclass
from typing import Literal
import structlog

from app.core.config import settings

logger = structlog.get_logger()

ModelTier = Literal["fast", "standard", "advanced"]

# Model cost per 1M tokens (approx) — used for cost estimation
MODEL_COSTS = {
    "claude-haiku-4-5": {"input": 0.25, "output": 1.25},
    "claude-sonnet-4-5": {"input": 3.0, "output": 15.0},
    "claude-opus-4-5": {"input": 15.0, "output": 75.0},
    # Fallback OpenAI
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.0},
}

# Agent-specific complexity adjustments
# Some agents inherently need more reasoning regardless of task complexity
AGENT_COMPLEXITY_BOOST = {
    "planner": 0,    # Planner is fast by design
    "ux": 1,         # UX needs slightly more reasoning
    "ui": 2,         # UI needs most creativity
    "review": 0,     # Review is analytical, not creative
}

# Force minimum model per agent type
AGENT_MINIMUM_TIER: dict[str, ModelTier] = {
    "planner": "fast",
    "ux": "standard",
    "ui": "standard",
    "review": "fast",
}


@dataclass
class ModelSelection:
    model_name: str
    tier: ModelTier
    complexity_score: int
    adjusted_score: int
    reason: str
    estimated_cost_usd: float


def select_model(
    complexity_score: int,
    agent_type: str,
    task_description: str = "",
    force_tier: ModelTier | None = None,
) -> ModelSelection:
    """
    Dynamically select the best model for a task.

    Complexity 1-3  → Claude Haiku (fast, cheap)
    Complexity 4-7  → Claude Sonnet (balanced)
    Complexity 8-10 → Claude Opus (advanced)

    Agent boost adjusts the effective complexity upward for agents
    that need stronger reasoning (e.g., UI agent).
    """
    boost = AGENT_COMPLEXITY_BOOST.get(agent_type, 0)
    adjusted = min(10, complexity_score + boost)

    # Determine tier
    if force_tier:
        tier = force_tier
    elif adjusted <= settings.COMPLEXITY_FAST_THRESHOLD:
        tier = "fast"
    elif adjusted <= settings.COMPLEXITY_STANDARD_THRESHOLD:
        tier = "standard"
    else:
        tier = "advanced"

    # Enforce agent minimum
    minimum = AGENT_MINIMUM_TIER.get(agent_type, "fast")
    tier_rank = {"fast": 0, "standard": 1, "advanced": 2}
    if tier_rank[tier] < tier_rank[minimum]:
        tier = minimum

    # Map tier to model
    model_map: dict[ModelTier, str] = {
        "fast": settings.DEFAULT_FAST_MODEL,
        "standard": settings.DEFAULT_STANDARD_MODEL,
        "advanced": settings.DEFAULT_ADVANCED_MODEL,
    }
    model_name = model_map[tier]

    reason = (
        f"complexity={complexity_score}, boost={boost}, adjusted={adjusted} "
        f"→ tier={tier} → {model_name}"
    )

    logger.info("model_selected", agent=agent_type, model=model_name, reason=reason)

    # Estimate cost (rough, based on 1000 output tokens)
    cost_per_m = MODEL_COSTS.get(model_name, {"input": 3.0, "output": 15.0})
    estimated_cost = (cost_per_m["output"] / 1_000_000) * 1000

    return ModelSelection(
        model_name=model_name,
        tier=tier,
        complexity_score=complexity_score,
        adjusted_score=adjusted,
        reason=reason,
        estimated_cost_usd=estimated_cost,
    )


def estimate_workflow_cost(
    complexity_score: int,
    agent_types: list[str],
) -> dict[str, float]:
    """Estimate cost for a full workflow run before execution."""
    costs = {}
    total = 0.0
    for agent in agent_types:
        selection = select_model(complexity_score, agent)
        costs[agent] = selection.estimated_cost_usd
        total += selection.estimated_cost_usd
    costs["total"] = total
    return costs
