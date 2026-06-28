"""
Research Agent — personas, competitor analysis, market research, user stories, PRD.
Supports optional screen image input: vision LLM extracts UI context before research.
RAG checks org knowledge docs for compliance on every response.
"""
import json
import re
from typing import Optional


RESEARCH_SYSTEM = """You are a senior product researcher and UX strategist with deep expertise
in user research, competitive analysis, and product strategy. You produce precise,
actionable research backed by domain knowledge. Return only valid JSON."""


async def _analyze_screen_image(image_b64: str, research_type: str, llm_chat_vision) -> str:
    """Use vision LLM to extract UI context from an uploaded screen image."""
    focus_map = {
        "user_stories":  "user interface elements, user actions, form fields, navigation, and user goals visible",
        "personas":      "the type of user this UI targets, use patterns, complexity level, and demographic signals",
        "competitor":    "product category, key features, design patterns, value proposition, and market positioning",
        "prd":           "all visible features, functionality, user flows, data fields, and system requirements",
        "market":        "the market segment, user needs, product category, and competitive landscape",
        "user_flow":     "all screens, navigation paths, user actions, decision points, and interactive elements",
        "journey_map":   "the user journey stages, touchpoints, emotions, and pain points visible",
        "task_flow":     "the specific task steps, actions, inputs, and outcomes visible",
        "service_blueprint": "all visible service layers, user actions, system processes, and touchpoints",
    }
    focus = focus_map.get(research_type, "all UI elements, user flows, and functionality")

    prompt = f"""You are analyzing a UI screen or product screenshot for research purposes.

Describe in detail:
1. WHAT THE SCREEN IS: Page type, product category, industry/domain
2. KEY UI ELEMENTS: All visible components (buttons, forms, nav, cards, modals, etc.)
3. USER ACTIONS: What a user can do on this screen
4. INFORMATION ARCHITECTURE: How content is organized and what sections exist
5. FUNCTIONAL FLOWS: Any visible multi-step flows, decision points, or state changes
6. SPECIFIC FOCUS — {focus}

Be specific and thorough. This description will be used to generate {research_type.replace("_", " ")} research.
Format as clear paragraphs, not JSON."""

    try:
        description = await llm_chat_vision(image_b64, prompt)
        return description.strip() if description else ""
    except Exception as e:
        return f"[Vision analysis unavailable: {e}]"


async def _check_rag_compliance(result: dict, topic: str, rag_query) -> dict:
    """Check org knowledge docs for any compliance requirements relevant to this research."""
    try:
        compliance_docs = await rag_query("documents", f"compliance requirements {topic}", top_k=3)
        standards_docs  = await rag_query("guidelines", f"standards policy {topic}", top_k=2)
        all_docs = [d for d in (compliance_docs + standards_docs) if d and len(d) > 50]

        if not all_docs:
            return result

        # Inject compliance notes into result
        compliance_notes = []
        for doc in all_docs[:3]:
            snippet = doc[:300].strip()
            if snippet:
                compliance_notes.append(snippet)

        if compliance_notes:
            result["rag_compliance_notes"] = {
                "source": "Organization knowledge base",
                "notes": compliance_notes,
                "guidance": "These excerpts from your organization's documents are relevant to this research.",
            }
    except Exception:
        pass
    return result


async def run_research(
    research_type: str,  # personas | competitor | market | user_stories | prd
    topic: str,
    domain: str,
    context: str,
    llm_chat,
    select_model,
    rag_query,
    image_b64: Optional[str] = None,
    llm_chat_vision=None,
) -> dict:
    """
    Research agent — routes to right sub-task based on research_type.
    If image_b64 is provided, vision-analyzes it first to enrich context.
    Always checks org RAG docs for compliance at the end.
    """
    model = select_model(6, "research")

    # Vision analysis — extract UI context from image if provided
    image_context = ""
    if image_b64 and llm_chat_vision:
        image_context = await _analyze_screen_image(image_b64, research_type, llm_chat_vision)

    # Merge image context into the user context
    enriched_context = context
    if image_context:
        enriched_context = f"{context}\n\nSCREEN ANALYSIS FROM UPLOADED IMAGE:\n{image_context}".strip()

    # RAG enrichment
    domain_docs  = await rag_query("guidelines", f"{domain} {topic}", top_k=3)
    rag_context  = "\n".join(domain_docs[:3]) or "No domain knowledge found — use general best practices."

    if research_type == "personas":
        result = await _run_personas(topic, domain, enriched_context, rag_context, model, llm_chat)
    elif research_type == "competitor":
        result = await _run_competitor(topic, domain, enriched_context, rag_context, model, llm_chat)
    elif research_type == "market":
        result = await _run_market(topic, domain, enriched_context, rag_context, model, llm_chat)
    elif research_type == "user_stories":
        result = await _run_user_stories(topic, domain, enriched_context, rag_context, model, llm_chat)
    elif research_type == "prd":
        result = await _run_prd(topic, domain, enriched_context, rag_context, model, llm_chat)
    else:
        return {"error": f"Unknown research type: {research_type}"}

    # Flag whether image was used
    if image_b64:
        result["_image_analyzed"] = True
        result["_image_context_summary"] = image_context[:200] + "..." if len(image_context) > 200 else image_context

    # RAG compliance check
    result = await _check_rag_compliance(result, topic, rag_query)

    return result


async def _run_personas(topic, domain, context, rag_context, model, llm_chat) -> dict:
    prompt = f"""You are a UX researcher creating detailed user personas.

PRODUCT: {topic}
DOMAIN: {domain}
CONTEXT: {context}

DOMAIN KNOWLEDGE:
{rag_context}

Create 3 distinct user personas. Return ONLY valid JSON:
{{
  "research_type": "personas",
  "topic": "{topic}",
  "personas": [
    {{
      "id": "persona-1",
      "name": "Full name",
      "age": 35,
      "role": "Job title",
      "photo_description": "Brief description for avatar generation",
      "quote": "A quote that captures their mindset about this product",
      "background": "2-3 sentences about their background",
      "goals": ["Primary goal", "Secondary goal", "Tertiary goal"],
      "frustrations": ["Key pain point", "Secondary pain point"],
      "motivations": ["What drives them", "What they value"],
      "tech_savviness": "low | medium | high",
      "frequency_of_use": "daily | weekly | monthly | occasional",
      "key_scenarios": [
        {{"scenario": "Specific situation they use this product", "need": "What they need in this moment"}}
      ],
      "success_criteria": "What does success look like for this persona?"
    }}
  ],
  "design_implications": ["Implication for UI/UX based on these personas"],
  "research_confidence": "high | medium | low"
}}"""
    raw = await llm_chat(RESEARCH_SYSTEM, prompt, model)
    return _parse_or_fallback(raw, "personas", topic)


async def _run_competitor(topic, domain, context, rag_context, model, llm_chat) -> dict:
    prompt = f"""You are a product strategist conducting competitive analysis.

PRODUCT: {topic}
DOMAIN: {domain}
CONTEXT: {context}

INDUSTRY KNOWLEDGE:
{rag_context}

Analyse 4 competitors or comparable products. Return ONLY valid JSON:
{{
  "research_type": "competitor",
  "topic": "{topic}",
  "market_overview": "2-3 sentence market landscape summary",
  "competitors": [
    {{
      "name": "Competitor name",
      "category": "Direct | Indirect | Aspirational",
      "description": "What they do",
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "key_features": ["Feature 1", "Feature 2", "Feature 3"],
      "target_audience": "Who they serve",
      "pricing_model": "Free | Freemium | Subscription | One-time",
      "ux_quality": "Excellent | Good | Average | Poor",
      "notable_patterns": ["UI/UX pattern worth noting"]
    }}
  ],
  "market_gaps": ["Gap in the market we can exploit"],
  "differentiation_opportunities": [
    {{"opportunity": "How we can differentiate", "impact": "high | medium | low"}}
  ],
  "recommended_features": ["Feature to prioritise based on analysis"],
  "research_confidence": "high | medium | low"
}}"""
    raw = await llm_chat(RESEARCH_SYSTEM, prompt, model)
    return _parse_or_fallback(raw, "competitor", topic)


async def _run_user_stories(topic, domain, context, rag_context, model, llm_chat) -> dict:
    # If image context is embedded, prompt explicitly instructs to use it
    image_note = ""
    if "SCREEN ANALYSIS FROM UPLOADED IMAGE:" in context:
        image_note = "\nIMPORTANT: Generate user stories that specifically reflect the UI elements and flows visible in the screen analysis above."

    prompt = f"""You are a Business Analyst creating detailed user stories with acceptance criteria.

PRODUCT/FEATURE: {topic}
DOMAIN: {domain}
CONTEXT: {context}{image_note}

DOMAIN KNOWLEDGE:
{rag_context}

Create comprehensive user stories. Return ONLY valid JSON:
{{
  "research_type": "user_stories",
  "epic": "{topic}",
  "epic_description": "One sentence description of this epic",
  "user_stories": [
    {{
      "id": "US-001",
      "title": "Story title",
      "as_a": "type of user",
      "i_want": "goal/desire",
      "so_that": "benefit/value",
      "priority": "Must Have | Should Have | Could Have | Won't Have",
      "story_points": 3,
      "acceptance_criteria": [
        "Given [context], When [action], Then [outcome]"
      ],
      "edge_cases": ["Edge case to handle"],
      "dependencies": ["US-00X"],
      "notes": "Additional context for developers"
    }}
  ],
  "definition_of_done": ["DoD criterion that applies to all stories in this epic"],
  "out_of_scope": ["Explicitly not included in this epic"],
  "total_story_points": 0
}}

Generate at least 5 user stories covering the happy path and key edge cases."""

    raw = await llm_chat(RESEARCH_SYSTEM, prompt, model)
    result = _parse_or_fallback(raw, "user_stories", topic)
    if "user_stories" in result:
        result["total_story_points"] = sum(s.get("story_points", 0) for s in result["user_stories"])
    return result


async def _run_prd(topic, domain, context, rag_context, model, llm_chat) -> dict:
    prompt = f"""You are a Senior Product Manager writing a Product Requirements Document.

PRODUCT/FEATURE: {topic}
DOMAIN: {domain}
CONTEXT: {context}

DOMAIN KNOWLEDGE:
{rag_context}

Write a comprehensive PRD. Return ONLY valid JSON:
{{
  "research_type": "prd",
  "title": "{topic} — Product Requirements Document",
  "version": "1.0",
  "status": "Draft",
  "executive_summary": "3-4 sentence overview",
  "problem_statement": "What problem are we solving and for whom",
  "objectives": [
    {{"objective": "Measurable objective", "metric": "How we measure success", "target": "Target value"}}
  ],
  "target_users": ["User segment 1", "User segment 2"],
  "scope": {{
    "in_scope": ["Feature/capability included"],
    "out_of_scope": ["Explicitly excluded"]
  }},
  "functional_requirements": [
    {{
      "id": "FR-001",
      "category": "Category name",
      "requirement": "The system shall...",
      "priority": "P1 | P2 | P3",
      "rationale": "Why this is required"
    }}
  ],
  "non_functional_requirements": [
    {{
      "category": "Performance | Security | Accessibility | Compliance",
      "requirement": "The system shall...",
      "standard": "Reference standard e.g. WCAG 2.1 AA"
    }}
  ],
  "constraints": ["Technical or business constraint"],
  "assumptions": ["Assumption made in writing this PRD"],
  "risks": [
    {{"risk": "Risk description", "impact": "high | medium | low", "mitigation": "How to mitigate"}}
  ],
  "success_metrics": [
    {{"metric": "KPI name", "baseline": "Current value", "target": "Target value", "timeline": "When"}}
  ],
  "timeline": {{
    "discovery": "Duration", "design": "Duration",
    "development": "Duration", "testing": "Duration", "launch": "Target date"
  }}
}}"""
    raw = await llm_chat(RESEARCH_SYSTEM, prompt, model)
    return _parse_or_fallback(raw, "prd", topic)


async def _run_market(topic, domain, context, rag_context, model, llm_chat) -> dict:
    prompt = f"""You are a market research analyst.

TOPIC: {topic}
DOMAIN: {domain}
CONTEXT: {context}

DOMAIN KNOWLEDGE:
{rag_context}

Create a market research report. Return ONLY valid JSON:
{{
  "research_type": "market",
  "topic": "{topic}",
  "market_size": "Estimated market size and growth",
  "trends": [
    {{"trend": "Market trend", "impact": "high | medium | low", "timeframe": "Now | 1yr | 3yr"}}
  ],
  "user_needs": [
    {{"need": "User need", "frequency": "Always | Often | Sometimes", "pain_level": "Critical | High | Medium | Low"}}
  ],
  "regulatory_considerations": ["Relevant regulation or compliance requirement"],
  "technology_enablers": ["Technology making this product possible"],
  "key_insights": ["Strategic insight for product development"],
  "recommendations": ["Actionable recommendation"]
}}"""
    raw = await llm_chat(RESEARCH_SYSTEM, prompt, model)
    return _parse_or_fallback(raw, "market", topic)


def _parse_or_fallback(raw: str, research_type: str, topic: str) -> dict:
    text = raw.strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    for prefix in ("```json", "```"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    if text.endswith("```"):
        text = text[:-3]
    try:
        data = json.loads(text.strip())
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return {
        "research_type": research_type,
        "topic": topic,
        "error": "LLM parse failed — retry with more specific prompt",
        "raw_output": raw[:500],
    }
