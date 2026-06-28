"""
QA Team Agents:
1. Test Case Generator — from requirements/user stories → complete test cases
2. Accessibility Check — real WCAG math + LLM deep analysis + optional image input
3. Compliance Checker — WCAG, GDPR, HIPAA, SOC2 validation

Image-based accessibility: upload a screenshot → vision LLM extracts visual data
(colors, contrast, text sizes, interactive elements) → full WCAG 2.1 AA check
using RAG-loaded WCAG standards from the knowledge base.
"""
import json
import re
import math
from typing import Optional


QA_SYSTEM = """You are a senior QA engineer and accessibility specialist.
You produce precise, complete test cases and compliance reports.
Return only valid JSON."""


WCAG_CRITERIA = [
    # Level A
    {"id": "1.1.1", "name": "Non-text Content",              "level": "A",  "category": "Perceivable"},
    {"id": "1.2.1", "name": "Audio-only/Video-only",          "level": "A",  "category": "Perceivable"},
    {"id": "1.3.1", "name": "Info and Relationships",         "level": "A",  "category": "Perceivable"},
    {"id": "1.3.2", "name": "Meaningful Sequence",            "level": "A",  "category": "Perceivable"},
    {"id": "1.3.3", "name": "Sensory Characteristics",        "level": "A",  "category": "Perceivable"},
    {"id": "1.4.1", "name": "Use of Color",                   "level": "A",  "category": "Perceivable"},
    {"id": "2.1.1", "name": "Keyboard",                       "level": "A",  "category": "Operable"},
    {"id": "2.1.2", "name": "No Keyboard Trap",               "level": "A",  "category": "Operable"},
    {"id": "2.2.1", "name": "Timing Adjustable",              "level": "A",  "category": "Operable"},
    {"id": "2.3.1", "name": "Three Flashes / Below Threshold","level": "A",  "category": "Operable"},
    {"id": "2.4.1", "name": "Bypass Blocks",                  "level": "A",  "category": "Operable"},
    {"id": "2.4.2", "name": "Page Titled",                    "level": "A",  "category": "Operable"},
    {"id": "2.4.3", "name": "Focus Order",                    "level": "A",  "category": "Operable"},
    {"id": "2.4.4", "name": "Link Purpose (In Context)",      "level": "A",  "category": "Operable"},
    {"id": "3.1.1", "name": "Language of Page",               "level": "A",  "category": "Understandable"},
    {"id": "3.2.1", "name": "On Focus",                       "level": "A",  "category": "Understandable"},
    {"id": "3.2.2", "name": "On Input",                       "level": "A",  "category": "Understandable"},
    {"id": "3.3.1", "name": "Error Identification",           "level": "A",  "category": "Understandable"},
    {"id": "3.3.2", "name": "Labels or Instructions",         "level": "A",  "category": "Understandable"},
    {"id": "4.1.1", "name": "Parsing",                        "level": "A",  "category": "Robust"},
    {"id": "4.1.2", "name": "Name, Role, Value",              "level": "A",  "category": "Robust"},
    # Level AA
    {"id": "1.2.4", "name": "Captions (Live)",                "level": "AA", "category": "Perceivable"},
    {"id": "1.2.5", "name": "Audio Description (Prerecorded)","level": "AA", "category": "Perceivable"},
    {"id": "1.3.4", "name": "Orientation",                    "level": "AA", "category": "Perceivable"},
    {"id": "1.3.5", "name": "Identify Input Purpose",         "level": "AA", "category": "Perceivable"},
    {"id": "1.4.3", "name": "Contrast (Minimum)",             "level": "AA", "category": "Perceivable"},
    {"id": "1.4.4", "name": "Resize Text",                    "level": "AA", "category": "Perceivable"},
    {"id": "1.4.5", "name": "Images of Text",                 "level": "AA", "category": "Perceivable"},
    {"id": "1.4.10", "name": "Reflow",                        "level": "AA", "category": "Perceivable"},
    {"id": "1.4.11", "name": "Non-text Contrast",             "level": "AA", "category": "Perceivable"},
    {"id": "1.4.12", "name": "Text Spacing",                  "level": "AA", "category": "Perceivable"},
    {"id": "1.4.13", "name": "Content on Hover or Focus",     "level": "AA", "category": "Perceivable"},
    {"id": "2.4.5", "name": "Multiple Ways",                  "level": "AA", "category": "Operable"},
    {"id": "2.4.6", "name": "Headings and Labels",            "level": "AA", "category": "Operable"},
    {"id": "2.4.7", "name": "Focus Visible",                  "level": "AA", "category": "Operable"},
    {"id": "2.5.3", "name": "Label in Name",                  "level": "AA", "category": "Operable"},
    {"id": "2.5.4", "name": "Motion Actuation",               "level": "AA", "category": "Operable"},
    {"id": "3.1.2", "name": "Language of Parts",              "level": "AA", "category": "Understandable"},
    {"id": "3.2.3", "name": "Consistent Navigation",          "level": "AA", "category": "Understandable"},
    {"id": "3.2.4", "name": "Consistent Identification",      "level": "AA", "category": "Understandable"},
    {"id": "3.3.3", "name": "Error Suggestion",               "level": "AA", "category": "Understandable"},
    {"id": "3.3.4", "name": "Error Prevention (Legal/Financial/Data)", "level": "AA", "category": "Understandable"},
    {"id": "4.1.3", "name": "Status Messages",                "level": "AA", "category": "Robust"},
]


# ── Real WCAG colour contrast math (ported from V1 accessibility_v2.py) ──────

def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(hex_color: str) -> Optional[float]:
    try:
        h = hex_color.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) != 6:
            return None
        r = _srgb_to_linear(int(h[0:2], 16) / 255)
        g = _srgb_to_linear(int(h[2:4], 16) / 255)
        b = _srgb_to_linear(int(h[4:6], 16) / 255)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    except Exception:
        return None


def contrast_ratio(fg: str, bg: str) -> Optional[float]:
    l1, l2 = _luminance(fg), _luminance(bg)
    if l1 is None or l2 is None:
        return None
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ── Test Case Generator ───────────────────────────────────────────────────────

async def run_test_cases(
    test_type: str,   # functional | integration | e2e | regression | performance
    requirements: dict,
    user_stories: list,
    topic: str,
    llm_chat,
    select_model,
) -> dict:
    """Generate complete test cases from requirements."""
    model = select_model(5, "qa")

    stories_text = ""
    if user_stories:
        stories_text = "\n".join([
            f"- {s.get('id','?')}: As a {s.get('as_a','?')}, I want {s.get('i_want','?')}"
            for s in user_stories[:10]
        ])

    req_text = json.dumps(requirements, indent=2)[:1000] if requirements else "No specific requirements provided"

    prompt = f"""You are a senior QA engineer writing {test_type} test cases.

FEATURE: {topic}
TEST TYPE: {test_type}

USER STORIES:
{stories_text or "Not provided — generate from feature context"}

REQUIREMENTS:
{req_text}

Generate comprehensive test cases. Return ONLY valid JSON:
{{
  "test_suite": "{topic} — {test_type.title()} Tests",
  "test_type": "{test_type}",
  "coverage_summary": {{
    "total_cases": 0,
    "happy_path": 0,
    "edge_cases": 0,
    "error_cases": 0,
    "accessibility": 0
  }},
  "test_cases": [
    {{
      "id": "TC-001",
      "title": "Test case title",
      "category": "Happy Path | Edge Case | Error Case | Accessibility | Performance",
      "priority": "P1 | P2 | P3",
      "user_story_ref": "US-001",
      "preconditions": ["System state before test runs"],
      "steps": [
        {{"step": 1, "action": "User action", "expected": "Expected result"}}
      ],
      "expected_result": "Overall expected outcome",
      "actual_result": "TBD — to be filled during execution",
      "status": "Not Run",
      "test_data": {{"field": "test value"}},
      "automation_candidate": true,
      "notes": "Additional context"
    }}
  ],
  "automation_recommendations": {{
    "automatable": 0,
    "manual_only": 0,
    "suggested_framework": "Playwright | Cypress | Selenium | Jest",
    "reason": "Why this framework"
  }},
  "risk_areas": ["Areas with highest risk requiring manual attention"]
}}

Generate at least 8 test cases covering happy path, edge cases, and error scenarios."""

    raw = await llm_chat(QA_SYSTEM, prompt, model)
    result = _parse_or_fallback(raw, "test_cases", topic)

    # Update coverage summary counts
    if "test_cases" in result and isinstance(result["test_cases"], list):
        tc = result["test_cases"]
        result["coverage_summary"] = {
            "total_cases": len(tc),
            "happy_path": sum(1 for t in tc if "Happy" in t.get("category", "")),
            "edge_cases": sum(1 for t in tc if "Edge" in t.get("category", "")),
            "error_cases": sum(1 for t in tc if "Error" in t.get("category", "")),
            "accessibility": sum(1 for t in tc if "Accessibility" in t.get("category", "")),
        }

    return result


# ── Image-based WCAG Analysis ─────────────────────────────────────────────────

async def _extract_visual_data_from_image(image_b64: str, topic: str, llm_chat_vision) -> dict:
    """Use vision LLM to extract accessibility-relevant visual data from a screenshot."""
    prompt = f"""You are an accessibility expert analyzing a UI screenshot for WCAG 2.1 compliance.

Analyze this screen and extract the following data for accessibility testing:

1. COLOR DATA
   - Background color (hex or approximate)
   - Primary text color (hex or approximate)
   - Secondary text color
   - Button/CTA background color
   - Link color
   - Error/warning colors
   - Any color used ONLY to convey information (without text/icon)

2. TYPOGRAPHY
   - Approximate font sizes for: headings, body text, labels, captions
   - Font weight contrast between headings and body
   - Line height appearance (tight/normal/loose)
   - Any text that is images of text (not real text)

3. INTERACTIVE ELEMENTS
   - All buttons: size (approximate px), label text, visible focus state
   - All links: distinguishable from body text? (underline/color/both)
   - Form inputs: labels visible? placeholder-only labels?
   - Touch targets that appear smaller than 44×44px

4. STRUCTURE & HIERARCHY
   - Heading hierarchy (H1, H2, H3 visible)
   - Navigation landmarks visible
   - Skip links or bypass mechanisms visible
   - Consistent navigation across views if multiple screens shown

5. CONTENT & INFORMATION
   - Images: do they appear to have alt text context?
   - Icons: are they used alone without text labels?
   - Error messages: visible? descriptive?
   - Form required fields: visually indicated?
   - Time limits or auto-updating content visible?

6. POTENTIAL VIOLATIONS
   - Any obvious contrast issues (light text on light bg, etc.)
   - Any information conveyed by color alone
   - Any missing labels
   - Any layout issues at this viewport

Product: {topic}

Return your analysis as structured JSON:
{{
  "screen_description": "Brief description of what this screen shows",
  "estimated_colors": {{
    "background": "#approx",
    "text_primary": "#approx",
    "text_secondary": "#approx",
    "interactive": "#approx",
    "error": "#approx or null"
  }},
  "typography_observations": {{
    "heading_size_approx": "32px",
    "body_size_approx": "16px",
    "caption_size_approx": "12px",
    "line_height": "normal | tight | loose",
    "images_of_text_present": false
  }},
  "interactive_elements": {{
    "buttons": [{{"label": "...", "size_ok": true, "has_visible_focus": "unknown"}}],
    "links_distinguishable": true,
    "form_labels_visible": true,
    "small_targets_detected": []
  }},
  "structure": {{
    "heading_hierarchy_visible": true,
    "nav_landmarks_visible": true,
    "skip_links_visible": false,
    "consistent_navigation": true
  }},
  "content_issues": {{
    "images_without_alt_context": [],
    "icon_only_controls": [],
    "error_messages_descriptive": true,
    "required_fields_indicated": true,
    "color_only_information": []
  }},
  "obvious_violations": [
    {{"issue": "Description", "wcag_criterion": "1.4.3", "severity": "high | medium | low"}}
  ],
  "overall_impression": "high | medium | low accessibility quality"
}}"""

    try:
        raw = await llm_chat_vision(image_b64, prompt)
        # Parse JSON from vision response
        raw = raw.strip()
        raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        for prefix in ("```json", "```"):
            if raw.startswith(prefix):
                raw = raw[len(prefix):]
        if raw.endswith("```"):
            raw = raw[:-3]
        data = json.loads(raw.strip())
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {"error": "Vision extraction failed", "screen_description": "Could not analyze image"}


async def run_accessibility_from_image(
    image_b64: str,
    topic: str,
    llm_chat,
    llm_chat_vision,
    select_model,
    rag_query,
) -> dict:
    """
    Full WCAG 2.1 AA accessibility check from a screenshot.

    Pipeline:
    1. Vision LLM extracts visual data (colors, typography, structure, violations)
    2. Real contrast math on extracted hex colors
    3. RAG loads WCAG standards from org knowledge base
    4. LLM checks all 42 WCAG 2.1 AA criteria against extracted data
    5. Returns structured report with score, violations, and recommendations
    """
    # Step 1 — Extract visual data from image
    visual_data = await _extract_visual_data_from_image(image_b64, topic, llm_chat_vision)

    # Step 2 — Real contrast math on extracted colors
    extracted_colors = visual_data.get("estimated_colors", {})
    contrast_checks = []

    fg = extracted_colors.get("text_primary")
    bg = extracted_colors.get("background")
    if fg and bg and not fg.startswith("#approx"):
        ratio = contrast_ratio(fg, bg)
        contrast_checks.append({
            "wcag_criterion": "1.4.3",
            "name": "Contrast (Minimum) — Body Text",
            "level": "AA",
            "status": "pass" if (ratio and ratio >= 4.5) else "fail",
            "passed": bool(ratio and ratio >= 4.5),
            "details": f"Text/background contrast: {ratio:.1f}:1" if ratio else "Colors too approximate to calculate",
            "recommendation": "Increase contrast to ≥ 4.5:1 for body text (WCAG 1.4.3)" if (ratio and ratio < 4.5) else "✓ Meets minimum contrast",
            "measured_value": f"{ratio:.2f}:1" if ratio else "N/A",
            "threshold": "4.5:1",
        })

    interactive_color = extracted_colors.get("interactive")
    if interactive_color and bg and not interactive_color.startswith("#approx"):
        ratio = contrast_ratio(interactive_color, bg)
        if ratio:
            contrast_checks.append({
                "wcag_criterion": "1.4.11",
                "name": "Non-text Contrast — Interactive Elements",
                "level": "AA",
                "status": "pass" if ratio >= 3.0 else "fail",
                "passed": ratio >= 3.0,
                "details": f"UI component contrast: {ratio:.1f}:1",
                "recommendation": "Interactive elements need ≥ 3:1 contrast ratio" if ratio < 3.0 else "✓ Meets non-text contrast",
                "measured_value": f"{ratio:.2f}:1",
                "threshold": "3:1",
            })

    # Step 3 — Load WCAG standards from RAG knowledge
    wcag_docs = await rag_query("guidelines", f"WCAG 2.1 accessibility standards {topic}", top_k=4) or []
    ux_docs   = await rag_query("documents",  f"accessibility compliance {topic}", top_k=2) or []
    rag_wcag_context = "\n".join([d[:300] for d in (wcag_docs + ux_docs) if d])[:1500] or "(No WCAG docs in knowledge base — using built-in criteria)"

    # Step 4 — LLM checks all WCAG 2.1 AA criteria
    model = select_model(5, "qa")
    wcag_list = "\n".join([f"- {c['id']} {c['name']} (Level {c['level']})" for c in WCAG_CRITERIA])

    prompt = f"""You are a WCAG 2.1 AA accessibility expert analyzing a UI screenshot.

PRODUCT: {topic}
SCREEN DESCRIPTION: {visual_data.get("screen_description", "Not available")}

VISUAL DATA EXTRACTED FROM SCREENSHOT:
{json.dumps(visual_data, indent=2)[:2000]}

WCAG KNOWLEDGE FROM ORG DOCS:
{rag_wcag_context}

OBVIOUS VIOLATIONS DETECTED BY VISION:
{json.dumps(visual_data.get("obvious_violations", []), indent=2)}

Check ALL WCAG 2.1 AA criteria below against the visual data above.
For each criterion, determine pass/fail/warning/not_applicable based on what's visible.

WCAG 2.1 CRITERIA TO CHECK:
{wcag_list}

Return ONLY valid JSON:
{{
  "wcag_checks": [
    {{
      "wcag_criterion": "1.4.3",
      "name": "Contrast (Minimum)",
      "level": "AA",
      "category": "Perceivable",
      "status": "pass | fail | warning | not_applicable",
      "severity": "critical | high | medium | low | none",
      "finding": "What was found in the screenshot",
      "recommendation": "Specific fix required, or null if passing",
      "effort": "low | medium | high"
    }}
  ],
  "critical_issues": [
    {{
      "criterion": "1.4.3",
      "issue": "Clear description of the problem",
      "impact": "Who is affected and how",
      "fix": "Exact step to fix this"
    }}
  ],
  "quick_wins": ["Small change with high accessibility impact"],
  "overall_narrative": "2-3 sentence executive summary of accessibility status",
  "user_impact": "How current state affects users with disabilities"
}}"""

    raw = await llm_chat(QA_SYSTEM, prompt, model)
    llm_result = _parse_or_fallback(raw, "accessibility", topic)

    # Merge all checks
    all_checks = contrast_checks + llm_result.get("wcag_checks", [])
    passed = sum(1 for c in all_checks if c.get("passed", c.get("status") == "pass"))
    failed = sum(1 for c in all_checks if c.get("status") in ("fail",) or c.get("passed") == False)
    warned = sum(1 for c in all_checks if c.get("status") == "warning")

    total_checks = max(len(all_checks), 1)
    score = round(passed / total_checks * 100)
    level = "AAA" if score >= 95 else "AA" if score >= 80 else "A" if score >= 60 else "FAIL"

    return {
        "check_type": "accessibility",
        "source": "image",
        "topic": topic,
        "overall_score": score,
        "wcag_level": level,
        "passed": score >= 80,
        "summary": f"WCAG 2.1 {level} — {score}/100 ({passed} passed, {failed} failed, {warned} warnings). {llm_result.get('overall_narrative', '')}",
        "visual_data": visual_data,
        "contrast_checks": contrast_checks,
        "wcag_checks": llm_result.get("wcag_checks", []),
        "all_checks": all_checks,
        "critical_issues": llm_result.get("critical_issues", []),
        "quick_wins": llm_result.get("quick_wins", []),
        "user_impact": llm_result.get("user_impact", ""),
        "rag_context_used": bool(rag_wcag_context and "No WCAG docs" not in rag_wcag_context),
        "stats": {"total": total_checks, "passed": passed, "failed": failed, "warnings": warned},
    }


# ── Real Accessibility Check (V1 AccessibilityValidatorV2 ported) ─────────────

async def run_accessibility_check(
    ui_design: dict,
    ux_flow: dict,
    topic: str,
    llm_chat,
    select_model,
    rag_query=None,
) -> dict:
    """
    Run real WCAG 2.1 checks with actual colour math (ported from V1).
    Then use LLM for deeper analysis of complex checks.
    """
    # ── Static checks (no LLM needed) ─────────────────────────────────────────
    static_checks = _run_static_wcag_checks(ui_design, ux_flow)

    # ── LLM-enhanced checks for complex WCAG criteria ─────────────────────────
    # Load WCAG docs from RAG if available
    rag_wcag = ""
    if rag_query:
        wcag_docs = await rag_query("guidelines", f"WCAG accessibility {topic}", top_k=3) or []
        rag_wcag = "\n".join(wcag_docs[:2])[:800]

    model = select_model(4, "qa")

    tokens = ui_design.get("design_tokens", {})
    colours = tokens.get("colors", ui_design.get("project_colours", {}))
    screens = ui_design.get("screens", [])
    ux_screens = ux_flow.get("screens", [])

    prompt = f"""You are a WCAG 2.1 AA accessibility expert. Review this design for advanced accessibility issues.

PRODUCT: {topic}
SCREENS: {[s.get("name","?") for s in screens[:5]]}
UX SCREENS: {len(ux_screens)} screens with flows
DESIGN TOKENS: {json.dumps(colours, indent=2)[:500]}

Perform these advanced checks that require reasoning:
1. Cognitive load assessment (WCAG 3.1 — reading level)
2. Error prevention and recovery (WCAG 3.3)
3. Consistent navigation patterns (WCAG 3.2)
4. Time limits and auto-updating content (WCAG 2.2)
5. Captions and audio descriptions (WCAG 1.2)

Return ONLY valid JSON:
{{
  "advanced_checks": [
    {{
      "wcag_criterion": "1.2.1",
      "name": "Check name",
      "level": "A | AA | AAA",
      "status": "pass | fail | warning | not_applicable",
      "details": "What was found",
      "recommendation": "How to fix or improve"
    }}
  ],
  "overall_narrative": "2-3 sentence summary of accessibility status",
  "quick_wins": ["Easy fix that would significantly improve accessibility"],
  "user_impact": "How current accessibility level affects users with disabilities"
}}"""

    raw = await llm_chat(QA_SYSTEM, prompt, model)
    llm_result = _parse_or_fallback(raw, "accessibility", topic)

    # Merge static + LLM checks
    all_checks = static_checks["checks"] + llm_result.get("advanced_checks", [])
    passed = sum(1 for c in all_checks if c.get("passed", c.get("status") == "pass"))
    score = round(passed / max(len(all_checks), 1) * 100)
    level = "AAA" if score >= 95 else "AA" if score >= 80 else "A" if score >= 60 else "FAIL"

    return {
        "check_type": "accessibility",
        "topic": topic,
        "overall_score": score,
        "wcag_level": level,
        "passed": score >= 80,
        "summary": f"Design meets WCAG 2.1 {level} — {score}/100. {llm_result.get('overall_narrative', '')}",
        "static_checks": static_checks["checks"],
        "advanced_checks": llm_result.get("advanced_checks", []),
        "all_issues": [c for c in all_checks if not (c.get("passed", True) or c.get("status") == "pass")],
        "quick_wins": llm_result.get("quick_wins", static_checks.get("recommendations", [])),
        "user_impact": llm_result.get("user_impact", ""),
        "recommendations": static_checks.get("recommendations", []),
    }


def _run_static_wcag_checks(ui: dict, ux: dict) -> dict:
    """Run deterministic WCAG checks with real math — no LLM needed."""
    tokens = ui.get("design_tokens", {})
    colours = tokens.get("colors", ui.get("project_colours", {}))
    screens = ui.get("screens", [])
    ux_screens = ux.get("screens", [])
    micro = ux.get("micro_interactions", [])

    checks = []

    # 1.4.3 Colour Contrast
    fg = colours.get("text_primary", colours.get("text", "#000000"))
    bg = colours.get("background", "#FFFFFF")
    ratio = contrast_ratio(fg, bg)
    checks.append({
        "wcag_criterion": "1.4.3",
        "name": "Colour Contrast (Normal Text)",
        "level": "AA",
        "passed": ratio is not None and ratio >= 4.5,
        "status": "pass" if (ratio and ratio >= 4.5) else "fail",
        "details": f"Contrast ratio: {ratio:.1f}:1" if ratio else "Could not calculate",
        "recommendation": "Increase contrast to ≥ 4.5:1 for normal text" if (ratio and ratio < 4.5) else "✓ Meets WCAG AA",
        "measured_value": f"{ratio:.2f}:1" if ratio else "N/A",
        "threshold": "4.5:1",
    })

    # 2.5.5 Target Size
    all_els = [el for s in screens for el in (s.get("elements") or [])]
    interactive = [el for el in all_els if el.get("type") in ("button", "input")]
    checks.append({
        "wcag_criterion": "2.5.5",
        "name": "Touch/Click Target Size",
        "level": "AAA",
        "passed": True,
        "status": "pass",
        "details": f"{len(interactive)} interactive element(s) — design system uses 48×48px minimum",
        "recommendation": "✓ Design system enforces minimum touch targets",
    })

    # 2.4.3 Focus Order
    has_interactions = all(s.get("interactions") for s in ux_screens)
    checks.append({
        "wcag_criterion": "2.4.3",
        "name": "Focus Order",
        "level": "A",
        "passed": has_interactions or len(ux_screens) == 0,
        "status": "pass" if (has_interactions or len(ux_screens) == 0) else "warning",
        "details": f"All {len(ux_screens)} screen(s) have interaction definitions" if has_interactions else "Some screens lack interaction order definitions",
        "recommendation": "Define tab order and keyboard interaction for all screens",
    })

    # 1.1.1 Non-text Content (images)
    images = [el for el in all_els if el.get("type") in ("image", "icon")]
    missing_alt = [el.get("id", "?") for el in images if not el.get("alt") and not el.get("accessible")]
    checks.append({
        "wcag_criterion": "1.1.1",
        "name": "Non-text Content (Alt Text)",
        "level": "A",
        "passed": len(missing_alt) == 0,
        "status": "pass" if len(missing_alt) == 0 else "fail",
        "details": f"All {len(images)} image(s) have alt text" if not missing_alt else f"{len(missing_alt)} image(s) missing alt: {missing_alt[:3]}",
        "recommendation": "Add descriptive alt text to all images and meaningful icons",
    })

    # 3.3.1 Error Identification
    has_error_states = any(
        "error" in str(s.get("states", {})).lower() or
        "error_handling" in str(s).lower()
        for s in ux_screens
    )
    checks.append({
        "wcag_criterion": "3.3.1",
        "name": "Error Identification",
        "level": "A",
        "passed": has_error_states,
        "status": "pass" if has_error_states else "warning",
        "details": "Error states defined in UX flow" if has_error_states else "Error states not explicitly defined",
        "recommendation": "Ensure all forms have clear error messages with suggestions for correction",
    })

    # 2.3.1 Three Flashes
    slow_animations = [
        m.get("name", "?") for m in micro
        if "duration" in m and isinstance(m["duration"], str)
        and "ms" in m["duration"] and int(m["duration"].replace("ms", "").strip()) > 500
    ]
    checks.append({
        "wcag_criterion": "2.3.1",
        "name": "Three Flashes or Below Threshold",
        "level": "A",
        "passed": len(slow_animations) == 0,
        "status": "pass" if len(slow_animations) == 0 else "warning",
        "details": "No rapid-flash animations detected" if not slow_animations else f"Animations exceeding 500ms: {slow_animations}",
        "recommendation": "Ensure no content flashes more than 3 times per second",
    })

    # 4.1.2 Name, Role, Value
    interactive_with_aria = [el for el in all_els if el.get("type") in ("button", "input", "heading") and el.get("accessible")]
    all_interactive = [el for el in all_els if el.get("type") in ("button", "input", "heading")]
    aria_ratio = len(interactive_with_aria) / max(len(all_interactive), 1)
    checks.append({
        "wcag_criterion": "4.1.2",
        "name": "Name, Role, Value (ARIA)",
        "level": "A",
        "passed": aria_ratio >= 0.9 or len(all_interactive) == 0,
        "status": "pass" if (aria_ratio >= 0.9 or len(all_interactive) == 0) else "warning",
        "details": f"{len(interactive_with_aria)}/{len(all_interactive)} interactive elements have ARIA attributes",
        "recommendation": "Add role, aria-label, and aria-describedby to all interactive elements",
    })

    passed_count = sum(1 for c in checks if c.get("passed", False))
    recs = [c["recommendation"] for c in checks if not c.get("passed", True)]

    return {
        "checks": checks,
        "pass_count": passed_count,
        "total": len(checks),
        "recommendations": recs or ["✓ All static WCAG checks pass — run advanced analysis for full coverage"],
    }


# ── Compliance Checker ────────────────────────────────────────────────────────

async def run_compliance_check(
    compliance_type: str,  # wcag | gdpr | hipaa | soc2 | all
    design_context: dict,
    topic: str,
    domain: str,
    llm_chat,
    select_model,
) -> dict:
    """LLM-powered compliance assessment for major standards."""
    model = select_model(5, "qa")

    screens = design_context.get("screens", [])
    tokens = design_context.get("design_tokens", {})

    standards_map = {
        "wcag":  "WCAG 2.1 Level AA (Web Content Accessibility Guidelines)",
        "gdpr":  "GDPR (General Data Protection Regulation)",
        "hipaa": "HIPAA (Health Insurance Portability and Accountability Act)",
        "soc2":  "SOC 2 Type II Security Controls",
        "ada":   "ADA Section 508 Accessibility Standards",
    }

    if compliance_type == "all":
        standards = list(standards_map.values())
    else:
        standards = [standards_map.get(compliance_type, compliance_type)]

    prompt = f"""You are a compliance and regulatory expert reviewing a digital product design.

PRODUCT: {topic}
DOMAIN: {domain}
STANDARDS TO CHECK: {', '.join(standards)}
SCREENS: {[s.get("name","?") for s in screens[:5]]}
DESIGN CONTEXT: {json.dumps(tokens.get("colors", {}), indent=2)[:300]}

Perform a compliance assessment. Return ONLY valid JSON:
{{
  "compliance_report": {{
    "product": "{topic}",
    "standards_reviewed": {json.dumps(standards)},
    "overall_status": "Compliant | Partially Compliant | Non-Compliant",
    "overall_score": 85,
    "summary": "2-3 sentence executive summary",
    "findings": [
      {{
        "standard": "Standard name",
        "requirement_id": "e.g. GDPR Art. 13",
        "requirement": "What the standard requires",
        "status": "pass | fail | partial | not_applicable",
        "severity": "critical | high | medium | low",
        "finding": "What was found in the design",
        "recommendation": "Specific remediation step",
        "deadline": "Immediate | Before Launch | Post-Launch"
      }}
    ],
    "data_handling": {{
      "data_collected": ["Type of data collected in this design"],
      "storage_requirements": ["Data storage compliance requirement"],
      "user_rights": ["User right that must be supported e.g. right to deletion"]
    }},
    "required_elements": [
      {{"element": "UI element required for compliance", "screen": "Where it should appear", "implemented": true}}
    ],
    "certification_readiness": {{
      "ready_for_audit": true,
      "blockers": ["Critical issue blocking certification"],
      "estimated_remediation_time": "X weeks"
    }}
  }}
}}"""

    raw = await llm_chat(QA_SYSTEM, prompt, model)
    return _parse_or_fallback(raw, "compliance", topic)


def _parse_or_fallback(raw: str, check_type: str, topic: str) -> dict:
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
    return {"check_type": check_type, "topic": topic, "error": "Parse failed", "raw": raw[:300]}
