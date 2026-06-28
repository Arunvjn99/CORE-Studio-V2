import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SAEnum, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db.base import Base


class ArtifactType(str, enum.Enum):
    REQUIREMENT = "requirement"
    USER_FLOW = "user_flow"
    WIREFRAME = "wireframe"
    HIFI_SCREEN = "hifi_screen"
    COMPONENT = "component"
    DESIGN_SYSTEM = "design_system"
    REVIEW_REPORT = "review_report"
    CODE_REACT = "code_react"
    CODE_HTML = "code_html"
    DOCUMENTATION = "documentation"


class ArtifactStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class StartingPoint(str, enum.Enum):
    PROJECT = "project"
    REQUIREMENT = "requirement"
    USER_FLOW = "user_flow"
    EXISTING_SCREEN = "existing_screen"


class WorkMode(str, enum.Enum):
    CREATE = "create"
    IMPROVE = "improve"
    RECREATE = "recreate"


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("artifacts.id"), nullable=True)
    workflow_run_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workflow_runs.id"), nullable=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[ArtifactType] = mapped_column(SAEnum(ArtifactType), nullable=False)
    status: Mapped[ArtifactStatus] = mapped_column(SAEnum(ArtifactStatus), default=ArtifactStatus.DRAFT)
    starting_point: Mapped[StartingPoint | None] = mapped_column(SAEnum(StartingPoint), nullable=True)
    work_mode: Mapped[WorkMode | None] = mapped_column(SAEnum(WorkMode), nullable=True)

    # Content — structured output from agents
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    raw_output: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Input that generated this artifact
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_files: Mapped[list] = mapped_column(JSON, default=list)  # uploaded file refs

    # Agent metadata
    agent_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # planner, ux, ui, review
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    complexity_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    generation_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Version control
    version: Mapped[int] = mapped_column(Integer, default=1)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="artifacts")
    parent: Mapped["Artifact | None"] = relationship("Artifact", remote_side="Artifact.id", back_populates="children")
    children: Mapped[list["Artifact"]] = relationship("Artifact", back_populates="parent")
    workflow_run: Mapped["WorkflowRun | None"] = relationship("WorkflowRun", back_populates="artifacts")
    approval_gates: Mapped[list["ApprovalGate"]] = relationship("ApprovalGate", back_populates="artifact", cascade="all, delete-orphan")
