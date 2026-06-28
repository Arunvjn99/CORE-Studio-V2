import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SAEnum, JSON, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db.base import Base


class WorkflowStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGES_REQUESTED = "changes_requested"


class WorkflowRun(Base):
    """Represents a single end-to-end design generation run."""
    __tablename__ = "workflow_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    initiated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[WorkflowStatus] = mapped_column(SAEnum(WorkflowStatus), default=WorkflowStatus.PENDING)
    current_step: Mapped[str | None] = mapped_column(String(50), nullable=True)  # planner, ux, ui, review

    # Original user input
    starting_point: Mapped[str] = mapped_column(String(50), nullable=False)
    work_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    user_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    input_files: Mapped[list] = mapped_column(JSON, default=list)

    # Decomposed pipeline context
    pipeline_context: Mapped[dict] = mapped_column(JSON, default=dict)
    knowledge_context: Mapped[dict] = mapped_column(JSON, default=dict)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_time_ms: Mapped[int] = mapped_column(Integer, default=0)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="workflow_runs")
    steps: Mapped[list["WorkflowStep"]] = relationship("WorkflowStep", back_populates="workflow_run", cascade="all, delete-orphan", order_by="WorkflowStep.order")
    artifacts: Mapped[list["Artifact"]] = relationship("Artifact", back_populates="workflow_run")
    approval_gates: Mapped[list["ApprovalGate"]] = relationship("ApprovalGate", back_populates="workflow_run", cascade="all, delete-orphan")


class WorkflowStep(Base):
    """Individual agent step within a workflow run."""
    __tablename__ = "workflow_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id"), nullable=False)

    agent_type: Mapped[str] = mapped_column(String(50), nullable=False)  # planner, ux, ui, review
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[StepStatus] = mapped_column(SAEnum(StepStatus), default=StepStatus.PENDING)

    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    complexity_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    input_context: Mapped[dict] = mapped_column(JSON, default=dict)
    output: Mapped[dict] = mapped_column(JSON, default=dict)
    stream_log: Mapped[list] = mapped_column(JSON, default=list)  # streaming tokens log

    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    workflow_run: Mapped["WorkflowRun"] = relationship("WorkflowRun", back_populates="steps")


class ApprovalGate(Base):
    """Human-in-the-loop approval checkpoint."""
    __tablename__ = "approval_gates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id"), nullable=False)
    artifact_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("artifacts.id"), nullable=True)

    gate_type: Mapped[str] = mapped_column(String(50), nullable=False)  # after_planner, after_ux, after_ui, after_review
    status: Mapped[ApprovalStatus] = mapped_column(SAEnum(ApprovalStatus), default=ApprovalStatus.PENDING)

    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reviewer_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    change_requests: Mapped[list] = mapped_column(JSON, default=list)

    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    workflow_run: Mapped["WorkflowRun"] = relationship("WorkflowRun", back_populates="approval_gates")
    artifact: Mapped["Artifact | None"] = relationship("Artifact", back_populates="approval_gates")
