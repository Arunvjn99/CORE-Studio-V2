"""
RAG Retriever — Semantic search over knowledge chunks using pgvector.
"""
from typing import Optional
import structlog
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

logger = structlog.get_logger()


async def get_query_embedding(query: str) -> list[float]:
    """Generate embedding for a search query."""
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    response = await client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=query,
    )
    return response.data[0].embedding


async def retrieve_relevant_chunks(
    query: str,
    category: str | None = None,
    subcategory: str | None = None,
    top_k: int = 5,
    similarity_threshold: float = 0.7,
    db: AsyncSession = None,
) -> list[dict]:
    """
    Retrieve the most relevant knowledge chunks for a query.
    Uses cosine similarity via pgvector.
    """
    if not db:
        return []

    try:
        query_embedding = await get_query_embedding(query)

        # Build filter conditions
        filters = []
        params: dict = {
            "embedding": query_embedding,
            "threshold": 1 - similarity_threshold,  # pgvector uses L2 distance
            "top_k": top_k,
        }

        if category:
            filters.append("kd.category = :category")
            params["category"] = category

        if subcategory:
            filters.append("kd.subcategory = :subcategory")
            params["subcategory"] = subcategory

        where_clause = ("WHERE " + " AND ".join(filters)) if filters else ""

        sql = text(f"""
            SELECT
                kc.id::text,
                kc.content,
                kc.chunk_metadata,
                kd.name as document_name,
                kd.category,
                kd.subcategory,
                1 - (kc.embedding <=> :embedding::vector) as similarity
            FROM knowledge_chunks kc
            JOIN knowledge_documents kd ON kd.id = kc.document_id
            {where_clause}
            AND kc.embedding IS NOT NULL
            AND kd.status = 'indexed'
            ORDER BY kc.embedding <=> :embedding::vector
            LIMIT :top_k
        """)

        result = await db.execute(sql, params)
        rows = result.fetchall()

        return [
            {
                "id": row.id,
                "content": row.content,
                "document_name": row.document_name,
                "category": row.category,
                "subcategory": row.subcategory,
                "similarity": float(row.similarity),
                "metadata": row.chunk_metadata,
            }
            for row in rows
            if float(row.similarity) >= similarity_threshold
        ]

    except Exception as e:
        logger.error("rag_retrieval_failed", error=str(e))
        return []
