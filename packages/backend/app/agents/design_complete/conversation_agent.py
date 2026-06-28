"""
Conversational Design Agent — UX Magic-style two-phase workflow:

1. PLAN phase  → Agent analyzes prompt, shows thought process, plans N screens
                 User approves/rejects/edits the plan before generation
2. GENERATE   → Agent generates only the approved screens
3. CONTINUE   → Agent extends an existing flow with new screens (uses convo history)

Conversation history is preserved per session so "create next flow of screens" works.
RAG is queried on every step.
"""
import json
import re
from typing import Optional


PLANNER_SYSTEM = """You are a senior product designer running a design sprint.
You analyze user requests, think through the problem, then propose a structured plan.
You speak in first person ("I'll", "My approach") and explain your reasoning naturally.
Always ground your reasoning in the design system + RAG context provided.
Return only valid JSON.

CRITICAL — SCREEN TYPE DETECTION:
You must decide the correct screen_type and canvas_size for EVERY screen.
Read the user's request carefully:
- "website", "landing page", "marketing page", "homepage" → screen_type: "website", canvas: {width:1440, height:900}
- "web app", "dashboard", "admin panel", "portal", "platform" → screen_type: "web_dashboard", canvas: {width:1440, height:900}
- "mobile app", "iOS", "Android", "phone screen" OR financial onboarding/enrollment flows → screen_type: "mobile", canvas: {width:390, height:844}
- "tablet" → screen_type: "tablet", canvas: {width:768, height:1024}
- "desktop app" → screen_type: "desktop_app", canvas: {width:1280, height:800}
When ambiguous: financial onboarding → mobile; analytics/reporting → web_dashboard; product marketing → website.
Each screen in the SAME flow should share the same screen_type unless the request explicitly mixes platforms."""


# ── Phase 1: Plan & think (returns thought process + planned screens) ────────

async def plan_flow(
    prompt: str,
    design_system_id: str,
    fidelity: str,
    screen_count: int,
    domain: str,
    conversation_history: list,
    existing_screens: list,
    reference_image_b64: Optional[str],
    reference_mode: Optional[str],
    llm_chat,
    llm_chat_vision,
    select_model,
    rag_query,
    progress_callback=None,
) -> dict:
    """
    Phase 1 — agent analyzes, thinks, and proposes a screen plan.
    Returns thought process + screen list. Does NOT generate HTML yet.
    """
    from app.design_system.registry import get_design_system, get_system_prompt_injection

    ds = get_design_system(design_system_id)
    ds_block = get_system_prompt_injection(design_system_id)

    # ── Step A: Analyze reference image (if provided) ─────────────────────────
    image_analysis = None
    if reference_image_b64 and reference_mode:
        if progress_callback:
            await progress_callback({
                "type": "step", "phase": "plan", "step": "vision",
                "message": "🔍 Reading reference image with llava:7b...",
            })
        from app.agents.design_complete.flow_generator import _build_vision_prompt
        vision_prompt = _build_vision_prompt(reference_mode, prompt)
        try:
            raw = await llm_chat_vision(reference_image_b64, vision_prompt)
            image_analysis = _parse_json(raw) or {"raw": raw[:600]}
        except Exception as e:
            image_analysis = {"error": str(e)}
        if progress_callback:
            await progress_callback({
                "type": "step", "phase": "plan", "step": "vision_done",
                "message": "✓ Image analyzed",
            })

    # ── Step B: RAG retrieval (always) ───────────────────────────────────────
    if progress_callback:
        await progress_callback({
            "type": "step", "phase": "plan", "step": "rag",
            "message": f"📚 Reading knowledge for {domain}...",
        })
    domain_docs = await rag_query("guidelines", f"{domain} {prompt}", top_k=4) or []
    company_docs = await rag_query("company_standards", f"UX {prompt}", top_k=3) or []
    compliance_docs = await rag_query("company_standards", f"compliance regulations requirements {domain} {prompt}", top_k=4) or []
    pattern_docs = await rag_query("design_patterns", prompt, top_k=3) or []
    past_docs = await rag_query("past_designs", f"{domain} {prompt}", top_k=2) or []
    rag_context = _format_rag([domain_docs, company_docs, compliance_docs, pattern_docs, past_docs])

    if progress_callback:
        total_chunks = len(domain_docs) + len(company_docs) + len(compliance_docs) + len(pattern_docs) + len(past_docs)
        await progress_callback({
            "type": "step", "phase": "plan", "step": "rag_done",
            "message": f"✓ {total_chunks} knowledge chunks (incl. {len(compliance_docs)} compliance)",
        })

    # ── Step C: Build conversation context ───────────────────────────────────
    convo_block = ""
    if conversation_history:
        convo_block = "PRIOR CONVERSATION:\n"
        for turn in conversation_history[-6:]:
            convo_block += f"- {turn['role']}: {turn['content'][:200]}\n"
        convo_block += "\n"

    existing_block = ""
    if existing_screens:
        existing_block = "EXISTING SCREENS IN THIS PROJECT:\n"
        for s in existing_screens[-8:]:
            existing_block += f"- {s.get('name', '?')}: {s.get('purpose', '')}\n"
        existing_block += "\n"

    image_block = ""
    if image_analysis:
        image_block = f"REFERENCE IMAGE ANALYSIS:\n{json.dumps(image_analysis, indent=2)[:1000]}\n\n"

    # ── Step D: Generate the plan with thought process ───────────────────────
    if progress_callback:
        await progress_callback({
            "type": "step", "phase": "plan", "step": "thinking",
            "message": "💭 Analyzing request and planning screens...",
        })

    # Agent decides count: if screen_count <= 0, the agent infers the optimal number
    count_instruction = (
        f"The user did not specify how many screens. YOU decide the optimal number "
        f"(typically 2-6) based on the complexity of the request. Justify your choice."
        if screen_count <= 0 else
        f"The user requested approximately {screen_count} screens, but adjust if the task "
        f"genuinely needs more or fewer for a coherent flow."
    )

    plan_prompt = f"""You are planning a design sprint. Analyze the user's request and propose a structured plan.

USER REQUEST: {prompt}
DOMAIN: {domain}
FIDELITY: {fidelity}
SCREEN COUNT: {count_instruction}

{ds_block}

{rag_context}

{convo_block}{existing_block}{image_block}

STEP 1 — DECIDE SCREEN TYPE (do this first, before planning screens):
Read the user request carefully. Ask yourself: "Is this a website, a web dashboard/app, a mobile app, or a tablet app?"
Clues: "landing page" → website (1440px). "dashboard/portal/admin" → web_dashboard (1440px). "onboarding/enrollment/retirement flow/loan application" → mobile (390px). Explicit "mobile app" → mobile. No clue → default to web_dashboard (1440px) for ambiguous prompts.

CANVAS SIZE TABLE — you MUST use exactly these values based on screen_type:
- mobile:        width=390,  height=844
- tablet:        width=768,  height=1024
- web_dashboard: width=1440, height=900
- website:       width=1440, height=900
- desktop_app:   width=1280, height=800

Then return ONLY valid JSON (canvas_size MUST match screen_type using the table above — do NOT copy the example values):
{{
  "analyze_request": "1-2 sentences interpreting what the user is asking for",
  "screen_type": "web_dashboard",
  "screen_type_rationale": "Why you chose this screen type — cite specific words in the request",
  "canvas_size": {{"width": 1440, "height": 900}},
  "thought_process": "3-4 sentences of your design reasoning in first person. Be specific about patterns, layout, and design system choices.",
  "recommended_screen_count": 3,
  "count_rationale": "Why this number is right for this flow",
  "design_approach": {{
    "primary_pattern": "Multi-step wizard | Dashboard | Conversational | List + Detail | Landing | Sidebar app",
    "rationale": "Why this pattern fits",
    "visual_direction": "Brief visual direction grounded in the design system"
  }},
  "planned_screens": [
    {{
      "id": "screen-1",
      "name": "Specific screen name — not 'Step 1'",
      "purpose": "One concrete sentence on what this screen does and why it exists in the flow",
      "user_action": "What the user does on this screen",
      "key_elements": ["Specific element 1", "Specific element 2", "Specific element 3"],
      "layout_type": "centered | sidebar | dashboard | form | list | detail | onboarding | confirmation | landing",
      "screen_type": "web_dashboard",
      "canvas_size": {{"width": 1440, "height": 900}}
    }}
  ],
  "what_makes_this_good": "1-2 sentences explaining the strengths of this plan",
  "open_questions": []
}}

CRITICAL: canvas_size MUST always match screen_type. Use the CANVAS SIZE TABLE values exactly.
If screen_type is mobile → canvas_size width=390, height=844.
If screen_type is web_dashboard or website → canvas_size width=1440, height=900.
If screen_type is tablet → canvas_size width=768, height=1024.
Make screens specific to {domain}. Give each planned screen a unique id (screen-1, screen-2, ...).
Every screen in the planned_screens array MUST have screen_type and canvas_size fields."""

    model = select_model(min(8, screen_count + 3), "ux")
    raw_plan = await llm_chat(PLANNER_SYSTEM, plan_prompt, model)
    plan = _parse_json(raw_plan) or _fallback_plan(prompt, screen_count, domain)

    if progress_callback:
        await progress_callback({
            "type": "thought", "phase": "plan",
            "thought_process": plan.get("thought_process", ""),
            "analyze_request": plan.get("analyze_request", ""),
        })

        screens_meta = [
            {"id": s.get("id"), "name": s.get("name"), "purpose": s.get("purpose")}
            for s in plan.get("planned_screens", [])
        ]
        await progress_callback({
            "type": "plan_ready", "phase": "plan",
            "planned_screens": screens_meta,
            "recommended_count": plan.get("recommended_screen_count", len(screens_meta)),
            "count_rationale": plan.get("count_rationale", ""),
            "message": f"✓ I recommend {len(screens_meta)} screens — review and approve",
        })

    return {
        "phase": "planned",
        "plan": plan,
        "image_analysis": image_analysis,
        "rag_context": rag_context,
        "rag_used": {
            "domain": len(domain_docs),
            "company": len(company_docs),
            "patterns": len(pattern_docs),
            "past": len(past_docs),
        },
        "design_system": {"id": design_system_id, "name": ds["name"], "tokens": ds["tokens"]},
        "fidelity": fidelity,
        "domain": domain,
    }


# ── Phase 2: Generate approved screens ────────────────────────────────────────

async def generate_approved_screens(
    plan_payload: dict,
    approved_screen_ids: list[str],
    user_prompt: str,
    llm_chat,
    select_model,
    progress_callback=None,
    llm_chat_vision=None,
) -> dict:
    """Phase 2 — generate HTML for the approved screens only."""
    from app.agents.design_complete.flow_generator import _generate_single_screen, WIREFRAME_SYSTEM, HIFI_SYSTEM
    from app.design_system.registry import get_design_system, get_system_prompt_injection

    plan = plan_payload.get("plan", {})
    fidelity = plan_payload.get("fidelity", "hifi")
    design_system_id = plan_payload.get("design_system", {}).get("id", "company")
    rag_context = plan_payload.get("rag_context", "")
    image_analysis = plan_payload.get("image_analysis")
    reference_b64 = plan_payload.get("reference_image_b64")
    reference_mode = plan_payload.get("reference_mode")

    ds = get_design_system(design_system_id)
    ds_block = get_system_prompt_injection(design_system_id)

    # Filter to approved
    all_screens = plan.get("planned_screens", [])
    approved = [s for s in all_screens if s.get("id") in approved_screen_ids] if approved_screen_ids else all_screens

    if progress_callback:
        await progress_callback({
            "type": "step", "phase": "generate", "step": "start",
            "message": f"🎨 Generating {len(approved)} approved screens...",
        })

    # High-accuracy recreate: pass the actual image to vision for the first screen
    use_vision_recreate = (
        reference_b64 and reference_mode in ("recreate", "improve")
        and llm_chat_vision is not None
    )

    generated = []
    for idx, screen_plan in enumerate(approved):
        if progress_callback:
            await progress_callback({
                "type": "screen_start", "phase": "generate",
                "screen_number": idx + 1,
                "screen_name": screen_plan.get("name", f"Screen {idx+1}"),
                "message": f"🖼️ {screen_plan.get('name', f'Screen {idx+1}')} ({idx+1}/{len(approved)})",
            })

        # Resolve screen_type + canvas_size — screen-level overrides plan-level
        plan_screen_type = plan.get("screen_type", "web_dashboard")
        _canvas_defaults = {
            "mobile": {"width": 390, "height": 844},
            "tablet": {"width": 768, "height": 1024},
            "web_dashboard": {"width": 1440, "height": 900},
            "website": {"width": 1440, "height": 900},
            "desktop_app": {"width": 1280, "height": 800},
        }
        plan_canvas = plan.get("canvas_size") or _canvas_defaults.get(plan_screen_type, {"width": 1440, "height": 900})
        screen_type = screen_plan.get("screen_type", plan_screen_type)
        canvas_size = screen_plan.get("canvas_size", plan_canvas)

        screen_meta = {
            "screen_number": idx + 1,
            "screen_id": screen_plan.get("id", f"screen-{idx+1}"),
            "name": screen_plan.get("name", f"Screen {idx+1}"),
            "purpose": screen_plan.get("purpose", ""),
            "layout_type": screen_plan.get("layout_type", "centered"),
            "content_elements": screen_plan.get("key_elements", []),
            "primary_action": screen_plan.get("user_action", ""),
            "screen_type": screen_type,
            "canvas_size": canvas_size,
        }

        try:
            # First screen + recreate/improve mode → use vision for pixel-accuracy
            if use_vision_recreate and idx == 0:
                screen_result = await _generate_screen_from_image(
                    screen_meta=screen_meta, reference_b64=reference_b64,
                    reference_mode=reference_mode, fidelity=fidelity,
                    ds_block=ds_block, rag_context=rag_context,
                    user_prompt=user_prompt, llm_chat_vision=llm_chat_vision,
                )
            else:
                screen_result = await _generate_single_screen(
                    screen_plan=screen_meta,
                    fidelity=fidelity,
                    design_system=ds,
                    ds_prompt_block=ds_block,
                    rag_context=rag_context,
                    user_prompt=user_prompt,
                    flow_context={
                        "flow_name": plan.get("design_approach", {}).get("primary_pattern", "Flow"),
                        "screens": all_screens,
                        "domain": plan_payload.get("domain", "general"),
                    },
                    image_analysis=image_analysis,
                    llm_chat=llm_chat,
                    select_model=select_model,
                )
        except Exception as e:
            screen_result = {"html": "", "error": str(e), "model_used": ""}

        full_screen = {
            **screen_meta,
            "html": screen_result.get("html", ""),
            "design_notes": screen_result.get("design_notes", ""),
            "components_used": screen_result.get("components_used", []),
            "model_used": screen_result.get("model_used", ""),
            "version": 1,
        }
        generated.append(full_screen)

        if progress_callback:
            await progress_callback({
                "type": "screen_complete", "phase": "generate",
                "screen_number": idx + 1,
                "screen": full_screen,
                "message": f"✓ {full_screen['name']} rendered",
            })

    return {
        "phase": "generated",
        "fidelity": fidelity,
        "design_system": plan_payload.get("design_system"),
        "flow_name": plan.get("design_approach", {}).get("primary_pattern", "Generated Flow"),
        "thought_process": plan.get("thought_process", ""),
        "analyze_request": plan.get("analyze_request", ""),
        "design_approach": plan.get("design_approach", {}),
        "screens": generated,
    }


async def _generate_screen_from_image(
    screen_meta, reference_b64, reference_mode, fidelity,
    ds_block, rag_context, user_prompt, llm_chat_vision,
) -> dict:
    """
    Pixel-accurate recreation: pass the ACTUAL image to a vision model and ask
    it to output matching HTML. This is what gets ~90% visual fidelity.
    """
    if reference_mode == "recreate":
        instruction = """Recreate this exact UI screen as clean, production HTML with Tailwind CSS.
Match it as closely as possible (target 90%+ visual fidelity):
- EXACT same layout, structure, and element positions
- EXACT same colors (sample them from the image)
- Same typography hierarchy, font sizes, and weights
- Same spacing, padding, and component sizes
- Same text content where readable; realistic placeholder where not
- Same buttons, inputs, cards, navigation — recreate every visible element
Reproduce it faithfully, pixel by pixel."""
    else:  # improve
        instruction = f"""Recreate this UI screen as HTML with Tailwind CSS, but IMPROVED.
Keep the same overall layout and purpose, but fix UX/UI issues:
{user_prompt}
Apply better spacing, hierarchy, contrast, and modern polish while keeping it recognizable as the same screen."""

    prompt = f"""{instruction}

{ds_block}

DESIGN CONTEXT (from knowledge base):
{rag_context[:800]}

Output ONLY valid JSON:
{{
  "html": "Complete self-contained HTML with Tailwind CSS classes that visually matches the image. Use exact hex colors sampled from the image. Make it a full screen layout.",
  "design_notes": "What you matched / changed",
  "components_used": ["list of components"],
  "fidelity_estimate": "How closely this matches the original (e.g. '90%')"
}}

Output complete, ready-to-render HTML. Real content matching the image. No <!-- comments -->."""

    raw = await llm_chat_vision(reference_b64, prompt)
    parsed = _parse_json(raw)
    if parsed and parsed.get("html"):
        parsed["model_used"] = "vision (recreate)"
        return parsed

    # Extract HTML if JSON parse failed
    import re as _re
    m = _re.search(r"<(?:div|section|main|html|!DOCTYPE)[\s\S]*?</(?:div|section|main|html)>", raw)
    if m:
        return {"html": m.group(), "design_notes": "Vision recreation", "components_used": [], "model_used": "vision"}
    return {"html": "", "error": "Vision recreation failed to produce HTML", "model_used": "vision", "raw": raw[:300]}


# ── Phase 3: Regenerate a single screen (versioning) ──────────────────────────

async def regenerate_screen(
    screen_id: str,
    existing_screen: dict,
    refinement_instruction: str,
    plan_payload: dict,
    user_prompt: str,
    llm_chat,
    select_model,
    progress_callback=None,
) -> dict:
    """Regenerate a single screen with refinement — bumps version."""
    from app.agents.design_complete.flow_generator import _generate_single_screen
    from app.design_system.registry import get_design_system, get_system_prompt_injection

    plan = plan_payload.get("plan", {})
    fidelity = plan_payload.get("fidelity", "hifi")
    design_system_id = plan_payload.get("design_system", {}).get("id", "company")
    rag_context = plan_payload.get("rag_context", "")
    image_analysis = plan_payload.get("image_analysis")

    ds = get_design_system(design_system_id)
    ds_block = get_system_prompt_injection(design_system_id)

    if progress_callback:
        await progress_callback({
            "type": "screen_start", "phase": "regenerate",
            "screen_id": screen_id,
            "message": f"🔄 Regenerating {existing_screen.get('name', 'screen')} with refinement",
        })

    refined_purpose = f"{existing_screen.get('purpose', '')} — Refinement: {refinement_instruction}"
    screen_meta = {
        **existing_screen,
        "purpose": refined_purpose,
    }

    screen_result = await _generate_single_screen(
        screen_plan=screen_meta,
        fidelity=fidelity,
        design_system=ds,
        ds_prompt_block=ds_block,
        rag_context=rag_context,
        user_prompt=f"{user_prompt}\n\nRefinement: {refinement_instruction}",
        flow_context={
            "flow_name": plan.get("design_approach", {}).get("primary_pattern", "Flow"),
            "screens": [],
            "domain": plan_payload.get("domain", "general"),
        },
        image_analysis=image_analysis,
        llm_chat=llm_chat,
        select_model=select_model,
    )

    new_version = (existing_screen.get("version", 1) or 1) + 1

    return {
        **existing_screen,
        "html": screen_result.get("html", existing_screen.get("html", "")),
        "design_notes": screen_result.get("design_notes", ""),
        "components_used": screen_result.get("components_used", []),
        "model_used": screen_result.get("model_used", ""),
        "version": new_version,
        "refinement_history": (existing_screen.get("refinement_history") or []) + [{
            "from_version": existing_screen.get("version", 1),
            "instruction": refinement_instruction,
        }],
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _format_rag(doc_lists):
    """Format RAG results into a compact context block for the plan phase.

    Cap at 200 chars/doc × 2 docs/category × 5 categories = ~2000 chars max.
    This keeps the planner prompt lean enough for Haiku while still providing real signal.
    The generation step (flow_generator.py) applies an even tighter cap (120 chars).
    """
    parts = []
    labels = ["DOMAIN KNOWLEDGE", "COMPANY STANDARDS", "COMPLIANCE REQUIREMENTS", "APPROVED PATTERNS", "PAST SIMILAR DESIGNS"]
    for label, docs in zip(labels, doc_lists):
        text = "\n".join([d[:200] for d in docs[:2]])
        if not text:
            if "COMPLIANCE" in label:
                text = "(apply WCAG 2.1 AA, 4.5:1 contrast, 44px touch targets)"
            else:
                text = "(apply general best practices)"
        parts.append(f"{label}:\n{text}")
    return "\n\n".join(parts)


def _fallback_plan(prompt: str, screen_count: int, domain: str) -> dict:
    return {
        "analyze_request": f"User wants to design something related to {prompt[:80]}",
        "thought_process": f"I'll plan a {screen_count}-step flow grounded in {domain} domain best practices.",
        "design_approach": {
            "primary_pattern": "Multi-step flow",
            "rationale": "Breaks complex tasks into digestible steps",
            "visual_direction": "Apply the selected design system tokens",
        },
        "planned_screens": [
            {
                "id": f"screen-{i+1}",
                "name": f"Step {i+1}",
                "purpose": "Generic step in the flow",
                "user_action": "Continue",
                "key_elements": ["Heading", "Body content", "Primary CTA"],
                "layout_type": "centered",
            }
            for i in range(screen_count)
        ],
        "what_makes_this_good": "Fallback plan — agent reasoning was unavailable",
        "open_questions": [],
    }


def _parse_json(raw: str):
    text = raw.strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    for prefix in ("```json", "```"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    if text.endswith("```"):
        text = text[:-3]
    try:
        return json.loads(text.strip())
    except Exception:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return None
