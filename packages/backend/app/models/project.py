import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db.base import Base


class ProjectStatus(str, enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    COMPLETED = "completed"


class ProjectDomain(str, enum.Enum):
    RETIREMENT = "retirement"
    LOAN = "loan"
    INSURANCE = "insurance"
    HEALTHCARE = "healthcare"
    BANKING = "banking"
    OTHER = "other"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    domain: Mapped[ProjectDomain] = mapped_column(SAEnum(ProjectDomain), default=ProjectDomain.OTHER)
    status: Mapped[ProjectStatus] = mapped_column(SAEnum(ProjectStatus), default=ProjectStatus.ACTIVE)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    figma_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="projects")
    artifacts: Mapped[list["Artifact"]] = relationship("Artifact", back_populates="project", cascade="all, delete-orphan")
    workflow_runs: Mapped[list["WorkflowRun"]] = relationship("WorkflowRun", back_populates="project", cascade="all, delete-orphan")
