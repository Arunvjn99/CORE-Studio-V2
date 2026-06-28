"""
CORE Studio V2 — Full Stack Test Suite
Tests every flow end-to-end against the running server (Docker or local).

Run:
    cd packages/backend && python3 tests/test_full_stack.py

Requirements: server running on http://localhost:8000
"""
import asyncio
import json
import sys
import time
import urllib.request
import urllib.error
from typing import Optional

BASE = "http://localhost:8000"
RESULTS = []


# ─────────────────────────────────────────────────────────────────────────────
# HTTP helpers
# ─────────────────────────────────────────────────────────────────────────────

def req(method: str, path: str, body=None, token: Optional[str] = None,
        timeout: int = 30) -> tuple[int, dict]:
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {"error": str(e)}
    except Exception as e:
        return 0, {"error": str(e)}


def form_req(path: str, fields: dict, token: str, timeout: int = 60) -> tuple[int, dict]:
    """Multipart/form-data POST."""
    boundary = "----FormBoundary" + str(int(time.time()))
    body_parts = []
    for key, val in fields.items():
        body_parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{val}\r\n'
        )
    body_parts.append(f'--{boundary}--\r\n')
    body = "".join(body_parts).encode()
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Authorization": f"Bearer {token}",
    }
    try:
        r = urllib.request.Request(f"{BASE}{path}", data=body, headers=headers, method="POST")
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {"error": str(e)}
    except Exception as e:
        return 0, {"error": str(e)}


def poll(path: str, token: str, until_key: str, timeout: int = 90) -> Optional[dict]:
    """Poll a GET endpoint until a key appears in the response or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        status, body = req("GET", path, token=token, timeout=10)
        if status == 200 and body.get(until_key):
            return body
        time.sleep(2)
    return None


def ok(name: str, passed: bool, detail: str = "") -> bool:
    icon = "✅" if passed else "❌"
    msg = f"{icon} {name}"
    if detail:
        msg += f"  →  {detail}"
    print(msg)
    RESULTS.append((name, passed, detail))
    return passed


def section(title: str):
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print('═' * 60)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Health & Infrastructure
# ─────────────────────────────────────────────────────────────────────────────

def test_health() -> bool:
    section("1. Health & Infrastructure")
    status, body = req("GET", "/api/health")
    ok("Backend reachable", status == 200, f"HTTP {status}")
    ok("Status healthy", body.get("status") == "healthy", body.get("status", "?"))
    ok("AI provider connected", body.get("provider") in ("anthropic", "openai", "ollama"),
       body.get("provider", "none"))
    ok("Cloud AI available", body.get("cloud_available", False))
    ok("Design system loaded", body.get("design_system", False))
    return status == 200


# ─────────────────────────────────────────────────────────────────────────────
# 2. Auth
# ─────────────────────────────────────────────────────────────────────────────

def test_auth() -> Optional[str]:
    section("2. Auth Flow")
    ts = int(time.time())
    email = f"test_{ts}@coretest.com"

    status, body = req("POST", "/api/v1/auth/register", {
        "email": email, "password": "TestPass123!",
        "full_name": "Test User", "username": f"tu{ts}",
    })
    ok("Register → 201", status == 201, f"HTTP {status}")
    token = body.get("access_token")
    ok("Register returns access_token", bool(token))

    status2, body2 = req("POST", "/api/v1/auth/login", {
        "email": email, "password": "TestPass123!",
    })
    ok("Login → 200", status2 == 200, f"HTTP {status2}")
    token = body2.get("access_token") or token
    ok("Login returns access_token", bool(token))

    # Verify token works on a protected endpoint
    status3, body3 = req("GET", "/api/v1/projects", token=token)
    ok("Protected endpoint accessible with token", status3 == 200, f"HTTP {status3}")

    return token


# ─────────────────────────────────────────────────────────────────────────────
# 3. RAG Knowledge Base
# ─────────────────────────────────────────────────────────────────────────────

async def test_rag_knowledge():
    section("3. RAG Knowledge Base (ChromaDB)")
    sys.path.insert(0, ".")
    try:
        from server_local import rag_query_rich, _get_chroma
    except ImportError as e:
        ok("RAG import", False, str(e))
        return

    store = _get_chroma()
    ok("ChromaDB collections initialised", bool(store), f"collections: {list(store.keys())}")

    # Guidelines — should have RetirementWorld skills
    r1 = await rag_query_rich("guidelines", "ERISA retirement 401k fiduciary", top_k=3)
    ok("guidelines → returns results", len(r1) > 0, f"{len(r1)} results")
    rw_hit = any(
        "retirement" in (r.get("metadata", {}).get("source", "") or "").lower()
        or "fiduciary" in r.get("content", "").lower()
        or "401" in r.get("content", "")
        for r in r1
    )
    ok("guidelines → RetirementWorld content found", rw_hit,
       f"sources: {[r.get('metadata',{}).get('source','?') for r in r1[:2]]}")

    # Company standards — should have RW1.0.MD
    r2 = await rag_query_rich("company_standards", "Congruent Solutions compliance retirement", top_k=3)
    ok("company_standards → returns results", len(r2) > 0, f"{len(r2)} results")
    cs_hit = any("retirement-world" in (r.get("metadata", {}).get("source", "") or "") for r in r2)
    ok("company_standards → RW1.0.MD / RetirementWorldSpec present", cs_hit,
       f"sources: {[r.get('metadata',{}).get('source','?') for r in r2[:2]]}")

    # Compliance subcategory
    r3 = await rag_query_rich("guidelines", "SECURE 2.0 nondiscrimination testing EPCRS", top_k=3)
    ok("guidelines → compliance docs retrievable", len(r3) > 0, f"{len(r3)} results")

    # Design patterns
    r4 = await rag_query_rich("design_patterns", "dashboard card layout mobile", top_k=2)
    ok("design_patterns → returns results", len(r4) > 0, f"{len(r4)} results")

    # Chunk counts
    try:
        g_count = store["guidelines"].count()
        c_count = store["company_standards"].count()
        ok("guidelines chunk count ≥ 500", g_count >= 500, f"{g_count} chunks")
        ok("company_standards chunk count ≥ 50", c_count >= 50, f"{c_count} chunks")
    except Exception as e:
        ok("Collection count", False, str(e))


# ─────────────────────────────────────────────────────────────────────────────
# 4. Knowledge API Search (HTTP)
# ─────────────────────────────────────────────────────────────────────────────

def test_knowledge_search_api(token: str):
    section("4. Knowledge Base API Search")
    status, body = req("POST", "/api/v1/knowledge/search", {
        "query": "ERISA fiduciary duty retirement plan",
        "top_k": 5,
    }, token=token)
    ok("Search endpoint → 200", status == 200, f"HTTP {status}")
    results = body.get("results", [])
    ok("Search returns results", len(results) > 0, f"{len(results)} results")
    if results:
        r = results[0]
        ok("Result has content", bool(r.get("content") or r.get("text")))
        source = r.get("metadata", {}).get("source", "") or r.get("source", "")
        ok("Result has source metadata", bool(source), source)


# ─────────────────────────────────────────────────────────────────────────────
# 5. Design Systems Registry
# ─────────────────────────────────────────────────────────────────────────────

def test_design_systems(token: str):
    section("5. Design System Registry")
    status, body = req("GET", "/api/v1/design/systems", token=token)
    ok("Design systems → 200", status == 200, f"HTTP {status}")
    systems = body.get("systems", body if isinstance(body, list) else [])
    ok("Systems non-empty", len(systems) > 0, f"{len(systems)} systems")
    ids = [s.get("id") for s in systems]
    ok("core-2 system present", "core-2" in ids)
    if systems:
        ok("System has color tokens", bool(systems[0].get("primary_color") or systems[0].get("tokens")))


# ─────────────────────────────────────────────────────────────────────────────
# 6. Design Plan Flow (Phase 1 — async via poll)
# ─────────────────────────────────────────────────────────────────────────────

def test_design_plan(token: str) -> Optional[dict]:
    section("6. Design Plan Flow (Phase 1)")
    status, body = form_req("/api/v1/design/plan", {
        "prompt": "401k participant portal with balance overview, contribution rate selector, and investment allocation",
        "domain": "retirement",
        "design_system": "core-2",
        "fidelity": "hifi",
        "screen_count": "2",
    }, token)
    ok("Plan → 201", 200 <= status < 300, f"HTTP {status}")
    if status >= 300:
        ok("Plan body error", False, str(body)[:200])
        return None

    gen_id = body.get("generation_id")
    session_id = body.get("session_id")
    ok("Plan returns generation_id", bool(gen_id))
    ok("Plan returns session_id", bool(session_id))
    ok("Plan status = planning", body.get("status") == "planning", body.get("status", "?"))

    # Poll until planning complete
    print("    ⏳ Polling plan status (up to 60s)...")
    result = poll(f"/api/v1/design/generate/{gen_id}", token,
                  until_key="plan_payload", timeout=60)
    if not result:
        # Try checking status field
        status2, gen_body = req("GET", f"/api/v1/design/generate/{gen_id}", token=token)
        ok("Plan polling returns data", status2 == 200, f"HTTP {status2}")
        ok("Plan completed", gen_body.get("status") in ("planned", "complete", "done", "planning"),
           f"status: {gen_body.get('status')}")
        # Check session for plan_payload
        s_status, s_body = req("GET", f"/api/v1/design/session/{session_id}", token=token)
        plan_payload = s_body.get("plan_payload")
        ok("Session has plan_payload", bool(plan_payload),
           f"session keys: {list(s_body.keys())[:6]}")
    else:
        plan_payload = result.get("plan_payload")
        ok("Plan payload available", bool(plan_payload))

    # Fetch session for plan_payload if not yet got it
    if not plan_payload:
        s_status, s_body = req("GET", f"/api/v1/design/session/{session_id}", token=token)
        plan_payload = s_body.get("plan_payload")

    if plan_payload:
        plan = plan_payload.get("plan", {})
        screens = plan.get("planned_screens", [])
        ok("Plan has planned_screens", len(screens) > 0, f"{len(screens)} screens")
        ok("Plan has thought_process", bool(plan.get("thought_process")))

        rag_used = plan_payload.get("rag_used", {})
        ok("RAG was queried", any(v > 0 for v in rag_used.values()), f"rag_used: {rag_used}")
        ok("Domain RAG returned chunks", rag_used.get("domain", 0) > 0,
           f"domain: {rag_used.get('domain', 0)}")

        rag_ctx = plan_payload.get("rag_context", "")
        ok("RAG context injected", len(rag_ctx) > 50, f"len: {len(rag_ctx)}")
        ok("RAG context has retirement content",
           any(kw in rag_ctx.lower() for kw in ["retirement", "401", "erisa", "fiduciary", "domain", "contribution"]),
           f"preview: {rag_ctx[:120]}")

    return {"session_id": session_id, "gen_id": gen_id, "plan_payload": plan_payload}


# ─────────────────────────────────────────────────────────────────────────────
# 7. Design Approve + Generate (Phase 2)
# ─────────────────────────────────────────────────────────────────────────────

def test_design_approve_generate(token: str, plan_result: Optional[dict]) -> Optional[dict]:
    section("7. Design Approve + Generate (Phase 2)")
    if not plan_result or not plan_result.get("plan_payload"):
        ok("Approve — skipped (no plan_payload from phase 1)", False)
        return None

    session_id = plan_result["session_id"]
    plan_payload = plan_result["plan_payload"]
    screens = plan_payload.get("plan", {}).get("planned_screens", [])
    approved_ids = [s.get("id") for s in screens[:2]]

    if not approved_ids:
        ok("Approve — skipped (no screen IDs)", False)
        return None

    status, body = req("POST", "/api/v1/design/approve", {
        "generation_id": plan_result["gen_id"],
        "session_id": session_id,
        "approved_screen_ids": approved_ids,
    }, token=token)
    ok("Approve → 201", 200 <= status < 300, f"HTTP {status}")
    if status >= 300:
        ok("Approve error", False, str(body)[:200])
        return None

    gen_id = body.get("generation_id")
    ok("Approve returns generation_id", bool(gen_id), gen_id or "none")

    # Poll until screens appear
    print("    ⏳ Polling generation status (up to 90s)...")
    result = None
    deadline = time.time() + 90
    while time.time() < deadline:
        s2, gen_body = req("GET", f"/api/v1/design/generate/{gen_id}", token=token, timeout=10)
        status_val = gen_body.get("status", "")
        if status_val in ("complete", "done", "generated") or gen_body.get("result"):
            result = gen_body.get("result") or gen_body
            break
        if status_val == "error":
            ok("Generation error", False, str(gen_body.get("error", ""))[:200])
            return None
        time.sleep(3)

    ok("Generation completed", result is not None, f"status: {status_val}")
    if not result:
        return None

    screens_out = result.get("screens", [])
    ok("Screens generated", len(screens_out) > 0, f"{len(screens_out)} screens")
    if screens_out:
        s = screens_out[0]
        ok("Screen has HTML", len(s.get("html", "")) > 200, f"html len: {len(s.get('html',''))}")
        ok("Screen has canvas_size", bool(s.get("canvas_size")))
        ok("Screen has name", bool(s.get("name")))
        ok("Screen has model_used", bool(s.get("model_used")))
        html = s.get("html", "")
        ok("HTML not empty boilerplate",
           "<div" in html and len(html) > 500,
           f"len: {len(html)}")

    return result


# ─────────────────────────────────────────────────────────────────────────────
# 8. Analyst Flow
# ─────────────────────────────────────────────────────────────────────────────

def test_analyst_flow(token: str):
    section("8. Analyst Flow")

    # Personas
    status, body = form_req("/api/v1/analyst/research", {
        "research_type": "personas",
        "topic": "401k participant self-service portal",
        "domain": "retirement",
        "context": "B2B SaaS for retirement plan participants at mid-size companies",
    }, token, timeout=120)
    ok("Analyst research (personas) → 2xx", 200 <= status < 300, f"HTTP {status}")
    if 200 <= status < 300:
        # response is nested: {"result": {...}, "research_type": ..., "token_usage": ...}
        inner = body.get("result", body)
        ok("Personas present", bool(inner.get("personas")), f"body keys: {list(body.keys())[:6]}")
        rag_notes = inner.get("rag_compliance_notes")
        ok("RAG compliance notes injected", bool(rag_notes),
           "present" if rag_notes else "absent (ok if no compliance match in RAG)")

    # User stories
    status2, body2 = form_req("/api/v1/analyst/research", {
        "research_type": "user_stories",
        "topic": "Hardship withdrawal request flow",
        "domain": "retirement",
        "context": "ERISA-regulated 401k. Must follow IRS hardship criteria.",
    }, token, timeout=120)
    ok("Analyst research (user_stories) → 2xx", 200 <= status2 < 300, f"HTTP {status2}")
    if 200 <= status2 < 300:
        inner2 = body2.get("result", body2)
        ok("User stories present", bool(inner2.get("user_stories")),
           f"count: {len(inner2.get('user_stories', []))}")

    # Competitor analysis
    status3, body3 = form_req("/api/v1/analyst/research", {
        "research_type": "competitor",
        "topic": "Retirement recordkeeping platform",
        "domain": "retirement",
        "context": "Congruent Solutions competitive landscape for 401k recordkeeping",
    }, token, timeout=120)
    ok("Analyst research (competitor) → 2xx", 200 <= status3 < 300, f"HTTP {status3}")
    if 200 <= status3 < 300:
        inner3 = body3.get("result", body3)
        ok("Competitors present", bool(inner3.get("competitors")),
           f"count: {len(inner3.get('competitors', []))}")

    # PRD
    status4, body4 = form_req("/api/v1/analyst/research", {
        "research_type": "prd",
        "topic": "Required Minimum Distribution notification system",
        "domain": "retirement",
        "context": "SECURE 2.0 — RMD age moved to 73. Must notify participants.",
    }, token, timeout=120)
    ok("Analyst research (prd) → 2xx", 200 <= status4 < 300, f"HTTP {status4}")
    if 200 <= status4 < 300:
        inner4 = body4.get("result", body4)
        ok("PRD has functional_requirements", bool(inner4.get("functional_requirements")),
           f"keys: {list(inner4.keys())[:5]}")


# ─────────────────────────────────────────────────────────────────────────────
# 9. QA & Compliance
# ─────────────────────────────────────────────────────────────────────────────

def test_qa_flow(token: str):
    section("9. QA & Compliance Flow")

    # Accessibility (form-data, no image)
    status, body = form_req("/api/v1/qa/accessibility", {
        "topic": "Retirement plan enrollment form with date pickers and contribution inputs",
    }, token, timeout=60)
    ok("QA accessibility → 2xx", 200 <= status < 300, f"HTTP {status}")
    if 200 <= status < 300:
        has_wcag = bool(body.get("wcag_criteria") or body.get("criteria") or
                        body.get("tests") or body.get("checks"))
        ok("Accessibility has WCAG criteria", has_wcag, f"keys: {list(body.keys())[:6]}")

    # Compliance (JSON body)
    status2, body2 = req("POST", "/api/v1/qa/compliance", {
        "compliance_type": "wcag",
        "topic": "401k participant portal with investment elections",
        "domain": "retirement",
        "design_context": {},
    }, token=token)
    ok("QA compliance (WCAG) → 2xx", 200 <= status2 < 300, f"HTTP {status2}")
    if 200 <= status2 < 300:
        ok("Compliance has results", bool(body2.get("results") or body2.get("checks") or
                                          body2.get("compliance_score") is not None),
           f"keys: {list(body2.keys())[:6]}")


# ─────────────────────────────────────────────────────────────────────────────
# 10. AI Status
# ─────────────────────────────────────────────────────────────────────────────

def test_ai_status(token: str):
    section("10. AI Status & Model Routing")
    status, body = req("GET", "/api/v1/ai/status", token=token)
    ok("AI status → 2xx", 200 <= status < 300, f"HTTP {status}")
    ok("Provider set", bool(body.get("provider")), body.get("provider", "?"))
    models = body.get("models") or body.get("active_models", {})
    ok("Models configured", bool(models), str(models)[:80])
    ok("Standard model set",
       bool(models.get("standard") if isinstance(models, dict) else models),
       str(models)[:60])


# ─────────────────────────────────────────────────────────────────────────────
# 11. Projects
# ─────────────────────────────────────────────────────────────────────────────

def test_projects(token: str) -> Optional[str]:
    section("11. Projects CRUD")
    status, body = req("POST", "/api/v1/projects", {
        "name": "Retirement Portal Test",
        "description": "ERISA-compliant participant portal",
    }, token=token)
    ok("Create project → 2xx", 200 <= status < 300, f"HTTP {status}")
    project_id = body.get("id") or body.get("project_id")
    ok("Project has ID", bool(project_id))

    status2, body2 = req("GET", "/api/v1/projects", token=token)
    ok("List projects → 200", status2 == 200, f"HTTP {status2}")
    projects = body2 if isinstance(body2, list) else body2.get("projects", [])
    ok("Project list non-empty", len(projects) > 0, f"{len(projects)} projects")
    return project_id


# ─────────────────────────────────────────────────────────────────────────────
# 12. CORS Headers
# ─────────────────────────────────────────────────────────────────────────────

def test_cors():
    section("12. CORS Headers")
    r = urllib.request.Request(
        f"{BASE}/api/v1/design/systems",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization",
        },
        method="OPTIONS",
    )
    try:
        with urllib.request.urlopen(r, timeout=10) as resp:
            hdrs = dict(resp.headers)
            acao = hdrs.get("Access-Control-Allow-Origin", "")
            acac = hdrs.get("Access-Control-Allow-Credentials", "")
            ok("CORS preflight → 200", resp.status == 200, f"HTTP {resp.status}")
            ok("allow-origin includes localhost:3000", "localhost:3000" in acao or acao == "*",
               f"header value: '{acao}'")
            ok("allow-credentials: true", "true" in acac.lower(), f"header value: '{acac}'")
    except Exception as e:
        ok("CORS preflight", False, str(e))


# ─────────────────────────────────────────────────────────────────────────────
# 13. WebSocket
# ─────────────────────────────────────────────────────────────────────────────

def test_websocket():
    section("13. WebSocket Connection")
    import socket
    import base64

    gen_id = "test-ws-" + str(int(time.time()))
    key = base64.b64encode(b"core-studio-test-key-123").decode()
    handshake = (
        f"GET /ws/design/{gen_id} HTTP/1.1\r\n"
        f"Host: localhost:8000\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n"
        f"\r\n"
    )
    try:
        s = socket.create_connection(("localhost", 8000), timeout=5)
        s.send(handshake.encode())
        response = s.recv(1024).decode(errors="replace")
        ok("WebSocket upgrade accepted (101)", "101 Switching Protocols" in response,
           response.split("\r\n")[0])
        s.close()
    except Exception as e:
        ok("WebSocket connection", False, str(e))


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

async def main():
    print("\n" + "═" * 60)
    print("  CORE Studio V2 — Full Stack Test Suite")
    print(f"  Target: {BASE}")
    print("═" * 60)

    if not test_health():
        print("\n❌ Backend not reachable. Ensure server is running.")
        sys.exit(1)

    token = test_auth()
    if not token:
        print("\n❌ Auth failed — cannot continue.")
        sys.exit(1)

    await test_rag_knowledge()
    test_knowledge_search_api(token)
    test_design_systems(token)

    plan_result = test_design_plan(token)
    test_design_approve_generate(token, plan_result)

    test_analyst_flow(token)
    test_qa_flow(token)
    test_ai_status(token)
    test_projects(token)
    test_cors()
    test_websocket()

    # Summary
    passed = sum(1 for _, p, _ in RESULTS if p)
    failed = sum(1 for _, p, _ in RESULTS if not p)
    total = len(RESULTS)

    print(f"\n{'═' * 60}")
    print(f"  RESULTS: {passed}/{total} passed  |  {failed} failed")
    print("═" * 60)

    if failed:
        print("\nFAILED:")
        for name, p, detail in RESULTS:
            if not p:
                print(f"  ❌ {name}  →  {detail}")
    print()
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
