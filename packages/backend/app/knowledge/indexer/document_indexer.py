"""
Document Indexer — Processes uploaded files into searchable vector chunks.

Supports: PDF, DOCX, MD, TXT
Chunks intelligently (preserving semantic boundaries)
Generates embeddings via OpenAI text-embedding-3-small
"""
import uuid
import re
from pathlib import Path
from typing import AsyncGenerator
import structlog

from app.core.config import settings

logger = structlog.get_logger()

CHUNK_SIZE = 800       # chars per chunk
CHUNK_OVERLAP = 150    # overlap between chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks, preserving paragraph boundaries."""
    # Split on paragraphs first
    paragraphs = re.split(r'\n\s*\n', text.strip())
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) < chunk_size:
            current += "\n\n" + para if current else para
        else:
            if current:
                chunks.append(current.strip())
            # Start new chunk with overlap from previous
            if current and overlap > 0:
                overlap_text = current[-overlap:]
                current = overlap_text + "\n\n" + para
            else:
                current = para

    if current:
        chunks.append(current.strip())

    return [c for c in chunks if len(c) > 50]  # Filter tiny chunks


async def extract_text(file_path: str, file_type: str) -> str:
    """Extract plain text from various file types."""
    path = Path(file_path)

    if file_type in ("txt", "md"):
        return path.read_text(encoding="utf-8", errors="ignore")

    elif file_type == "pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            text = "\n\n".join(
                page.extract_text() or "" for page in reader.pages
            )
            return text
        except Exception as e:
            logger.error("pdf_extraction_failed", error=str(e))
            return ""

    elif file_type == "docx":
        try:
            import docx
            doc = docx.Document(str(path))
            text = "\n\n".join(para.text for para in doc.paragraphs if para.text)
            return text
        except Exception as e:
            logger.error("docx_extraction_failed", error=str(e))
            return ""

    return ""


async def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings using OpenAI."""
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    # Batch in groups of 100
    all_embeddings = []
    batch_size = 100

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = await client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=batch,
        )
        all_embeddings.extend([item.embedding for item in response.data])

    return all_embeddings


async def index_document(
    document_id: str,
    file_path: str,
    file_type: str,
    category: str,
    subcategory: str | None,
    db,
) -> int:
    """
    Full pipeline: extract → chunk → embed → store.
    Returns number of chunks indexed.
    """
    from app.models.knowledge import KnowledgeChunk, KnowledgeDocument, KnowledgeDocStatus
    from sqlalchemy import select

    logger.info("indexing_start", document_id=document_id, file_type=file_type)

    # Extract text
    text = await extract_text(file_path, file_type)
    if not text.strip():
        logger.warning("empty_document", document_id=document_id)
        return 0

    # Chunk
    chunks = chunk_text(text)
    if not chunks:
        return 0

    # Embed
    try:
        embeddings = await generate_embeddings(chunks)
    except Exception as e:
        logger.error("embedding_failed", error=str(e))
        # Store without embeddings if embedding fails
        embeddings = [None] * len(chunks)

    # Store chunks
    chunk_records = []
    for i, (chunk_text_content, embedding) in enumerate(zip(chunks, embeddings)):
        chunk = KnowledgeChunk(
            id=uuid.uuid4(),
            document_id=uuid.UUID(document_id),
            content=chunk_text_content,
            embedding=embedding,
            chunk_index=i,
            chunk_metadata={
                "category": category,
                "subcategory": subcategory,
                "char_count": len(chunk_text_content),
            }
        )
        chunk_records.append(chunk)

    db.add_all(chunk_records)

    # Update document status
    stmt = select(KnowledgeDocument).where(KnowledgeDocument.id == uuid.UUID(document_id))
    result = await db.execute(stmt)
    doc = result.scalar_one_or_none()
    if doc:
        doc.status = KnowledgeDocStatus.INDEXED
        doc.chunk_count = len(chunk_records)

    await db.commit()

    logger.info("indexing_complete", document_id=document_id, chunks=len(chunk_records))
    return len(chunk_records)
