"""Workflow endpoints — create, run steps, approve gates."""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.workflow import WorkflowRun, ApprovalGate
from app.services.workflow_service import workflow_service

router = APIRouter(prefix="/workflows", tags=["workflows"])


class CreateWorkflowRequest(BaseModel):
    project_id: str
    user_prompt: str
    starting_point: str = "requirement"  # project | requirement | user_flow | existing_screen
    work_mode: str = "create"            # create | improve | recreate
    input_files: list = []


class RunStepRequest(BaseModel):
    step: str  # pipeline | planner | ux | ui | review
    # Context for later steps
    requirement_artifact_id: Optional[str] = None
    ux_artifact_id: Optional[str] = None
    ui_artifact_id: Optional[str] = None


class ApproveGateRequest(BaseModel):
    status: str  # approved | rejected | changes_requested
    comment: str = ""


@router.post("/", status_code=201)
async def create_workflow(
    req: CreateWorkflowRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new workflow run and automatically kick off the pipeline step."""
    run = await workflow_service.create_workflow(
        project_id=req.project_id,
        user_id=str(current_user.id),
        user_prompt=req.user_prompt,
        starting_point=req.starting_point,
        work_mode=req.work_mode,
        input_files=req.input_files,
        db=db,
    )

    # Start pipeline step in background
    background_tasks.add_task(
        workflow_service.run_pipeline_and_planner,
        str(run.id),
        db,
    )

    return {"workflow_run_id": str(run.id), "status": "started"}


@router.post("/{run_id}/steps")
async def run_step(
    run_id: str,
    req: RunStepRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Manually trigger the next agent step after approval."""
    handlers = {
        "ux": lambda: workflow_service.run_ux_step(
            run_id, req.requirement_artifact_id, db
        ),
        "ui": lambda: workflow_service.run_ui_step(
            run_id, req.ux_artifact_id, req.requirement_artifact_id, db
        ),
        "review": lambda: workflow_service.run_review_step(
            run_id, req.ui_artifact_id, req.ux_artifact_id, req.requirement_artifact_id, db
        ),
    }

    handler = handlers.get(req.step)
    if not handler:
        raise HTTPException(status_code=400, detail=f"Unknown step: {req.step}")

    background_tasks.add_task(handler)
    return {"status": "step_started", "step": req.step}


@router.post("/{run_id}/gates/{gate_id}/approve")
async def approve_gate(
    run_id: str,
    gate_id: str,
    req: ApproveGateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Human approves or rejects an approval gate."""
    gate = await workflow_service.approve_gate(
        gate_id=gate_id,
        user_id=str(current_user.id),
        status=req.status,
        comment=req.comment,
        db=db,
    )
    return {"gate_id": str(gate.id), "status": gate.status}


@router.get("/{run_id}")
async def get_workflow(
    run_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(WorkflowRun).where(WorkflowRun.id == uuid.UUID(run_id))
    result = await db.execute(stmt)
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return {
        "id": str(run.id),
        "project_id": str(run.project_id),
        "title": run.title,
        "status": run.status,
        "current_step": run.current_step,
        "starting_point": run.starting_point,
        "work_mode": run.work_mode,
        "user_prompt": run.user_prompt,
        "total_tokens": run.total_tokens,
        "pipeline_context": run.pipeline_context,
        "created_at": run.created_at.isoformat(),
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
    }
