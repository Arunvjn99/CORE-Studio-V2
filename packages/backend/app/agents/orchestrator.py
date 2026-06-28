"""
Design Workflow Orchestrator — LangGraph-powered multi-agent coordinator.

This is the main execution engine. It:
1. Runs the full prompt pipeline (classify → decompose → enrich)
2. Executes agents in order with the right model
3. Pauses at approval gates for human review
4. Aggregates outputs into a coherent workflow result
5. Saves approved patterns for self-learning
"""
from typing import TypedDict, Annotated, AsyncGenerator
from datetime import datetime, timezone
import operator
import structlog

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.pipeline.intent.classifier import classify_intent, IntentResult
from app.pipeline.decomposer.task_decomposer import decompose_tasks, DecomposedPlan
from app.pipeline.enricher.context_enricher import enrich_context, EnrichedContext
from app.pipeline.router.model_router import select_model
from app.agents.planner.planner_agent import PlannerAgent
from app.agents.ux.ux_agent import UXAgent
from app.agents.ui.ui_agent import UIAgent
from app.agents.review.review_agent import ReviewAgent

logger = structlog.get_logger()


class WorkflowState(TypedDict):
    # Input
    workflow_run_id: str
    project_id: str
    user_id: str
    original_prompt: str
    starting_point: str
    work_mode: str
    input_files: list

    # Pipeline results
    intent: dict
    decomposed_plan: dict
    enriched_context: dict
    complexity_score: int

    # Agent outputs
    requirement_blueprint: dict
    ux_blueprint: dict
    ui_blueprint: dict
    review_report: dict

    # Control flow
    current_step: str
    awaiting_approval: bool
    approval_status: str  # pending | approved | rejected | changes_requested
    change_requests: list

    # Metadata
    total_tokens: int
    steps_completed: list[str]
    errors: list[str]
    status_updates: Annotated[list[str], operator.add]  # For WebSocket streaming


# Initialize agents (singletons)
planner = PlannerAgent()
ux_agent = UXAgent()
ui_agent = UIAgent()
review_agent = ReviewAgent()


async def pipeline_node(state: WorkflowState, config: dict = None) -> WorkflowState:
    """Run prompt pipeline: classify → decompose → enrich.

    Accepts an optional db session via LangGraph's configurable mechanism:
        graph.invoke(state, config={"configurable": {"db": session}})
    """
    logger.info("pipeline_start", workflow_id=state["workflow_run_id"])

    # Pull db session from LangGraph config if provided
    db = (config or {}).get("configurable", {}).get("db")

    intent = await classify_intent(
        prompt=state["original_prompt"],
        starting_point=state["starting_point"],
        work_mode=state["work_mode"],
    )

    plan = await decompose_tasks(intent, state["original_prompt"])

    # Enrich context via RAG — db session enables pgvector retrieval
    context = await enrich_context(intent, plan, db=db)

    return {
        **state,
        "intent": intent.model_dump(),
        "decomposed_plan": plan.model_dump(),
        "enriched_context": context.model_dump(),
        "complexity_score": intent.complexity_score,
        "current_step": "pipeline_complete",
        "status_updates": ["✓ Prompt analyzed and decomposed"],
    }


async def planner_node(state: WorkflowState) -> WorkflowState:
    """Planner agent execution."""
    logger.info("planner_start", workflow_id=state["workflow_run_id"])

    from app.pipeline.enricher.context_enricher import EnrichedContext
    context = EnrichedContext(**state["enriched_context"])

    instruction = (
        f"Analyze this design request and produce a Requirement Blueprint:\n"
        f"{state['original_prompt']}\n\n"
        f"Starting point: {state['starting_point']}\n"
        f"Work mode: {state['work_mode']}"
    )

    result = await planner.execute(
        instruction=instruction,
        context=context,
        complexity_score=state["complexity_score"],
        design_system_guidance=state["decomposed_plan"].get("design_system_guidance", ""),
    )

    return {
        **state,
        "requirement_blueprint": result.output,
        "total_tokens": state["total_tokens"] + result.tokens_used,
        "current_step": "awaiting_approval_after_planner",
        "awaiting_approval": True,
        "steps_completed": state["steps_completed"] + ["planner"],
        "status_updates": [
            f"✓ Requirement Blueprint generated ({result.model_selection.model_name}, "
            f"{result.tokens_used} tokens)"
        ],
    }


async def ux_node(state: WorkflowState) -> WorkflowState:
    """UX agent execution."""
    logger.info("ux_start", workflow_id=state["workflow_run_id"])

    from app.pipeline.enricher.context_enricher import EnrichedContext
    context = EnrichedContext(**state["enriched_context"])

    plan = state["decomposed_plan"]
    ux_tasks = [t for t in plan.get("sub_tasks", []) if t["agent"] == "ux"]
    instruction = ux_tasks[0]["instruction"] if ux_tasks else (
        "Design the user experience structure based on the requirement blueprint."
    )

    result = await ux_agent.execute(
        instruction=instruction,
        context=context,
        complexity_score=state["complexity_score"],
        extra_context={"requirement_blueprint": state["requirement_blueprint"]},
        design_system_guidance=plan.get("design_system_guidance", ""),
    )

    return {
        **state,
        "ux_blueprint": result.output,
        "total_tokens": state["total_tokens"] + result.tokens_used,
        "current_step": "awaiting_approval_after_ux",
        "awaiting_approval": True,
        "steps_completed": state["steps_completed"] + ["ux"],
        "status_updates": [
            f"✓ UX Blueprint generated ({result.model_selection.model_name}, "
            f"{result.tokens_used} tokens)"
        ],
    }


async def ui_node(state: WorkflowState) -> WorkflowState:
    """UI agent execution."""
    logger.info("ui_start", workflow_id=state["workflow_run_id"])

    from app.pipeline.enricher.context_enricher import EnrichedContext
    context = EnrichedContext(**state["enriched_context"])

    plan = state["decomposed_plan"]
    ui_tasks = [t for t in plan.get("sub_tasks", []) if t["agent"] == "ui"]
    instruction = ui_tasks[0]["instruction"] if ui_tasks else (
        "Design the complete visual UI based on the UX blueprint."
    )

    result = await ui_agent.execute(
        instruction=instruction,
        context=context,
        complexity_score=state["complexity_score"],
        extra_context={
            "requirement_blueprint": state["requirement_blueprint"],
            "ux_blueprint": state["ux_blueprint"],
        },
        design_system_guidance=plan.get("design_system_guidance", ""),
    )

    return {
        **state,
        "ui_blueprint": result.output,
        "total_tokens": state["total_tokens"] + result.tokens_used,
        "current_step": "awaiting_approval_after_ui",
        "awaiting_approval": True,
        "steps_completed": state["steps_completed"] + ["ui"],
        "status_updates": [
            f"✓ UI Blueprint generated ({result.model_selection.model_name}, "
            f"{result.tokens_used} tokens)"
        ],
    }


async def review_node(state: WorkflowState) -> WorkflowState:
    """Review agent execution."""
    logger.info("review_start", workflow_id=state["workflow_run_id"])

    from app.pipeline.enricher.context_enricher import EnrichedContext
    context = EnrichedContext(**state["enriched_context"])

    instruction = (
        "Review all design artifacts for quality, accessibility, "
        "compliance, and design system adherence."
    )

    result = await review_agent.execute(
        instruction=instruction,
        context=context,
        complexity_score=min(state["complexity_score"], 5),  # Review is analytical, cap complexity
        extra_context={
            "requirement_blueprint": state["requirement_blueprint"],
            "ux_blueprint": state["ux_blueprint"],
            "ui_blueprint": state["ui_blueprint"],
        },
    )

    return {
        **state,
        "review_report": result.output,
        "total_tokens": state["total_tokens"] + result.tokens_used,
        "current_step": "review_complete",
        "steps_completed": state["steps_completed"] + ["review"],
        "status_updates": [
            f"✓ Review complete — Score: {result.output.get('overall_score', 'N/A')}/100"
        ],
    }



def build_design_workflow() -> StateGraph:
    """Construct the LangGraph workflow with human-in-the-loop approval gates.

    Flow:
        pipeline → planner → [interrupt: planner approval]
                            → ux     → [interrupt: ux approval]
                            → ui     → [interrupt: ui approval]
                            → review → END

    Each interrupt pauses the graph at that node boundary.
    Resume by calling graph.invoke(None, config=same_thread_config).
    The WorkflowService handles the HTTP-level approval; this graph is the
    LangGraph execution path (not used by the service layer, which manages
    approvals manually — but this makes the graph correctly structured).
    """
    workflow = StateGraph(WorkflowState)

    workflow.add_node("pipeline_node", pipeline_node)
    workflow.add_node("planner_node", planner_node)
    workflow.add_node("ux_node", ux_node)
    workflow.add_node("ui_node", ui_node)
    workflow.add_node("review_node", review_node)

    workflow.set_entry_point("pipeline_node")
    workflow.add_edge("pipeline_node", "planner_node")
    workflow.add_edge("planner_node", "ux_node")
    workflow.add_edge("ux_node", "ui_node")
    workflow.add_edge("ui_node", "review_node")
    workflow.add_edge("review_node", END)

    # interrupt_before causes the graph to pause BEFORE each named node,
    # allowing a human to review the previous node's output before proceeding.
    return workflow.compile(
        checkpointer=MemorySaver(),
        interrupt_before=["ux_node", "ui_node", "review_node"],
    )


# Singleton compiled graph
design_workflow = build_design_workflow()
