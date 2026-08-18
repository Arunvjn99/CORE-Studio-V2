"""
Regression tests for the CORE 2.0 ("core-2") design-system fix.

Guards against the three bug classes found while diagnosing why generated
screens didn't match the real Figma product:
1. Fabricated tokens instead of real Figma-derived values.
2. Layout grammar missing / silently truncated out of the prompt.
3. The generic "Stripe/Linear/Coinbase gradient" prompt leaking into core-2
   generation (and, symmetrically, core-2's flat overrides leaking into
   other design systems).

Run:
    cd packages/backend && pytest tests/test_core_design_system.py -v
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from app.design_system.registry import get_design_system, get_system_prompt_injection
from app.agents.design_complete.flow_generator import (
    _get_layout_template,
    _generate_single_screen,
    _build_vision_prompt,
    _extract_html,
    CORE_LAYOUT_TEMPLATES,
    LAYOUT_TEMPLATES,
    CORE_HIFI_SYSTEM,
    HIFI_SYSTEM,
)


SCREEN_PLAN = {
    "name": "Payroll Validation Dashboard",
    "purpose": "Review payroll file validation status",
    "layout_type": "sidebar",
    "content_elements": ["file list", "status badges"],
    "primary_action": "Resolve",
    "screen_type": "web_dashboard",
    "canvas_size": {"width": 1440, "height": 900},
}


def _make_capturing_llm_chat():
    """Returns (llm_chat, calls) — calls[-1] = (system, user, model) of the last invocation."""
    calls = []

    async def llm_chat(system, user, model):
        calls.append((system, user, model))
        return '<div class="w-full min-h-screen">stub screen content long enough to pass the length check............</div>'

    return llm_chat, calls


# ─────────────────────────────────────────────────────────────────────────────
# 1. Token correctness — core-2 must use the real Figma-derived values
# ─────────────────────────────────────────────────────────────────────────────

def test_core2_primary_color_matches_figma():
    ds = get_design_system("core-2")
    assert ds["tokens"]["colors"]["primary"] == "#004DCB"


def test_core2_font_is_open_sans():
    ds = get_design_system("core-2")
    assert "Open Sans" in ds["tokens"]["typography"]["font_family"]


def test_core2_spacing_scale_matches_figma():
    ds = get_design_system("core-2")
    assert ds["tokens"]["spacing"]["scale"] == [4, 8, 12, 16, 24, 32, 48]


def test_core2_shadows_are_neutral_not_colored():
    ds = get_design_system("core-2")
    shadows = ds["tokens"]["shadows"]
    # Regression guard: none of the elevation shadows may carry a primary-color tint —
    # the real Figma shadows are neutral grey.
    for key in ("sm", "md", "lg"):
        assert "004DCB" not in shadows[key]


# ─────────────────────────────────────────────────────────────────────────────
# 2. Layout grammar must be present in the injected prompt and never truncated
# ─────────────────────────────────────────────────────────────────────────────

EXPECTED_TEMPLATE_KEYS = [
    "shell_sidebar",
    "shell_topnav",
    "split_wizard",
    "panel_header_body_footer",
    "auth_split",
]


def test_core2_layout_templates_present_in_registry():
    ds = get_design_system("core-2")
    for key in EXPECTED_TEMPLATE_KEYS:
        assert key in ds["layout_templates"]


def test_core2_prompt_injection_includes_full_layout_grammar():
    prompt = get_system_prompt_injection("core-2")
    assert "PAGE LAYOUT TEMPLATES" in prompt
    for key in EXPECTED_TEMPLATE_KEYS:
        assert key in prompt


def test_other_design_system_prompt_has_no_layout_grammar_block():
    # Regression guard: the layout-grammar injection must not leak into
    # design systems that don't define layout_templates.
    prompt = get_system_prompt_injection("stripe")
    assert "PAGE LAYOUT TEMPLATES" not in prompt


# ─────────────────────────────────────────────────────────────────────────────
# 3. _get_layout_template branching — core-2 gets exact-pixel templates,
#    every other design system is completely unaffected (byte-identical to
#    the pre-fix behavior).
# ─────────────────────────────────────────────────────────────────────────────

GENERIC_LAYOUT_TYPES = ["dashboard", "sidebar", "list", "form", "detail", "confirmation", "centered", "settings"]


@pytest.mark.parametrize("layout_type", GENERIC_LAYOUT_TYPES)
def test_core2_layout_template_uses_mined_pixel_values(layout_type):
    tpl = _get_layout_template(layout_type, "core-2")
    assert tpl == CORE_LAYOUT_TEMPLATES.get(layout_type, CORE_LAYOUT_TEMPLATES["sidebar"])
    # Every core template should reference a real mined dimension somewhere.
    assert any(px in tpl for px in ("100px", "66px", "96px", "72px", "592px", "848px", "61px", "890px", "73px", "638px", "803px"))


@pytest.mark.parametrize("layout_type", GENERIC_LAYOUT_TYPES)
def test_other_design_system_layout_template_unchanged(layout_type):
    # No design_system_id passed (defaults to "") — must exactly match pre-fix behavior.
    tpl_default = _get_layout_template(layout_type)
    tpl_stripe = _get_layout_template(layout_type, "stripe")
    expected = LAYOUT_TEMPLATES.get(layout_type, LAYOUT_TEMPLATES["detail"])
    assert tpl_default == expected
    assert tpl_stripe == expected
    # Must NOT pick up core-2's mined pixel values.
    assert "592px" not in tpl_stripe


def test_unknown_layout_type_falls_back_safely():
    # Guards against a KeyError if the planner emits a layout_type outside the known set.
    assert _get_layout_template("some_unknown_type", "core-2") == CORE_LAYOUT_TEMPLATES["sidebar"]
    assert _get_layout_template("some_unknown_type", "stripe") == LAYOUT_TEMPLATES["detail"]
    assert _get_layout_template("some_unknown_type") == LAYOUT_TEMPLATES["detail"]


# ─────────────────────────────────────────────────────────────────────────────
# 4. System prompt selection — core-2 must never receive the generic
#    "Stripe/Linear/Coinbase gradient" system prompt, and other design
#    systems must never receive the flat core-2 one.
# ─────────────────────────────────────────────────────────────────────────────

def test_core_hifi_system_forbids_gradients():
    assert "gradient" in CORE_HIFI_SYSTEM.lower()
    assert "FORBIDDEN" in CORE_HIFI_SYSTEM
    assert "Stripe" not in CORE_HIFI_SYSTEM


def test_generic_hifi_system_unchanged():
    # Regression guard: the original generic prompt used by every non-core
    # design system must still ask for the modern gradient-rich look.
    assert "Stripe, Linear, Vercel, or Coinbase" in HIFI_SYSTEM
    assert "gradients" in HIFI_SYSTEM.lower()


# ─────────────────────────────────────────────────────────────────────────────
# 5. End-to-end prompt-content regression — the exact bug reported: core-2
#    generation must use the flat system prompt / no gradients, and other
#    design systems must be completely unaffected.
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_core2_screen_generation_uses_flat_system_prompt():
    ds = get_design_system("core-2")
    ds_block = get_system_prompt_injection("core-2")
    llm_chat, calls = _make_capturing_llm_chat()

    await _generate_single_screen(
        screen_plan=SCREEN_PLAN, fidelity="hifi", design_system=ds, ds_prompt_block=ds_block,
        rag_context="", user_prompt="Create a Payroll Validation screen",
        flow_context={"domain": "retirement"}, image_analysis=None,
        llm_chat=llm_chat, select_model=lambda *a, **k: "stub-model",
    )

    system, user, model = calls[-1]
    assert system == CORE_HIFI_SYSTEM
    # "linear-gradient" appears in our own forbidden-pattern reminder text
    # ("no linear-gradient, radial-gradient..."), so check it's never used as
    # an actual CSS value rather than merely absent as a substring.
    assert "background:linear-gradient" not in user
    assert "background: linear-gradient" not in user
    assert "Stripe, Linear, or Coinbase" not in user
    assert "shell_sidebar" in user or "PAGE LAYOUT TEMPLATES" in user


@pytest.mark.asyncio
async def test_other_design_system_still_uses_generic_gradient_prompt():
    ds = get_design_system("stripe")
    ds_block = get_system_prompt_injection("stripe")
    llm_chat, calls = _make_capturing_llm_chat()

    await _generate_single_screen(
        screen_plan=SCREEN_PLAN, fidelity="hifi", design_system=ds, ds_prompt_block=ds_block,
        rag_context="", user_prompt="Create a Payroll Validation screen",
        flow_context={"domain": "retirement"}, image_analysis=None,
        llm_chat=llm_chat, select_model=lambda *a, **k: "stub-model",
    )

    system, user, model = calls[-1]
    assert system == HIFI_SYSTEM
    assert "Stripe, Linear, or Coinbase" in user


# ─────────────────────────────────────────────────────────────────────────────
# 4. No missing-key crashes — a hypothetical design system with a sparse
#    tokens dict (or core-2 tagged onto minimal tokens) must not raise KeyError.
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_core2_generation_survives_sparse_tokens():
    sparse_ds = {
        "name": "Sparse Core",
        "design_system_id": "core-2",
        "tokens": {"colors": {}, "typography": {}, "radius": {}, "shadows": {}},
    }
    llm_chat, calls = _make_capturing_llm_chat()

    result = await _generate_single_screen(
        screen_plan=SCREEN_PLAN, fidelity="hifi", design_system=sparse_ds, ds_prompt_block="",
        rag_context="", user_prompt="Create a Payroll Validation screen",
        flow_context={"domain": "retirement"}, image_analysis=None,
        llm_chat=llm_chat, select_model=lambda *a, **k: "stub-model",
    )

    assert "html" in result  # did not raise KeyError building the prompt


# ─────────────────────────────────────────────────────────────────────────────
# 6. Brand mark (logo) — must be injected for core-2, must not leak elsewhere
# ─────────────────────────────────────────────────────────────────────────────

def test_core2_logo_snippet_present_in_registry():
    ds = get_design_system("core-2")
    # Real logo mined from Figma via get_design_context: exact vector paths + exact colors
    # (#292670 navy, #BA141A red) pulled from the Dev Mode MCP asset server.
    assert "path" in ds["logo_snippet"]
    assert "#292670" in ds["logo_snippet"]
    assert "#BA141A" in ds["logo_snippet"]


def test_core2_prompt_injection_includes_brand_mark():
    prompt = get_system_prompt_injection("core-2")
    assert "BRAND MARK" in prompt
    assert "#004DCB" in prompt


def test_other_design_system_prompt_has_no_brand_mark_block():
    prompt = get_system_prompt_injection("stripe")
    assert "BRAND MARK" not in prompt


@pytest.mark.asyncio
async def test_core2_generation_requires_logo_and_density():
    ds = get_design_system("core-2")
    ds_block = get_system_prompt_injection("core-2")
    llm_chat, calls = _make_capturing_llm_chat()

    await _generate_single_screen(
        screen_plan=SCREEN_PLAN, fidelity="hifi", design_system=ds, ds_prompt_block=ds_block,
        rag_context="", user_prompt="Create a Payroll Validation screen",
        flow_context={"domain": "retirement"}, image_analysis=None,
        llm_chat=llm_chat, select_model=lambda *a, **k: "stub-model",
    )

    system, user, model = calls[-1]
    assert "BRAND MARK" in user
    assert "#292670" in user and "#BA141A" in user  # exact logo colors present
    assert "DENSITY REQUIREMENT" in user
    assert "AT LEAST\n3 distinct content sections" in user or "AT LEAST 3 distinct content sections" in user.replace("\n", " ")


@pytest.mark.asyncio
async def test_other_design_system_generation_unaffected_by_logo_density_rules():
    ds = get_design_system("stripe")
    ds_block = get_system_prompt_injection("stripe")
    llm_chat, calls = _make_capturing_llm_chat()

    await _generate_single_screen(
        screen_plan=SCREEN_PLAN, fidelity="hifi", design_system=ds, ds_prompt_block=ds_block,
        rag_context="", user_prompt="Create a Payroll Validation screen",
        flow_context={"domain": "retirement"}, image_analysis=None,
        llm_chat=llm_chat, select_model=lambda *a, **k: "stub-model",
    )

    system, user, model = calls[-1]
    assert "BRAND MARK" not in user
    assert "DENSITY REQUIREMENT" not in user


# ─────────────────────────────────────────────────────────────────────────────
# 7. Recreate-mode image analysis accuracy — guards against the "recreate returns
#    an unrelated but domain-similar screen" bug (e.g. a reference titled "Manage
#    Year End Process" coming back planned as a generic "Plans" page instead).
# ─────────────────────────────────────────────────────────────────────────────

def test_recreate_vision_prompt_demands_verbatim_title():
    prompt = _build_vision_prompt("recreate", "recreate this screen")
    assert "exact_title_text" in prompt
    assert "exact_labels" in prompt
    assert "verbatim" in prompt.lower()
    # Regression guard for the literal bug reported: the schema must warn against
    # substituting a different, "similar" domain screen name.
    assert "Plans" in prompt  # the counter-example used in the instruction itself


def test_extract_html_handles_raw_html_without_json_wrapper():
    # Regression guard for the truncation bug: _generate_screen_from_image now asks
    # for raw HTML (no JSON wrapper) — confirm _extract_html handles that correctly
    # end-to-end, including a full multi-section page, not just the first tag.
    raw = (
        "<!DOCTYPE html><html><body>"
        "<div><div>Section 1</div><div>Section 2</div><div>Section 3</div></div>"
        "</body></html>"
    )
    html = _extract_html(raw)
    assert "Section 1" in html
    assert "Section 2" in html
    assert "Section 3" in html  # would have been truncated by the old first-closing-tag regex


def test_extract_html_strips_markdown_fences_around_raw_html():
    raw = "```html\n<div><div>A</div><div>B</div></div>\n```"
    html = _extract_html(raw)
    assert "A" in html and "B" in html
    assert "```" not in html


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
