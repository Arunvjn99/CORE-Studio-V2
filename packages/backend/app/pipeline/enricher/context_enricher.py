"""
Context Enricher — Step 3 of the Prompt Pipeline.

Fetches relevant knowledge from the RAG system and injects it
into the agent context BEFORE agents are invoked.

This ensures agents always work with:
- Domain-specific knowledge (retirement rules, loan terminology, etc.)
- Company standards (UX guidelines, accessibility rules)
- Design system context (token values, component patterns)
- Historical approved patterns (self-learning from past approvals)
"""
from pydantic import BaseModel

from app.pipeline.intent.classifier import IntentResult
from app.pipeline.decomposer.task_decomposer import DecomposedPlan


class EnrichedContext(BaseModel):
    domain_knowledge: list[dict]  # Retrieved domain chunks
    company_standards: list[dict]  # Retrieved company policy chunks
    design_system_rules: list[dict]  # Retrieved design system chunks
    approved_patterns: list[dict]  # Past approved similar patterns
    context_summary: str  # Synthesized context string for agent prompts


async def enrich_context(
    intent: IntentResult,
    plan: DecomposedPlan,
    db=None,  # AsyncSession
) -> EnrichedContext:
    """
    Retrieve and inject relevant knowledge for a workflow run.
    Falls back gracefully if RAG retrieval is unavailable.
    """
    domain_chunks = []
    company_chunks = []
    design_system_chunks = []
    approved_chunks = []

    if db:
        try:
            from app.knowledge.retriever.rag_retriever import retrieve_relevant_chunks

            # Domain knowledge
            if intent.domain != "general":
                domain_chunks = await retrieve_relevant_chunks(
                    query=f"{intent.domain} {' '.join(intent.key_entities)}",
                    category="domain",
                    subcategory=intent.domain,
                    top_k=5,
                    db=db,
                )

            # Company standards (always retrieved)
            company_chunks = await retrieve_relevant_chunks(
                query=f"UX standards accessibility compliance {intent.intent_type}",
                category="company",
                top_k=4,
                db=db,
            )

            # Design system
            design_system_chunks = await retrieve_relevant_chunks(
                query=f"components typography colors spacing {' '.join(intent.key_entities)}",
                category="design_system",
                top_k=4,
                db=db,
            )

        except Exception as e:
            # Non-fatal — agents work without RAG, just with less context
            pass

    # Build context summary for agent prompts
    summary_parts = []

    if domain_chunks:
        domain_text = "\n".join([c["content"][:300] for c in domain_chunks[:3]])
        summary_parts.append(f"DOMAIN KNOWLEDGE ({intent.domain.upper()}):\n{domain_text}")

    if company_chunks:
        company_text = "\n".join([c["content"][:300] for c in company_chunks[:2]])
        summary_parts.append(f"COMPANY STANDARDS:\n{company_text}")

    if design_system_chunks:
        ds_text = "\n".join([c["content"][:300] for c in design_system_chunks[:2]])
        summary_parts.append(f"DESIGN SYSTEM RULES:\n{ds_text}")

    if approved_chunks:
        ap_text = "\n".join([c["content"][:200] for c in approved_chunks[:2]])
        summary_parts.append(f"PREVIOUSLY APPROVED PATTERNS:\n{ap_text}")

    context_summary = "\n\n".join(summary_parts) if summary_parts else (
        f"No specific organizational knowledge found for {intent.domain}. "
        "Apply general UX best practices and accessibility standards."
    )

    return EnrichedContext(
        domain_knowledge=domain_chunks,
        company_standards=company_chunks,
        design_system_rules=design_system_chunks,
        approved_patterns=approved_chunks,
        context_summary=context_summary,
    )
