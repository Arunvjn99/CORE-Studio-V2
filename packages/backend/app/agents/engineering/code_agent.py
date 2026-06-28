"""
Engineering Team Agents:
1. Code Generator — React/HTML/Flutter from UI design (uses qwen2.5-coder)
2. API Designer — REST/GraphQL API design from requirements
3. Architecture Planner — system architecture from product requirements
4. Technical Documentation — from design to technical specs
"""
import json
import re
from typing import Optional


ENG_SYSTEM_CODE = """You are a senior frontend engineer specializing in React, TypeScript, and Tailwind CSS.
You write clean, production-ready, accessible code with proper component structure.
Return only valid JSON or code as requested."""

ENG_SYSTEM_ARCH = """You are a senior software architect. You design scalable, maintainable systems.
Return only valid JSON."""


async def run_code_generation(
    output_format: str,   # react | html | flutter | vue
    ui_design: dict,
    ux_flow: dict,
    topic: str,
    llm_chat,
    select_model,
) -> dict:
    """
    Generate production code from UI design.
    Routes to qwen2.5-coder:7b for code tasks.
    """
    model = select_model(7, "ui")  # ui agent = coder model

    screens = ui_design.get("screens", [])
    tokens = ui_design.get("design_tokens", {})
    colours = tokens.get("colors", {})

    prompt = f"""You are a senior {output_format} developer. Convert this design to production code.

PROJECT: {topic}
OUTPUT FORMAT: {output_format}
DESIGN TOKENS: {json.dumps(colours, indent=2)[:400]}
SCREENS: {[s.get("name","?") for s in screens[:4]]}

Generate complete, working {output_format} code. Return ONLY valid JSON:
{{
  "project_name": "{topic}",
  "framework": "{output_format}",
  "files": [
    {{
      "filename": "ComponentName.tsx",
      "path": "src/components/",
      "type": "component | page | hook | utility | styles | config",
      "description": "What this file does",
      "code": "Complete, working code here — no placeholders",
      "dependencies": ["package-name@version"]
    }}
  ],
  "design_tokens_file": {{
    "filename": "tokens.ts",
    "path": "src/",
    "code": "export const tokens = {{ colors: {{ primary: '{colours.get('primary','#007AFF')}' }} }} as const"
  }},
  "setup_instructions": [
    "npm install package-name",
    "Other setup step"
  ],
  "component_tree": {{
    "root": "App",
    "children": []
  }},
  "accessibility_notes": [
    "Accessibility consideration implemented in this code"
  ]
}}

Generate real, complete code — not placeholder comments."""

    raw = await llm_chat(ENG_SYSTEM_CODE, prompt, model)

    # Try parse
    result = _parse_json(raw)
    if result and "files" in result:
        return result

    # If pure code returned (no JSON), wrap it
    if raw.strip().startswith(("import ", "export ", "const ", "function ", "class ", "//", "/*")):
        return {
            "project_name": topic,
            "framework": output_format,
            "files": [{
                "filename": f"{topic.replace(' ', '')}.tsx",
                "path": "src/",
                "type": "component",
                "description": f"Generated {output_format} code for {topic}",
                "code": raw,
                "dependencies": ["react", "tailwindcss"],
            }],
            "setup_instructions": ["npm install", "npx tailwindcss init"],
        }

    return {"project_name": topic, "framework": output_format, "error": "Parse failed", "raw": raw[:500]}


async def run_api_design(
    requirements: dict,
    user_stories: list,
    topic: str,
    llm_chat,
    select_model,
) -> dict:
    """Design REST API from requirements."""
    model = select_model(6, "planner")

    stories = [f"{s.get('id','?')}: {s.get('i_want','?')}" for s in (user_stories or [])[:8]]

    prompt = f"""You are a senior backend engineer designing a REST API.

PRODUCT: {topic}
USER STORIES:
{chr(10).join(stories) or "Not provided"}

REQUIREMENTS:
{json.dumps(requirements, indent=2)[:600] if requirements else "Design based on product name"}

Design a complete, RESTful API. Return ONLY valid JSON:
{{
  "api_name": "{topic} API",
  "base_url": "/api/v1",
  "authentication": {{
    "type": "JWT | OAuth2 | API Key",
    "description": "How authentication works"
  }},
  "endpoints": [
    {{
      "method": "GET | POST | PUT | PATCH | DELETE",
      "path": "/resource/{{id}}",
      "description": "What this endpoint does",
      "auth_required": true,
      "request_body": {{
        "type": "object",
        "properties": {{"field": "type"}}
      }},
      "response": {{
        "200": {{"description": "Success", "schema": {{"field": "type"}}}}
      }},
      "query_params": [{{"name": "param", "type": "string", "required": false, "description": "What it does"}}]
    }}
  ],
  "data_models": [
    {{
      "name": "ModelName",
      "fields": [
        {{"name": "id", "type": "UUID", "required": true, "description": "Primary key"}},
        {{"name": "created_at", "type": "DateTime", "required": true, "description": "Creation timestamp"}}
      ],
      "relationships": [{{"type": "has_many | belongs_to", "model": "OtherModel"}}]
    }}
  ],
  "error_codes": [
    {{"code": 400, "name": "Bad Request", "description": "When it occurs"}}
  ],
  "versioning_strategy": "URL path versioning (/api/v1)",
  "rate_limiting": "100 requests per minute per user"
}}"""

    raw = await llm_chat(ENG_SYSTEM_ARCH, prompt, model)
    return _parse_json(raw) or {"error": "Parse failed", "raw": raw[:400]}


async def run_architecture_plan(
    requirements: dict,
    topic: str,
    scale: str,  # small | medium | enterprise
    llm_chat,
    select_model,
    rag_query=None,
) -> dict:
    """Generate system architecture plan."""
    model = select_model(8, "planner")  # High complexity → advanced model

    rag_ctx = ""
    if rag_query:
        docs = await rag_query("guidelines", f"architecture {topic}", top_k=3)
        rag_ctx = "\n".join(docs[:2]) or ""

    prompt = f"""You are a senior software architect designing system architecture.

PRODUCT: {topic}
SCALE: {scale}
REQUIREMENTS SUMMARY: {json.dumps(requirements, indent=2)[:600] if requirements else "Design based on product"}

ARCHITECTURE GUIDELINES:
{rag_ctx or "Follow cloud-native, microservices best practices"}

Design a complete architecture. Return ONLY valid JSON:
{{
  "architecture_name": "{topic} — System Architecture",
  "scale": "{scale}",
  "pattern": "Microservices | Monolith | Serverless | Event-driven | Hybrid",
  "overview": "2-3 sentence architecture summary",
  "components": [
    {{
      "name": "Component name",
      "type": "Frontend | Backend | Database | Cache | Queue | CDN | Auth | API Gateway",
      "technology": "Specific tech choice e.g. React 18, FastAPI, PostgreSQL 16",
      "responsibility": "What this component does",
      "scaling_strategy": "Horizontal | Vertical | Serverless | N/A",
      "estimated_load": "Requests/s or users"
    }}
  ],
  "data_flow": [
    {{"from": "Component A", "to": "Component B", "protocol": "REST | WebSocket | gRPC | Queue", "description": "What data flows"}}
  ],
  "infrastructure": {{
    "cloud_provider": "AWS | GCP | Azure | Multi-cloud",
    "deployment": "Kubernetes | Docker Compose | Serverless | PaaS",
    "ci_cd": "GitHub Actions | GitLab CI | Jenkins",
    "monitoring": "Datadog | Prometheus + Grafana | CloudWatch"
  }},
  "security": {{
    "authentication": "JWT + OAuth2",
    "authorization": "RBAC",
    "data_encryption": "AES-256 at rest, TLS 1.3 in transit",
    "compliance": ["GDPR", "SOC 2"]
  }},
  "scalability": {{
    "current_capacity": "X users",
    "target_capacity": "Y users",
    "bottlenecks": ["Potential scaling bottleneck"],
    "mitigation": ["How to address each bottleneck"]
  }},
  "cost_estimate": {{
    "monthly_infra": "$X-Y USD",
    "breakdown": [{{"component": "Service name", "cost": "$X/month"}}]
  }},
  "tech_stack": {{
    "frontend": [],
    "backend": [],
    "database": [],
    "devops": []
  }},
  "adr": [
    {{
      "id": "ADR-001",
      "title": "Architecture Decision Record title",
      "status": "Accepted",
      "context": "Why this decision was needed",
      "decision": "What was decided",
      "consequences": "Impact of this decision"
    }}
  ]
}}"""

    raw = await llm_chat(ENG_SYSTEM_ARCH, prompt, model)
    return _parse_json(raw) or {"error": "Parse failed", "raw": raw[:400]}


async def run_technical_docs(
    doc_type: str,  # readme | api_docs | deployment | runbook | adr
    artifacts: dict,
    topic: str,
    llm_chat,
    select_model,
) -> dict:
    """Generate technical documentation."""
    model = select_model(5, "planner")

    prompt = f"""You are a technical writer creating {doc_type} documentation.

PRODUCT: {topic}
DOC TYPE: {doc_type}
AVAILABLE ARTIFACTS: {list(artifacts.keys())}

Generate professional {doc_type} documentation. Return ONLY valid JSON:
{{
  "doc_type": "{doc_type}",
  "title": "Document title",
  "version": "1.0",
  "sections": [
    {{
      "title": "Section title",
      "content": "Full section content in Markdown format",
      "subsections": []
    }}
  ],
  "metadata": {{
    "author": "CORE Studio AI",
    "date": "Auto-generated",
    "last_updated": "Auto-generated",
    "status": "Draft | Review | Approved"
  }}
}}"""

    raw = await llm_chat(ENG_SYSTEM_ARCH, prompt, model)
    return _parse_json(raw) or {"error": "Parse failed", "raw": raw[:400]}


def _parse_json(raw: str) -> Optional[dict]:
    text = raw.strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    for prefix in ("```json", "```"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    if text.endswith("```"):
        text = text[:-3]
    try:
        data = json.loads(text.strip())
        return data if isinstance(data, dict) else None
    except Exception:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return None
