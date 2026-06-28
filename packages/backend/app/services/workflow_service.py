"""
Workflow Service — Orchestrates design workflow runs.

Handles:
- Workflow creation and state management
- Running agents in sequence with approval gates
- Broadcasting real-time updates via WebSocket
- Saving artifacts to the database
- Learning from approved outputs
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from app.models.workflow import WorkflowRun, WorkflowStep, ApprovalGate, WorkflowStatus, StepStatus, ApprovalStatus
from app.models.artifact import Artifact, ArtifactType, ArtifactStatus
from app.pipeline.intent.classifier import classify_intent
from app.pipeline.decomposer.task_decomposer import decompose_tasks
from app.pipeline.enricher.context_enricher import enrich_context
from app.agents.planner.planner_agent import PlannerAgent
from app.agents.ux.ux_agent import UXAgent
from app.agents.ui.ui_agent import UIAgent
from app.agents.review.review_agent import ReviewAgent
from app.websocket.manager import ws_manager

logger = structlog.get_logger()

planner = PlannerAgent()
ux_agent = UXAgent()
ui_agent = UIAgent()
review_agent = ReviewAgent()


class WorkflowService:

    async def create_workflow(
        self,
        project_id: str,
        user_id: str,
        user_prompt: str,
        starting_point: str,
        work_mode: str,
        input_files: list,
        db: AsyncSession,
    ) -> WorkflowRun:
        run = WorkflowRun(
            id=uuid.uuid4(),
            project_id=uuid.UUID(project_id),
            initiated_by=uuid.UUID(user_id),
            title=f"Design Run — {user_prompt[:60]}...",
            status=WorkflowStatus.PENDING,
            starting_point=starting_point,
            work_mode=work_mode,
            user_prompt=user_prompt,
            input_files=input_files,
        )
        db.add(run)
        await db.commit()
        await db.refresh(run)
        return run

    async def run_pipeline_step(
        self, workflow_run_id: str, db: AsyncSession
    ) -> WorkflowRun:
        """Run the prompt pipeline (classify, decompose, enrich)."""
        run = await self._get_run(workflow_run_id, db)
        run.status = WorkflowStatus.RUNNING
        run.started_at = datetime.now(timezone.utc)
        await db.commit()

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "step_start", "step": "pipeline", "message": "Analyzing your prompt..."
        })

        intent = await classify_intent(run.user_prompt, run.starting_point, run.work_mode)
        plan = await decompose_tasks(intent, run.user_prompt)
        context = await enrich_context(intent, plan, db=db)

        run.pipeline_context = {
            "intent": intent.model_dump(),
            "plan": plan.model_dump(),
        }
        run.knowledge_context = context.model_dump()
        run.current_step = "planner"
        await db.commit()

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "step_complete",
            "step": "pipeline",
            "message": f"Prompt analyzed — {len(plan.sub_tasks)} sub-tasks identified",
            "data": {"intent": intent.model_dump(), "complexity": intent.complexity_score},
        })

        return run

    async def run_planner_step(
        self, workflow_run_id: str, db: AsyncSession
    ) -> tuple[WorkflowRun, Artifact]:
        run = await self._get_run(workflow_run_id, db)
        step = await self._create_step(run.id, "planner", 1, db)

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "agent_start", "agent": "planner",
            "message": "Planner Agent is analyzing requirements...",
        })

        from app.pipeline.enricher.context_enricher import EnrichedContext
        context = EnrichedContext(**run.knowledge_context)
        plan = run.pipeline_context.get("plan", {})
        intent_data = run.pipeline_context.get("intent", {})
        complexity = intent_data.get("complexity_score", 5)

        result = await planner.execute(
            instruction=f"Analyze: {run.user_prompt}\nStarting point: {run.starting_point}\nWork mode: {run.work_mode}",
            context=context,
            complexity_score=complexity,
            design_system_guidance=plan.get("design_system_guidance", ""),
        )

        artifact = await self._save_artifact(
            project_id=str(run.project_id),
            workflow_run_id=workflow_run_id,
            artifact_type=ArtifactType.REQUIREMENT,
            name="Requirement Blueprint",
            content=result.output,
            agent_type="planner",
            model_used=result.model_selection.model_name,
            complexity_score=complexity,
            tokens_used=result.tokens_used,
            duration_ms=result.duration_ms,
            prompt=run.user_prompt,
            db=db,
        )

        await self._complete_step(step, result, db)

        gate = await self._create_approval_gate(
            workflow_run_id=workflow_run_id,
            artifact_id=str(artifact.id),
            gate_type="after_planner",
            db=db,
        )

        run.current_step = "awaiting_approval_after_planner"
        run.status = WorkflowStatus.AWAITING_APPROVAL
        run.total_tokens += result.tokens_used
        await db.commit()

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "approval_required",
            "step": "planner",
            "gate_id": str(gate.id),
            "artifact_id": str(artifact.id),
            "message": "Requirement Blueprint ready for review",
        })

        return run, artifact

    async def run_ux_step(
        self, workflow_run_id: str, requirement_artifact_id: str, db: AsyncSession
    ) -> tuple[WorkflowRun, Artifact]:
        run = await self._get_run(workflow_run_id, db)

        # Get the requirement blueprint
        req_artifact = await self._get_artifact(requirement_artifact_id, db)

        step = await self._create_step(run.id, "ux", 2, db)

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "agent_start", "agent": "ux",
            "message": "UX Agent is designing user flows and screens...",
        })

        from app.pipeline.enricher.context_enricher import EnrichedContext
        context = EnrichedContext(**run.knowledge_context)
        plan = run.pipeline_context.get("plan", {})
        complexity = run.pipeline_context.get("intent", {}).get("complexity_score", 5)

        ux_tasks = [t for t in plan.get("sub_tasks", []) if t["agent"] == "ux"]
        instruction = ux_tasks[0]["instruction"] if ux_tasks else "Design the UX structure."

        result = await ux_agent.execute(
            instruction=instruction,
            context=context,
            complexity_score=complexity,
            extra_context={"requirement_blueprint": req_artifact.content},
            design_system_guidance=plan.get("design_system_guidance", ""),
        )

        artifact = await self._save_artifact(
            project_id=str(run.project_id),
            workflow_run_id=workflow_run_id,
            artifact_type=ArtifactType.USER_FLOW,
            name="UX Blueprint",
            content=result.output,
            agent_type="ux",
            model_used=result.model_selection.model_name,
            complexity_score=complexity,
            tokens_used=result.tokens_used,
            duration_ms=result.duration_ms,
            prompt=instruction,
            db=db,
        )

        await self._complete_step(step, result, db)
        gate = await self._create_approval_gate(workflow_run_id, str(artifact.id), "after_ux", db)

        run.current_step = "awaiting_approval_after_ux"
        run.status = WorkflowStatus.AWAITING_APPROVAL
        run.total_tokens += result.tokens_used
        await db.commit()

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "approval_required",
            "step": "ux",
            "gate_id": str(gate.id),
            "artifact_id": str(artifact.id),
            "message": "UX Blueprint ready for review",
        })

        return run, artifact

    async def run_ui_step(
        self, workflow_run_id: str, ux_artifact_id: str, req_artifact_id: str, db: AsyncSession
    ) -> tuple[WorkflowRun, Artifact]:
        run = await self._get_run(workflow_run_id, db)
        ux_artifact = await self._get_artifact(ux_artifact_id, db)
        req_artifact = await self._get_artifact(req_artifact_id, db)

        step = await self._create_step(run.id, "ui", 3, db)

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "agent_start", "agent": "ui",
            "message": "UI Agent is designing visual screens...",
        })

        from app.pipeline.enricher.context_enricher import EnrichedContext
        context = EnrichedContext(**run.knowledge_context)
        plan = run.pipeline_context.get("plan", {})
        complexity = run.pipeline_context.get("intent", {}).get("complexity_score", 5)

        ui_tasks = [t for t in plan.get("sub_tasks", []) if t["agent"] == "ui"]
        instruction = ui_tasks[0]["instruction"] if ui_tasks else "Design the visual UI."

        result = await ui_agent.execute(
            instruction=instruction,
            context=context,
            complexity_score=complexity,
            extra_context={
                "requirement_blueprint": req_artifact.content,
                "ux_blueprint": ux_artifact.content,
            },
            design_system_guidance=plan.get("design_system_guidance", ""),
        )

        artifact = await self._save_artifact(
            project_id=str(run.project_id),
            workflow_run_id=workflow_run_id,
            artifact_type=ArtifactType.HIFI_SCREEN,
            name="UI Blueprint",
            content=result.output,
            agent_type="ui",
            model_used=result.model_selection.model_name,
            complexity_score=complexity,
            tokens_used=result.tokens_used,
            duration_ms=result.duration_ms,
            prompt=instruction,
            db=db,
        )

        await self._complete_step(step, result, db)
        gate = await self._create_approval_gate(workflow_run_id, str(artifact.id), "after_ui", db)

        run.current_step = "awaiting_approval_after_ui"
        run.status = WorkflowStatus.AWAITING_APPROVAL
        run.total_tokens += result.tokens_used
        await db.commit()

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "approval_required",
            "step": "ui",
            "gate_id": str(gate.id),
            "artifact_id": str(artifact.id),
            "message": "UI Design ready for review",
        })

        return run, artifact

    async def run_review_step(
        self, workflow_run_id: str, ui_artifact_id: str, ux_artifact_id: str, req_artifact_id: str, db: AsyncSession
    ) -> tuple[WorkflowRun, Artifact]:
        run = await self._get_run(workflow_run_id, db)
        ui_artifact = await self._get_artifact(ui_artifact_id, db)
        ux_artifact = await self._get_artifact(ux_artifact_id, db)
        req_artifact = await self._get_artifact(req_artifact_id, db)

        step = await self._create_step(run.id, "review", 4, db)

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "agent_start", "agent": "review",
            "message": "Review Agent is validating design quality...",
        })

        from app.pipeline.enricher.context_enricher import EnrichedContext
        context = EnrichedContext(**run.knowledge_context)

        result = await review_agent.execute(
            instruction="Review all design artifacts for quality, accessibility, and compliance.",
            context=context,
            complexity_score=min(run.pipeline_context.get("intent", {}).get("complexity_score", 5), 5),
            extra_context={
                "requirement_blueprint": req_artifact.content,
                "ux_blueprint": ux_artifact.content,
                "ui_blueprint": ui_artifact.content,
            },
        )

        artifact = await self._save_artifact(
            project_id=str(run.project_id),
            workflow_run_id=workflow_run_id,
            artifact_type=ArtifactType.REVIEW_REPORT,
            name="Design Review Report",
            content=result.output,
            agent_type="review",
            model_used=result.model_selection.model_name,
            complexity_score=5,
            tokens_used=result.tokens_used,
            duration_ms=result.duration_ms,
            prompt="Design review",
            db=db,
        )

        await self._complete_step(step, result, db)

        run.current_step = "completed"
        run.status = WorkflowStatus.COMPLETED
        run.completed_at = datetime.now(timezone.utc)
        run.total_tokens += result.tokens_used
        await db.commit()

        # Save approved patterns to knowledge base for self-learning
        await self._save_approved_patterns(result.output, run, db)

        await ws_manager.broadcast_to_run(workflow_run_id, {
            "type": "workflow_complete",
            "score": result.output.get("overall_score"),
            "status": result.output.get("overall_status"),
            "artifact_id": str(artifact.id),
        })

        return run, artifact

    async def approve_gate(
        self, gate_id: str, user_id: str, status: str, comment: str, db: AsyncSession
    ) -> ApprovalGate:
        """Human approves or rejects an approval gate."""
        stmt = select(ApprovalGate).where(ApprovalGate.id == uuid.UUID(gate_id))
        result = await db.execute(stmt)
        gate = result.scalar_one_or_none()
        if not gate:
            raise ValueError(f"Gate {gate_id} not found")

        gate.status = ApprovalStatus(status)
        gate.reviewer_id = uuid.UUID(user_id)
        gate.reviewer_comment = comment
        gate.reviewed_at = datetime.now(timezone.utc)
        await db.commit()

        await ws_manager.broadcast_to_run(str(gate.workflow_run_id), {
            "type": "gate_decision",
            "gate_id": gate_id,
            "status": status,
            "message": f"Gate {gate.gate_type} → {status}",
        })

        return gate

    # Private helpers

    async def _get_run(self, run_id: str, db: AsyncSession) -> WorkflowRun:
        stmt = select(WorkflowRun).where(WorkflowRun.id == uuid.UUID(run_id))
        result = await db.execute(stmt)
        run = result.scalar_one_or_none()
        if not run:
            raise ValueError(f"WorkflowRun {run_id} not found")
        return run

    async def _get_artifact(self, artifact_id: str, db: AsyncSession) -> Artifact:
        stmt = select(Artifact).where(Artifact.id == uuid.UUID(artifact_id))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def _create_step(self, run_id, agent_type: str, order: int, db) -> WorkflowStep:
        step = WorkflowStep(
            workflow_run_id=run_id,
            agent_type=agent_type,
            order=order,
            status=StepStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        db.add(step)
        await db.commit()
        await db.refresh(step)
        return step

    async def _complete_step(self, step: WorkflowStep, result, db):
        step.status = StepStatus.COMPLETED
        step.model_used = result.model_selection.model_name
        step.complexity_score = result.model_selection.complexity_score
        step.tokens_used = result.tokens_used
        step.duration_ms = result.duration_ms
        step.output = result.output
        step.completed_at = datetime.now(timezone.utc)
        await db.commit()

    async def _save_artifact(
        self, project_id, workflow_run_id, artifact_type, name, content,
        agent_type, model_used, complexity_score, tokens_used, duration_ms, prompt, db
    ) -> Artifact:
        artifact = Artifact(
            project_id=uuid.UUID(project_id),
            workflow_run_id=uuid.UUID(workflow_run_id),
            name=name,
            type=artifact_type,
            status=ArtifactStatus.PENDING_APPROVAL,
            content=content,
            agent_type=agent_type,
            model_used=model_used,
            complexity_score=complexity_score,
            tokens_used=tokens_used,
            generation_time_ms=duration_ms,
            prompt=prompt,
        )
        db.add(artifact)
        await db.commit()
        await db.refresh(artifact)
        return artifact

    async def _create_approval_gate(self, workflow_run_id, artifact_id, gate_type, db) -> ApprovalGate:
        gate = ApprovalGate(
            workflow_run_id=uuid.UUID(workflow_run_id),
            artifact_id=uuid.UUID(artifact_id) if artifact_id else None,
            gate_type=gate_type,
            status=ApprovalStatus.PENDING,
        )
        db.add(gate)
        await db.commit()
        await db.refresh(gate)
        return gate

    async def _save_approved_patterns(self, review_output: dict, run: WorkflowRun, db):
        """Save approved patterns to knowledge base for future use (self-learning)."""
        patterns = review_output.get("approved_patterns", [])
        if not patterns:
            return

        from app.models.knowledge import KnowledgeDocument, KnowledgeDocStatus
        import json

        doc_content = "\n\n".join([
            f"APPROVED PATTERN:\n{pattern}" for pattern in patterns
        ])

        doc = KnowledgeDocument(
            uploaded_by=run.initiated_by,
            name=f"Approved Patterns — {run.title[:60]}",
            category="company",
            subcategory="approved-patterns",
            file_type="txt",
            status=KnowledgeDocStatus.PROCESSING,
            doc_metadata={"auto_generated": True, "workflow_run_id": str(run.id)},
        )
        db.add(doc)
        await db.commit()
        await db.refresh(doc)

        # Index the patterns
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(doc_content)
            tmp_path = f.name

        try:
            from app.knowledge.indexer.document_indexer import index_document
            await index_document(
                document_id=str(doc.id),
                file_path=tmp_path,
                file_type="txt",
                category="company",
                subcategory="approved-patterns",
                db=db,
            )
        finally:
            os.unlink(tmp_path)


    async def run_pipeline_and_planner(self, workflow_run_id: str, db) -> None:
        """Combined step: run pipeline then immediately run planner."""
        try:
            run = await self.run_pipeline_step(workflow_run_id, db)
            await self.run_planner_step(workflow_run_id, db)
        except Exception as e:
            logger.error("workflow_failed", run_id=workflow_run_id, error=str(e))
            try:
                run = await self._get_run(workflow_run_id, db)
                run.status = WorkflowStatus.FAILED
                run.error_message = str(e)
                await db.commit()
                await ws_manager.broadcast_to_run(workflow_run_id, {
                    "type": "error", "message": str(e)
                })
            except Exception:
                pass


workflow_service = WorkflowService()
