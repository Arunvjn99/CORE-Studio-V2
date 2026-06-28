"""
BA/UX Flow Agent — generates node-based user flows and journey maps.
Output is a graph of nodes (screens/decisions/actions) + edges (connections)
that the frontend renders as a flowchart with connecting shapes.

Always runs RAG. Used by the Analyst team's flow canvas.
"""
import json
import re


FLOW_SYSTEM = """You are a senior UX strategist creating user flow diagrams and journey maps.
You think in terms of user goals, decision points, screens, and system actions.
You produce structured flow graphs with nodes and connections.
Return only valid JSON."""


async def generate_user_flow(
    prompt: str,
    flow_type: str,        # "user_flow" | "journey_map" | "task_flow" | "service_blueprint"
    domain: str,
    llm_chat,
    select_model,
    rag_query,
    progress_callback=None,
    image_b64: str = None,
    llm_chat_vision=None,
) -> dict:
    """Generate a node-based flow graph with UX analysis.
    If image_b64 is provided, vision-analyzes the screen first to ground the flow in real UI.
    """

    if progress_callback:
        await progress_callback({"type": "step", "message": "📚 Retrieving domain knowledge..."})

    domain_docs = await rag_query("guidelines", f"{domain} {prompt} user flow", top_k=4) or []
    pattern_docs = await rag_query("design_patterns", prompt, top_k=3) or []
    rag_context = "\n".join([d[:250] for d in (domain_docs[:3] + pattern_docs[:2])]) or "(No knowledge — applying UX best practices)"

    if progress_callback:
        await progress_callback({"type": "step", "message": f"✓ {len(domain_docs) + len(pattern_docs)} chunks retrieved"})

    # Vision screen analysis
    image_context = ""
    if image_b64 and llm_chat_vision:
        if progress_callback:
            await progress_callback({"type": "step", "message": "🖼️ Analyzing uploaded screen..."})
        try:
            image_context = await llm_chat_vision(
                image_b64,
                f"""Analyze this UI screen for a {flow_type.replace("_", " ")} diagram.
Describe in detail:
1. Every visible screen, page, or state
2. All interactive elements (buttons, links, inputs, navigation)
3. All decision points or branching logic visible
4. The sequence/order of user actions
5. Any system responses, confirmations, or error states
6. Entry and exit points of the flow

Be specific about labels, button text, and navigation paths visible."""
            )
            if progress_callback:
                await progress_callback({"type": "step", "message": "✓ Screen analyzed — mapping to flow nodes"})
        except Exception as e:
            image_context = f"[Vision analysis failed: {e}]"

    if progress_callback:
        await progress_callback({"type": "step", "message": "🧠 Designing flow structure..."})

    model = select_model(7, "ux")

    if flow_type == "journey_map":
        schema_hint = _journey_schema(prompt)
    elif flow_type == "service_blueprint":
        schema_hint = _blueprint_schema(prompt)
    else:
        schema_hint = _flow_schema(prompt, flow_type)

    image_section = f"\nSCREEN ANALYSIS FROM UPLOADED IMAGE:\n{image_context}\n\nIMPORTANT: Base the flow nodes, labels, and edges directly on the UI elements and flows visible in the screen analysis above." if image_context else ""

    full_prompt = f"""You are designing a {flow_type.replace('_', ' ')} for: {prompt}
DOMAIN: {domain}

KNOWLEDGE CONTEXT:
{rag_context}
{image_section}

{schema_hint}

Make it specific to {domain}, realistic, and complete. Map the actual user journey, not a generic one."""

    raw = await llm_chat(FLOW_SYSTEM, full_prompt, model)
    result = _parse_json(raw) or _fallback_flow(prompt, flow_type)

    # Auto-layout nodes if positions missing
    result = _auto_layout(result)

    # Flag whether image was used
    if image_b64:
        result["_image_analyzed"] = True

    if progress_callback:
        node_count = len(result.get("nodes", []))
        await progress_callback({"type": "complete", "message": f"✓ Flow ready — {node_count} nodes", "result": result})

    return result


def _flow_schema(prompt: str, flow_type: str) -> str:
    return f"""Return ONLY valid JSON for a user flow graph:
{{
  "flow_name": "Name of this flow",
  "flow_type": "{flow_type}",
  "goal": "The user's goal in this flow",
  "persona": "Who is going through this flow",
  "nodes": [
    {{
      "id": "n1",
      "type": "start | screen | decision | action | end | system",
      "label": "Short node label (e.g. 'Login Screen', 'Has account?', 'Send OTP')",
      "description": "What happens at this node",
      "row": 0,
      "col": 0
    }}
  ],
  "edges": [
    {{"from": "n1", "to": "n2", "label": "Optional condition (e.g. 'Yes', 'No', 'On submit')"}}
  ],
  "ux_analysis": {{
    "friction_points": [
      {{"node": "n3", "issue": "Specific friction", "severity": "high | medium | low", "fix": "How to reduce friction"}}
    ],
    "drop_off_risks": ["Where users likely abandon the flow"],
    "optimization_opportunities": ["Specific improvement"],
    "estimated_completion_rate": "75%",
    "estimated_steps": 5,
    "cognitive_load": "low | medium | high"
  }},
  "recommendations": ["Actionable UX recommendation"]
}}

Use these node types:
- start: entry point (1 per flow)
- screen: a UI screen the user sees
- decision: a branching point (diamond) with multiple outgoing edges
- action: a user action or system step
- system: backend/system process
- end: terminal state (can have multiple)

Layout: assign row (vertical, 0=top) and col (horizontal, 0=left) so the flow reads top-to-bottom or left-to-right. Branches from a decision get different cols.
Generate 6-12 nodes for a realistic flow."""


def _journey_schema(prompt: str) -> str:
    return f"""Return ONLY valid JSON for a customer journey map:
{{
  "flow_name": "Journey name",
  "flow_type": "journey_map",
  "persona": "Who is on this journey",
  "goal": "What they want to achieve",
  "stages": [
    {{
      "id": "s1",
      "stage": "Stage name (e.g. Awareness, Consideration, Onboarding, Usage, Advocacy)",
      "col": 0,
      "user_actions": ["What user does in this stage"],
      "touchpoints": ["Channel/screen they interact with"],
      "thoughts": "What the user is thinking",
      "emotion": "frustrated | neutral | satisfied | delighted | anxious",
      "emotion_score": 3,
      "pain_points": ["Pain in this stage"],
      "opportunities": ["Opportunity to improve experience"]
    }}
  ],
  "nodes": [
    {{"id": "s1", "type": "screen", "label": "Stage name", "row": 0, "col": 0, "description": "..."}}
  ],
  "edges": [{{"from": "s1", "to": "s2", "label": ""}}],
  "ux_analysis": {{
    "lowest_emotion_stage": "Stage with worst experience",
    "biggest_opportunity": "Where to focus improvement",
    "estimated_completion_rate": "70%",
    "cognitive_load": "medium"
  }},
  "recommendations": ["Recommendation"]
}}

Generate 4-6 journey stages. Map emotion_score 1 (very negative) to 5 (very positive) per stage."""


def _blueprint_schema(prompt: str) -> str:
    return f"""Return ONLY valid JSON for a service blueprint:
{{
  "flow_name": "Service name",
  "flow_type": "service_blueprint",
  "goal": "Service goal",
  "lanes": ["User Actions", "Frontstage", "Backstage", "Support Processes"],
  "nodes": [
    {{"id": "n1", "type": "action", "label": "Step", "lane": "User Actions", "row": 0, "col": 0, "description": "..."}}
  ],
  "edges": [{{"from": "n1", "to": "n2", "label": ""}}],
  "ux_analysis": {{"estimated_completion_rate": "80%", "cognitive_load": "medium"}},
  "recommendations": ["Recommendation"]
}}

Map nodes across 4 lanes. col = sequence step (0,1,2...). row = lane index (0-3)."""


def _auto_layout(result: dict) -> dict:
    """Ensure every node has row/col coordinates."""
    nodes = result.get("nodes", [])
    for i, n in enumerate(nodes):
        if "col" not in n or n.get("col") is None:
            n["col"] = i
        if "row" not in n or n.get("row") is None:
            n["row"] = 0
    return result


def _fallback_flow(prompt: str, flow_type: str) -> dict:
    return {
        "flow_name": prompt[:60],
        "flow_type": flow_type,
        "goal": "Complete the task",
        "persona": "User",
        "nodes": [
            {"id": "n1", "type": "start", "label": "Start", "description": "Entry point", "row": 0, "col": 0},
            {"id": "n2", "type": "screen", "label": "Main Screen", "description": "Primary interaction", "row": 0, "col": 1},
            {"id": "n3", "type": "decision", "label": "Valid?", "description": "Validation check", "row": 0, "col": 2},
            {"id": "n4", "type": "action", "label": "Submit", "description": "Submit data", "row": 0, "col": 3},
            {"id": "n5", "type": "end", "label": "Done", "description": "Complete", "row": 0, "col": 4},
        ],
        "edges": [
            {"from": "n1", "to": "n2", "label": ""},
            {"from": "n2", "to": "n3", "label": ""},
            {"from": "n3", "to": "n4", "label": "Yes"},
            {"from": "n3", "to": "n2", "label": "No"},
            {"from": "n4", "to": "n5", "label": ""},
        ],
        "ux_analysis": {
            "friction_points": [],
            "estimated_completion_rate": "75%",
            "estimated_steps": 5,
            "cognitive_load": "medium",
        },
        "recommendations": ["Fallback flow — agent reasoning unavailable"],
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
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return None
