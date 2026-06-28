"""Knowledge management endpoints — upload, index, search."""
import uuid
import os
import aiofiles
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.db.base import get_db
from app.core.deps import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.knowledge import KnowledgeDocument, KnowledgeCategory, KnowledgeDocStatus
from app.knowledge.indexer.document_indexer import index_document

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

ALLOWED_TYPES = {"pdf", "docx", "txt", "md"}


@router.post("/upload", status_code=201)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    category: str = Form(...),
    subcategory: str = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a knowledge document and trigger background indexing."""
    # Validate file type
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"File type .{ext} not supported")

    # Validate category
    try:
        cat = KnowledgeCategory(category)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    # Save file
    uploads_dir = Path(settings.UPLOADS_DIR) / "knowledge"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    file_id = str(uuid.uuid4())
    file_path = uploads_dir / f"{file_id}.{ext}"

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")

    async with aiofiles.open(str(file_path), "wb") as f:
        await f.write(content)

    # Create document record
    doc = KnowledgeDocument(
        id=uuid.uuid4(),
        uploaded_by=current_user.id,
        name=file.filename,
        category=cat,
        subcategory=subcategory,
        file_path=str(file_path),
        file_type=ext,
        file_size_bytes=len(content),
        status=KnowledgeDocStatus.PROCESSING,
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    # Index in background
    background_tasks.add_task(
        index_document,
        str(doc.id), str(file_path), ext, category, subcategory, db
    )

    return {
        "document_id": str(doc.id),
        "name": doc.name,
        "category": category,
        "status": "processing",
    }


@router.get("/")
async def list_documents(
    category: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(KnowledgeDocument)
    if category:
        stmt = stmt.where(KnowledgeDocument.category == category)
    stmt = stmt.order_by(KnowledgeDocument.created_at.desc())

    result = await db.execute(stmt)
    docs = result.scalars().all()

    return [
        {
            "id": str(d.id),
            "name": d.name,
            "category": d.category,
            "subcategory": d.subcategory,
            "file_type": d.file_type,
            "status": d.status,
            "chunk_count": d.chunk_count,
            "created_at": d.created_at.isoformat(),
        }
        for d in docs
    ]


class SearchRequest(BaseModel):
    query: str
    category: str = None
    subcategory: str = None
    top_k: int = 5


@router.post("/search")
async def search_knowledge(
    req: SearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Semantic search over knowledge base."""
    from app.knowledge.retriever.rag_retriever import retrieve_relevant_chunks

    results = await retrieve_relevant_chunks(
        query=req.query,
        category=req.category,
        subcategory=req.subcategory,
        top_k=req.top_k,
        db=db,
    )
    return {"results": results, "count": len(results)}


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(KnowledgeDocument).where(KnowledgeDocument.id == uuid.UUID(doc_id))
    result = await db.execute(stmt)
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.file_path and os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    await db.delete(doc)
    await db.commit()
    return {"deleted": True}
