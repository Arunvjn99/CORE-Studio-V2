"""Artifact endpoints — view, approve, get content."""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.artifact import Artifact, ArtifactStatus

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.get("/{artifact_id}")
async def get_artifact(
    artifact_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Artifact).where(Artifact.id == uuid.UUID(artifact_id))
    result = await db.execute(stmt)
    artifact = result.scalar_one_or_none()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    return {
        "id": str(artifact.id),
        "name": artifact.name,
        "type": artifact.type,
        "status": artifact.status,
        "content": artifact.content,
        "raw_output": artifact.raw_output,
        "agent_type": artifact.agent_type,
        "model_used": artifact.model_used,
        "complexity_score": artifact.complexity_score,
        "tokens_used": artifact.tokens_used,
        "generation_time_ms": artifact.generation_time_ms,
        "version": artifact.version,
        "created_at": artifact.created_at.isoformat(),
    }


class ApproveArtifactRequest(BaseModel):
    status: str  # approved | rejected
    comment: Optional[str] = None


@router.post("/{artifact_id}/approve")
async def approve_artifact(
    artifact_id: str,
    req: ApproveArtifactRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Artifact).where(Artifact.id == uuid.UUID(artifact_id))
    result = await db.execute(stmt)
    artifact = result.scalar_one_or_none()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    artifact.status = ArtifactStatus(req.status)
    await db.commit()

    return {"id": str(artifact.id), "status": artifact.status}
