"""Project endpoints."""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectStatus, ProjectDomain

router = APIRouter(prefix="/projects", tags=["projects"])


class CreateProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
    domain: str = "other"


class UpdateProjectRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    status: Optional[str] = None


@router.post("/", status_code=201)
async def create_project(
    req: CreateProjectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = Project(
        id=uuid.uuid4(),
        owner_id=current_user.id,
        name=req.name,
        description=req.description,
        domain=ProjectDomain(req.domain),
        status=ProjectStatus.ACTIVE,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return _project_dict(project)


@router.get("/")
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Project).where(
        Project.owner_id == current_user.id,
        Project.status != ProjectStatus.ARCHIVED,
    ).order_by(Project.updated_at.desc())
    result = await db.execute(stmt)
    projects = result.scalars().all()
    return [_project_dict(p) for p in projects]


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Project).where(Project.id == uuid.UUID(project_id))
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return _project_dict(project)


@router.get("/{project_id}/artifacts")
async def get_project_artifacts(
    project_id: str,
    artifact_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.models.artifact import Artifact
    stmt = select(Artifact).where(Artifact.project_id == uuid.UUID(project_id))
    if artifact_type:
        stmt = stmt.where(Artifact.type == artifact_type)
    stmt = stmt.order_by(Artifact.created_at.desc())
    result = await db.execute(stmt)
    artifacts = result.scalars().all()

    return [
        {
            "id": str(a.id),
            "name": a.name,
            "type": a.type,
            "status": a.status,
            "agent_type": a.agent_type,
            "model_used": a.model_used,
            "complexity_score": a.complexity_score,
            "tokens_used": a.tokens_used,
            "version": a.version,
            "created_at": a.created_at.isoformat(),
        }
        for a in artifacts
    ]


@router.put("/{project_id}")
async def update_project(
    project_id: str,
    req: UpdateProjectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Project).where(Project.id == uuid.UUID(project_id), Project.owner_id == current_user.id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if req.name: project.name = req.name
    if req.description: project.description = req.description
    if req.domain: project.domain = ProjectDomain(req.domain)
    if req.status: project.status = ProjectStatus(req.status)

    await db.commit()
    await db.refresh(project)
    return _project_dict(project)


def _project_dict(p: Project) -> dict:
    return {
        "id": str(p.id),
        "name": p.name,
        "description": p.description,
        "domain": p.domain,
        "status": p.status,
        "created_at": p.created_at.isoformat(),
        "updated_at": p.updated_at.isoformat(),
    }
