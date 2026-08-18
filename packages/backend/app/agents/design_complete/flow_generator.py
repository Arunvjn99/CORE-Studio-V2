"""
Multi-Screen Flow Generator — Production HIFI Quality
- UX Magic-level design output: layered depth, gradients, modern effects
- Domain-aware component patterns (financial, healthcare, etc.)
- Always runs RAG retrieval before LLM call
- Returns N rendered screens as an editable canvas flow
"""
import json
import re
import base64
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPTS
# ─────────────────────────────────────────────────────────────────────────────

WIREFRAME_SYSTEM = """You are a senior UX designer creating precise low-fidelity wireframes.
Rules:
- ONLY grayscale — bg-gray-50/100/200/300, text-gray-400/600/800, border-gray-200
- Text blocks = <div class="h-3 bg-gray-200 rounded mb-2" style="width:72%"></div>
- Images = <div class="bg-gray-100 rounded-xl flex items-center justify-center text-gray-400 text-xs font-medium" style="aspect-ratio:16/9">Image</div>
- Buttons = <div class="bg-gray-800 text-white rounded-xl px-4 py-2.5 text-sm font-medium text-center">Label</div>
- Cards = <div class="bg-white rounded-2xl border border-gray-200 p-5">
- Nav = <div class="flex items-center justify-between h-14 px-4 bg-white border-b border-gray-200">
- Show STRUCTURE clearly — section labels, button labels, field labels are real text
- NO color anywhere except grayscale
Output raw HTML starting with <div. No markdown. No JSON."""

HIFI_SYSTEM = """You are a world-class product designer and frontend engineer at a top-tier tech company.
Your screens look indistinguishable from Stripe, Linear, Vercel, or Coinbase — clean, modern, deeply polished.

YOUR DESIGN PHILOSOPHY:
1. DEPTH over flatness — every screen has foreground, midground, background layers
2. COLOR with intention — primary color used in gradients, tints, glows, not just flat fills
3. TYPOGRAPHY that breathes — generous whitespace, clear hierarchy, display numbers for data
4. MOTION implied — hover states, transitions described via opacity/transform classes
5. CONTENT is king — realistic domain-specific data, not placeholders
6. MODERN effects — gradients, subtle glassmorphism, layered shadows, tinted backgrounds

FORBIDDEN:
- Flat white cards with only a thin border (use shadow + slight tint instead)
- Generic grey placeholders for any text (use real content)
- Simple flat color buttons without depth (add gradient or subtle shadow)
- Uniform spacing everywhere (vary density to create rhythm)
- lorem ipsum or "Label" as text (use real domain content)

Output raw HTML starting with <div. No markdown fences. No JSON. No HTML comments."""

# CORE 2.0 — faithful reproduction mode. Used instead of HIFI_SYSTEM whenever
# design_system_id == "core-2": the goal here is the OPPOSITE of the generic
# system above — indistinguishable from the company's own existing screens,
# not a generic modern SaaS look.
CORE_HIFI_SYSTEM = """You are the in-house product designer for this company's enterprise platform.
Your job is to produce screens that are INDISTINGUISHABLE from the company's own existing
product screens — same shell, same spacing, same flat visual language. You are not designing
a new look; you are extending an existing one.

YOUR DESIGN PHILOSOPHY:
1. STRUCTURE is locked — reuse the exact page-layout template provided (shell type, sidebar/
   navbar dimensions, section order). You may only fill the named content slot.
2. FLAT surfaces — white/light-grey fills, hairline borders, at most a soft ambient shadow
   (Shadow1/2/3 from the token list). Never a gradient, never a glow, never a decorative blob.
3. ONE accent — the primary blue appears only on primary buttons, active/selected states,
   links, and focus rings. Everything else is neutral grey/white.
4. REAL content — realistic retirement/401k/enterprise data (plan names, employee names,
   dollar amounts, dates), never lorem ipsum or "Label".
5. DENSITY over decoration — enterprise data tables and forms are dense and functional,
   not spaced out for marketing effect.

FORBIDDEN (these break the "looks like our product" goal):
- Any linear-gradient, radial-gradient, or conic-gradient anywhere
- Decorative background blobs/orbs/blur shapes
- backdrop-filter / glassmorphism
- Colored glows or tinted box-shadows (box-shadow color must be neutral grey/black only)
- Changing the sidebar width, navbar height, or section order specified by the layout template
- Rounded pill-shaped hero cards with white text on a color fill

Output raw HTML starting with <div. No markdown fences. No JSON. No HTML comments."""

# Flat equivalent of MODERN_EFFECTS — no gradients/orbs/glass, just the real
# Shadow1/2/3 + focus-ring tokens extracted from the Figma file.
CORE_FLAT_EFFECTS = """
════════════ CORE 2.0 SURFACE TOOLKIT (flat — no gradients/orbs/glass) ════════════
CARD / PANEL:
  background:{surface}; border:1px solid {border}; border-radius:8px; box-shadow:{shadow_sm};

RAISED CARD (dropdowns, popovers, tooltips):
  background:{surface}; border-radius:8px; box-shadow:{shadow_md};

MODAL / FLOATING PANEL:
  background:{surface}; border-radius:8px; box-shadow:{shadow_lg};

PRIMARY BUTTON (flat, no gradient):
  background:{primary}; color:#FFFFFF; border-radius:8px; padding:10px 20px; font-weight:600; border:none;
SECONDARY BUTTON:
  background:{surface}; color:{text1}; border:1.5px solid {border}; border-radius:8px; padding:9px 20px; font-weight:500;

STATUS BADGE (flat tint, no glow):
  Success: background:{success_light}; color:{success}; border-radius:16px; padding:3px 10px; font-size:12px; font-weight:600;
  Warning: background:{warning_light}; color:{warning}; border-radius:16px; padding:3px 10px; font-size:12px; font-weight:600;
  Critical: background:{error_light}; color:{error}; border-radius:16px; padding:3px 10px; font-size:12px; font-weight:600;

ACTIVE / SELECTED ROW:
  background:{primary_light}; border-left:3px solid {primary};

FOCUS RING (every interactive element):
  box-shadow:{focus_default};

TABLE HEADER ROW:
  background:{surface_subtle}; border-bottom:2px solid {border}; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.04em; color:{text2};

TABLE DATA ROW:
  border-bottom:1px solid {border}; padding:14px 16px; font-size:14px; color:{text2};
"""


# ─────────────────────────────────────────────────────────────────────────────
# MODERN DESIGN EFFECTS LIBRARY (injected into every HIFI prompt)
# ─────────────────────────────────────────────────────────────────────────────

MODERN_EFFECTS = """
════════════ MODERN CSS EFFECTS TOOLKIT ════════════
Use these techniques to add visual depth and modernity. Choose what fits each screen.

GRADIENT BACKGROUNDS (for hero sections, summary cards, CTAs):
  Solid gradient:      background: linear-gradient(135deg, {primary} 0%, {primary_dark} 100%);
  Soft mesh gradient:  background: linear-gradient(135deg, {primary}15 0%, {primary}08 50%, transparent 100%);
  Diagonal stripe bg:  background: linear-gradient(135deg, {bg} 60%, {primary}08 100%);

GLASSMORPHISM CARD (for cards that float over gradient backgrounds):
  backdrop-filter: blur(20px); background: rgba(255,255,255,0.85); border: 1px solid rgba(255,255,255,0.6); box-shadow: 0 8px 32px rgba(0,0,0,0.08);

LAYERED CARD SHADOWS (choose depth level):
  Level 1 (subtle):  box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  Level 2 (raised):  box-shadow: 0 4px 16px rgba(0,0,0,0.08), 0 1px 4px rgba(0,0,0,0.04);
  Level 3 (floating):box-shadow: 0 20px 40px rgba(0,0,0,0.12), 0 4px 12px rgba(0,0,0,0.06);
  Colored glow:      box-shadow: 0 8px 24px {primary}30;

GRADIENT BUTTONS (much richer than flat color):
  Primary gradient: background: linear-gradient(135deg, {primary} 0%, {primary_dark} 100%); box-shadow: 0 4px 12px {primary}40;
  Tinted outline:   background: {primary}10; border: 1.5px solid {primary}30; color: {primary};

TINTED SURFACES (for section backgrounds, alternating rows):
  Warm tint:   background: {primary}06;
  Active row:  background: {primary}0D; border-left: 3px solid {primary};
  Highlight:   background: linear-gradient(90deg, {primary}12 0%, transparent 100%);

DECORATIVE ELEMENTS (add visual interest):
  Background orb:  <div style="position:absolute;top:-60px;right:-60px;width:200px;height:200px;border-radius:50%;background:{primary}15;filter:blur(40px);pointer-events:none;"></div>
  Accent dot:      <div style="width:8px;height:8px;border-radius:50%;background:{primary};"></div>
  Gradient line:   <div style="height:3px;background:linear-gradient(90deg,{primary},transparent);border-radius:2px;"></div>
  Icon container:  <div style="width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,{primary}20,{primary}10);display:flex;align-items:center;justify-content:center;">

HERO/SUMMARY CARD PATTERN (financial dashboards):
  <div style="background:linear-gradient(135deg,{primary} 0%,{primary_dark} 100%);border-radius:24px;padding:24px;color:white;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-30px;right:-30px;width:150px;height:150px;border-radius:50%;background:rgba(255,255,255,0.08);"></div>
    <div style="position:absolute;bottom:-40px;left:20px;width:100px;height:100px;border-radius:50%;background:rgba(255,255,255,0.06);"></div>
    <!-- content above decorative circles -->
  </div>

METRIC/STAT TILE:
  <div style="background:{surface};border-radius:20px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
    <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:{text2};margin-bottom:6px;">METRIC NAME</div>
    <div style="font-size:32px;font-weight:800;color:{text1};line-height:1;">$12,450</div>
    <div style="display:flex;align-items:center;gap:4px;margin-top:8px;">
      <span style="font-size:11px;font-weight:600;color:{success};background:{success}15;padding:2px 8px;border-radius:20px;">↑ 12.4%</span>
      <span style="font-size:11px;color:{text2};">vs last month</span>
    </div>
  </div>

PROGRESS RING (CSS-only for loan payoff, contribution %):
  <div style="width:80px;height:80px;border-radius:50%;background:conic-gradient({primary} 0% 50%, {border} 50% 100%);display:flex;align-items:center;justify-content:center;">
    <div style="width:60px;height:60px;border-radius:50%;background:{surface};display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:{text1};">50%</div>
  </div>

STEP TRACKER / STEPPER:
  <div style="display:flex;align-items:center;gap:0;margin-bottom:24px;">
    <div style="width:32px;height:32px;border-radius:50%;background:{primary};color:white;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0;">1</div>
    <div style="flex:1;height:2px;background:linear-gradient(90deg,{primary},{primary}40);"></div>
    <div style="width:32px;height:32px;border-radius:50%;background:{primary}20;color:{primary};display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;border:2px solid {primary}40;flex-shrink:0;">2</div>
    <div style="flex:1;height:2px;background:{border};"></div>
    <div style="width:32px;height:32px;border-radius:50%;background:{border};color:{text2};display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0;">3</div>
  </div>

AMOUNT INPUT (financial):
  <div style="background:{bg};border:2px solid {primary};border-radius:16px;padding:16px 20px;display:flex;align-items:center;gap:8px;">
    <span style="font-size:28px;font-weight:300;color:{text2};">$</span>
    <input style="flex:1;font-size:32px;font-weight:700;color:{text1};border:none;background:transparent;outline:none;" placeholder="0.00" />
  </div>

TAB / SEGMENTED CONTROL:
  <div style="background:{bg};border-radius:12px;padding:4px;display:flex;border:1px solid {border};">
    <div style="flex:1;background:{primary};color:white;border-radius:8px;padding:8px 12px;text-align:center;font-size:13px;font-weight:600;">Active Tab</div>
    <div style="flex:1;color:{text2};border-radius:8px;padding:8px 12px;text-align:center;font-size:13px;font-weight:500;">Tab 2</div>
    <div style="flex:1;color:{text2};border-radius:8px;padding:8px 12px;text-align:center;font-size:13px;font-weight:500;">Tab 3</div>
  </div>

NOTIFICATION / ALERT BANNER:
  <div style="background:linear-gradient(90deg,{primary}15,{primary}08);border-left:4px solid {primary};border-radius:12px;padding:14px 16px;display:flex;align-items:flex-start;gap:12px;">
    <div style="width:20px;height:20px;border-radius:50%;background:{primary};display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:11px;color:white;font-weight:700;">!</div>
    <div><div style="font-size:13px;font-weight:600;color:{text1};">Alert title</div><div style="font-size:12px;color:{text2};margin-top:2px;">Alert description text here</div></div>
  </div>
"""


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT TEMPLATES — the LLM gets a structural blueprint per layout_type
# ─────────────────────────────────────────────────────────────────────────────

LAYOUT_TEMPLATES = {
    "dashboard": """
DASHBOARD LAYOUT BLUEPRINT (DESKTOP — sidebar + main):
  [Sidebar 240px: logo, nav items with icons, section labels, user profile at bottom]
  [Main area: page header (title + primary CTA button), metric tiles 3-4 column grid]
  [Content tables or card lists with section headers and "View All" links]
  [Secondary panel or chart area below metrics]
  NOTE: NO bottom tab bar — this is a desktop dashboard, use left sidebar navigation
""",
    "detail": """
DETAIL SCREEN LAYOUT BLUEPRINT:
  [Back nav + title + action button (e.g. "Edit")]
  [Hero summary card — colored gradient, key metric in large text, secondary stats]
  [Info section — labeled rows (data key: value pairs)]
  [Action section — related actions as tappable rows with arrows]
  [CTA at bottom — primary button full-width]
""",
    "form": """
FORM LAYOUT BLUEPRINT:
  [Progress indicator — step X of N + progress bar]
  [Section heading + subtext describing this step]
  [Form fields — label (uppercase, small) + input field pairs, grouped in cards]
  [Optional: helper text or info card explaining a field]
  [Primary CTA at bottom — "Continue" or "Submit"]
  [Secondary action — "Save Draft" or "Back"]
""",
    "confirmation": """
CONFIRMATION / SUCCESS LAYOUT BLUEPRINT:
  [Large success icon or animation placeholder — centered, colored]
  [Success heading — e.g. "Payment Successful!" in bold large text]
  [Transaction summary card — key details of what was completed]
  [What's next section — 2-3 follow-up actions or information]
  [Primary CTA — "Done" or "View Receipt"]
  [Secondary link — "Make Another Payment"]
""",
    "list": """
LIST / HISTORY LAYOUT BLUEPRINT:
  [Search bar + filter chips row]
  [Section header with count badge]
  [List items — consistent rows with: icon + primary text + secondary text + value/badge]
  [Dividers between date groups (e.g. "January 2024")]
  [Empty state if no data — centered illustration + message + CTA]
""",
    "centered": """
CENTERED / ONBOARDING LAYOUT BLUEPRINT:
  [Decorative element — gradient orb, illustration area, or icon badge at top center]
  [Headline — 28-32px bold, centered, 2-3 lines max]
  [Subtext — 15-16px, muted color, 2-3 lines]
  [Content card or feature list]
  [Primary CTA — full width at bottom]
  [Secondary action or trust indicator below CTA]
""",
    "sidebar": """
SIDEBAR / SPLIT LAYOUT BLUEPRINT (DESKTOP — fixed sidebar + scrollable main):
  [Top nav bar: logo left, user actions right, 60px height, sticky]
  [Left sidebar 240px: fixed, nav items with icons, active state highlighted, section labels]
  [Main content flex-1: px-8 py-6, page title + actions header, 3-4 column metric grid, tables/cards]
  [Optional right panel 320px: contextual info, quick stats, activity feed]
  NOTE: Full 1440px width layout — no mobile padding or single-column stacking
""",
}


# CORE 2.0 — exact-pixel shells mined from the real Figma reference screens.
# Keyed by the SAME generic layout_type strings the planner already emits, so no
# other call site needs to change; only core-2 requests route here.
CORE_LAYOUT_TEMPLATES = {
    "dashboard": """
CORE SHELL — TOP NAVBAR + ICON RAIL (mined from Dashboard-enrolled, 3 consistent samples):
  Canvas 1440x1024.
  [Full-width top Navbar: height=72px, x=0,y=0,width=1440]
  [Icon rail Menubar: width=96px, below navbar at x=0,y=72,height=952]
  [Content area: x=96,y=72,width=1344,height=952 — ONLY this region varies]
  Do NOT combine with the 100px/66px sidebar shell below — this is a distinct, separate shell.
""",
    "sidebar": """
CORE SHELL — SIDEBAR + NAVBAR (mined from Payroll File Info, 4 consistent samples):
  Canvas 1440x900.
  [Fixed left sidebar 'Side Menu bar - Light': width=100px, full height]
  [Top navbar 'Navbar - Top': height=66px, spans x=100..1440]
  [Content area: x=100,y=66,width=1340,height=834 — ONLY this region varies]
""",
    "list": """
CORE SHELL — SIDEBAR + NAVBAR (same shell as 'sidebar' — reuse exactly):
  Canvas 1440x900. Sidebar 100px + Navbar 66px + content 1340x834.
  Content region: dense enterprise data table with header row (uppercase 12px labels),
  sortable columns, filter bar above the table, pagination footer. Flat rows, no gradients.
""",
    "form": """
CORE SPLIT WIZARD (mined from Questionnaire-1..6, 4+ consistent samples):
  Canvas 1440x1024.
  [Left rail: width=592px, full height — step indicator / context]
  [Right form panel: width=848px, x=592 — inner content padded x=84,y=72,width=680,height~=649]
""",
    "detail": """
CORE SHELL — APP BAR + NAVBAR (mined from Admin Dashborad ×4 + Employee details):
  Canvas 1440x900.
  [Icon rail 'App Bar': width=96px, full height, x=0,y=0]
  [Top navbar 'Navbar - Top': height=64px, spans x=98..1440]
  [Content area: x=98,y=67,width=1342,height=833 — ONLY this region varies]
  DISTINCT from 'dashboard' shell (72px navbar) and 'sidebar' shell (100px sidebar/66px navbar) —
  this shell uses a 96px rail with a 64px navbar. Use for record-detail / admin dashboards.
""",
    "confirmation": """
CORE HEADER-BODY-FOOTER PANEL (mined from Choose Investment ×9 + Risk level acknowledgement ×7):
  Canvas 1100x1024. This is an embedded panel/drawer — NO sidebar/navbar shell.
  [Header: height=61px, title left-aligned, ~24px padding]
  [Body: height=890px, scrollable primary content]
  [Footer: height=73px, right-aligned action buttons, ~24px right margin]
""",
    "centered": """
CORE AUTH SPLIT (mined from Login with password, 5 consistent samples):
  Canvas 1441x1019. NO app shell (no sidebar/navbar — auth screens are shell-free).
  [Left decorative/illustration column: width=638px]
  [Right form column: width=803px]
""",
    "settings": """
CORE SHELL — APP BAR + NAVBAR + NESTED SIDE MENU (mined from Plan -Sponsor, Plan - Basic Details,
Confg - Plan details — 3 consistent samples):
  Canvas 1440x900.
  [Icon rail 'App Bar': width=96px, full height]
  [Top navbar 'Navbar - Top': height=64px]
  [Secondary in-page 'Plan details-sidemenu': width=317px, full content height (836px), directly
   after the rail/navbar]
  [Remaining content area: ~1025px wide — ONLY this region varies]
  Use for settings/configuration/multi-section-form screens. The secondary side menu is the key
  structural signal — do not substitute a generic tab bar or accordion for it.
""",
}


def _get_layout_template(layout_type: str, design_system_id: str = "") -> str:
    if design_system_id == "core-2":
        return CORE_LAYOUT_TEMPLATES.get(layout_type, CORE_LAYOUT_TEMPLATES["sidebar"])
    return LAYOUT_TEMPLATES.get(layout_type, LAYOUT_TEMPLATES["detail"])


# ─────────────────────────────────────────────────────────────────────────────
# DOMAIN COMPONENT PATTERNS
# ─────────────────────────────────────────────────────────────────────────────

DOMAIN_COMPONENTS = {
    "loan": """
LOAN MODULE COMPONENTS — use realistic financial data:
- Hero summary card: gradient bg, "Current Balance $12,450.00", progress bar (50.2% paid), "On Track ✓" badge
- Loan info chips row: "4.25% APR" · "60 months" · "Matures Jan 2029" as pill badges
- Next payment card: "Next Payment" heading, large "$258.33", "Due March 15, 2024", "Principal $195 · Interest $63"
- Payment breakdown row: principal/interest split with colored mini bar
- Payment schedule table: Date | Payment | Principal | Interest | Balance columns
- Payoff calculator: amount input + "Calculate" → shows "Save $1,240 by paying extra $100/month"
- Payment method: "💳 Chase Checking ····2847" with radio selection
- Quick pay buttons: "$258.33 Min" · "$500 Extra" · "$12,450 Pay Off" selection cards
- Status timeline: loan start → current → maturity with progress marker
""",
    "retirement": """
RETIREMENT / 401K COMPONENTS — use realistic retirement data:
- Portfolio summary: gradient card, "Total Value $284,521.40", "+$12,840 (4.7%)" YTD badge
- Contribution summary: "You: 8% · Employer: 4% · Total: $1,840/mo" with edit link
- Allocation breakdown: colored segment bar (Stocks 70% · Bonds 20% · Cash 10%) + legend
- Fund performance row: "Vanguard S&P 500 · 0.03% fee · +18.4% 1Y · $198,164 (69.7%)"
- Retirement projection card: "Projected at 65: $2.1M" with "On Track" vs "Behind" status
- Beneficiary row: avatar initial + "Sarah Johnson · Spouse · 60%"
- Action tiles: "Increase Contribution ↑" · "Rebalance Portfolio ⟳" · "View Statements 📄"
- Vesting schedule: progress bar showing "Vested: 60% · Fully vested in 2 yrs"
""",
    "banking": """
BANKING COMPONENTS:
- Account overview: account name + last 4 digits + "Available $8,420.50" large + "Ledger $8,510.00"
- Transaction row: colored category icon circle + merchant name + "Grocery" chip + "-$84.20" right + "Jan 12"
- Transfer screen: "From" card selector + "To" card selector + amount keypad
- Spending donut: colored circle + "Food $840 · Transport $320 · Entertainment $180"
- Quick transfer: avatar circles for frequent payees with "+" add button
""",
    "insurance": """
INSURANCE COMPONENTS:
- Policy card: policy number chip + "Auto Insurance" heading + "$500K coverage" + "Premium: $284/mo" + renewal date
- Claims status stepper: Filed (✓ done) → Under Review (active/highlighted) → Decision → Paid
- Coverage checklist: item + green checkmark / red X with coverage limit
- Premium calculator: slider for coverage amount → live premium update
""",
    "healthcare": """
HEALTHCARE COMPONENTS:
- Appointment card: doctor avatar initial + "Dr. Sarah Kim · Cardiologist" + "Jan 15, 9:00 AM" + "Virtual" chip
- Vitals row: metric icon + name + big value + "Normal" green badge + sparkline
- Prescription tile: pill icon + "Lisinopril 10mg · 1x daily" + "28 refills left" + "Refill" button
- Health score circle: large ring chart + score number + "Excellent" label
""",
    "ecommerce": """
ECOMMERCE COMPONENTS:
- Product card: image placeholder + product name + rating stars + price + "Add to Cart"
- Cart summary: item rows with thumbnail + qty selector + price + total footer
- Order status: shipped/delivered tracker steps + carrier info + delivery estimate
""",
}


def _get_domain_components(domain: str) -> str:
    return DOMAIN_COMPONENTS.get(domain.lower(), "")


# ─────────────────────────────────────────────────────────────────────────────
# MULTI-SCREEN FLOW GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

async def generate_screen_flow(
    prompt: str,
    design_system_id: str,
    fidelity: str,           # "wireframe" | "hifi"
    screen_count: int,
    domain: str,
    reference_image_b64: Optional[str],
    reference_mode: Optional[str],
    llm_chat,
    llm_chat_vision,
    select_model,
    rag_query,
    progress_callback=None,
) -> dict:
    from app.design_system.registry import get_design_system, get_system_prompt_injection

    ds = get_design_system(design_system_id)
    ds_prompt_block = get_system_prompt_injection(design_system_id)

    # Step 1: Reference image analysis
    image_analysis = None
    if reference_image_b64 and reference_mode:
        if progress_callback:
            await progress_callback({"type": "step_start", "step": "vision", "message": "🔍 Analyzing reference image..."})
        vision_prompt = _build_vision_prompt(reference_mode, prompt)
        try:
            raw = await llm_chat_vision(reference_image_b64, vision_prompt)
            image_analysis = _parse_json(raw) or {"raw_analysis": raw[:800]}
        except Exception as e:
            image_analysis = {"error": str(e)}
        if progress_callback:
            await progress_callback({"type": "step_complete", "step": "vision", "message": "✓ Image analyzed", "data": image_analysis})

    # Step 2: RAG retrieval
    if progress_callback:
        await progress_callback({"type": "step_start", "step": "rag", "message": f"📚 Retrieving knowledge for {domain}..."})

    domain_docs     = await rag_query("guidelines",        f"{domain} {prompt}",                              top_k=4) or []
    company_docs    = await rag_query("company_standards", f"UX standards {prompt}",                          top_k=3) or []
    compliance_docs = await rag_query("company_standards", f"compliance regulations {domain} {prompt}",       top_k=4) or []
    pattern_docs    = await rag_query("design_patterns",   prompt,                                            top_k=3) or []
    past_designs    = await rag_query("past_designs",      f"{domain} {prompt}",                              top_k=2) or []

    # Keep RAG context compact — generation prompts are already large (effects lib, design tokens, layout templates)
    # Use first sentence / key rules only: 120 chars per doc, 2 docs per category max → ~1200 chars total
    domain_text     = "\n".join([d[:120] for d in domain_docs[:2]])     or "(apply industry best practices)"
    company_text    = "\n".join([d[:120] for d in company_docs[:2]])    or "(apply WCAG 2.1 AA)"
    compliance_text = "\n".join([d[:120] for d in compliance_docs[:2]]) or "(apply WCAG 2.1 AA, 4.5:1 contrast, 44px touch targets)"
    pattern_text    = "\n".join([d[:100] for d in pattern_docs[:2]])    or "(no saved patterns)"
    past_text       = "\n".join([d[:100] for d in past_designs[:1]])    or "(no past designs)"

    rag_context = f"""DOMAIN KNOWLEDGE ({domain.upper()}):
{domain_text}

COMPANY STANDARDS:
{company_text}

COMPLIANCE REQUIREMENTS:
{compliance_text}

APPROVED PATTERNS:
{pattern_text}

PAST SIMILAR DESIGNS:
{past_text}"""

    rag_summary = {
        "domain_docs": len(domain_docs), "company_docs": len(company_docs),
        "compliance_docs": len(compliance_docs), "patterns": len(pattern_docs), "past_designs": len(past_designs),
    }
    if progress_callback:
        await progress_callback({
            "type": "step_complete", "step": "rag",
            "message": f"✓ {sum(rag_summary.values())} knowledge chunks ({len(compliance_docs)} compliance)",
            "data": rag_summary,
        })

    # Step 3: Plan screens
    if progress_callback:
        await progress_callback({"type": "step_start", "step": "planning", "message": f"🗺️ Planning {screen_count}-screen flow..."})

    image_block = ""
    if image_analysis:
        image_block = f"\nREFERENCE IMAGE ANALYSIS:\n{json.dumps(image_analysis, indent=2)[:1200]}\n"

    plan_prompt = f"""You are a senior UX architect planning a {screen_count}-screen user flow.

USER REQUEST: {prompt}
DOMAIN: {domain}
{image_block}
{rag_context}

Plan a coherent, purposeful {screen_count}-screen flow where each screen advances the user's goal.

Return ONLY valid JSON:
{{
  "flow_name": "Specific descriptive name (e.g. '401k Loan Application Flow')",
  "flow_purpose": "One sentence on what users accomplish",
  "user_goal": "The user's underlying goal",
  "screens": [
    {{
      "screen_number": 1,
      "screen_id": "screen-1",
      "name": "Descriptive screen name (not just 'Screen 1')",
      "purpose": "What this screen does in the flow",
      "entry_action": "How user arrives",
      "primary_action": "Main user action on this screen",
      "exit_action": "What happens next",
      "content_elements": ["Specific element 1 with actual content", "Specific element 2"],
      "layout_type": "dashboard | detail | form | list | confirmation | centered | sidebar"
    }}
  ],
  "design_decisions": ["Specific design rationale"],
  "accessibility_notes": ["WCAG 2.1 AA considerations"]
}}

Generate exactly {screen_count} screens. Each screen must be distinct and necessary. Use domain-specific names."""

    plan_model = select_model(min(10, screen_count + 3), "ux")
    raw_plan = await llm_chat(
        "You are a UX architect. Return ONLY valid JSON. No markdown, no explanation.",
        plan_prompt,
        plan_model,
    )
    plan = _parse_json(raw_plan) or _fallback_plan(prompt, screen_count, image_analysis)

    if progress_callback:
        await progress_callback({
            "type": "step_complete", "step": "planning",
            "message": f"✓ Flow planned: {plan.get('flow_name', 'Flow')} ({len(plan.get('screens', []))} screens)",
        })

    # Step 4: Generate each screen
    generated_screens = []
    planned_screens = plan.get("screens", [])[:screen_count]

    for idx, screen_plan in enumerate(planned_screens):
        if progress_callback:
            await progress_callback({
                "type": "screen_start",
                "screen_number": idx + 1,
                "screen_name": screen_plan.get("name", f"Screen {idx+1}"),
                "message": f"🎨 Generating screen {idx+1}/{len(planned_screens)}: {screen_plan.get('name', '')}",
            })

        screen_html = await _generate_single_screen(
            screen_plan=screen_plan,
            fidelity=fidelity,
            design_system=ds,
            ds_prompt_block=ds_prompt_block,
            rag_context=rag_context,
            user_prompt=prompt,
            flow_context={**plan, "domain": domain},
            image_analysis=image_analysis,
            llm_chat=llm_chat,
            select_model=select_model,
        )

        generated_screen = {
            **screen_plan,
            "html": screen_html.get("html", ""),
            "design_notes": screen_html.get("design_notes", ""),
            "components_used": screen_html.get("components_used", []),
            "model_used": screen_html.get("model_used", ""),
        }
        generated_screens.append(generated_screen)

        if progress_callback:
            await progress_callback({
                "type": "screen_complete",
                "screen_number": idx + 1,
                "screen": generated_screen,
                "message": f"✓ Screen {idx+1} ready",
            })

    return {
        "flow_name": plan.get("flow_name", "Generated Flow"),
        "flow_purpose": plan.get("flow_purpose", ""),
        "user_goal": plan.get("user_goal", ""),
        "fidelity": fidelity,
        "design_system": {"id": design_system_id, "name": ds["name"], "tokens": ds["tokens"]},
        "domain": domain,
        "screens": generated_screens,
        "design_decisions": plan.get("design_decisions", []),
        "accessibility_notes": plan.get("accessibility_notes", []),
        "image_analysis": image_analysis,
        "rag_used": rag_summary,
    }


# ─────────────────────────────────────────────────────────────────────────────
# SINGLE SCREEN GENERATOR — the core generation function
# ─────────────────────────────────────────────────────────────────────────────

async def _generate_single_screen(
    screen_plan, fidelity, design_system, ds_prompt_block,
    rag_context, user_prompt, flow_context, image_analysis,
    llm_chat, select_model,
) -> dict:
    import json as _json

    tokens  = design_system.get("tokens", {})
    colors  = tokens.get("colors", {})
    typo    = tokens.get("typography", {})
    radius  = tokens.get("radius", {})
    shadows = tokens.get("shadows", {})

    design_system_id = design_system.get("design_system_id", "")
    is_core = design_system_id == "core-2"

    primary  = colors.get("primary",        "#5B5EF4")
    bg       = colors.get("background",     "#F8F9FC")
    surface  = colors.get("surface",        "#FFFFFF")
    text1    = colors.get("text_primary",   "#0F172A")
    text2    = colors.get("text_secondary", "#64748B")
    border   = colors.get("border",         "#E2E8F0")
    success  = colors.get("success",        "#22C55E")
    error    = colors.get("error",          "#EF4444")
    warning  = colors.get("warning",        "#F59E0B")
    font_fam = typo.get("font_family",      "Inter, sans-serif")
    success_light = colors.get("success_light", "#DCFCE7")
    warning_light = colors.get("warning_light", "#FEF3C7")
    error_light   = colors.get("error_light",   "#FEE2E2")
    primary_light = colors.get("primary_light", "#EFF6FF")

    # Derive a slightly darker primary for gradients (non-core design systems only)
    primary_dark = _darken_hex(primary, 0.15)

    domain       = flow_context.get("domain", "general")
    layout_type  = screen_plan.get("layout_type", "detail")
    screen_name  = screen_plan.get("name", "Screen")
    purpose      = screen_plan.get("purpose", "")
    elements     = screen_plan.get("content_elements", [])
    primary_action = screen_plan.get("primary_action", "Continue")

    domain_comps    = _get_domain_components(domain)
    layout_template = _get_layout_template(layout_type, design_system_id)

    # ── WIREFRAME ──────────────────────────────────────────────────────────────
    if fidelity == "wireframe":
        model = select_model(5, "ux")
        prompt = f"""Create a precise low-fidelity wireframe for this screen.

SCREEN: {screen_name}
PURPOSE: {purpose}
LAYOUT: {layout_type}
ELEMENTS TO SHOW: {', '.join(elements) if elements else 'relevant elements for this screen type'}

{layout_template}

WIREFRAME RULES:
- ONLY Tailwind grayscale classes — NO color
- Text placeholder: <div class="h-3 bg-gray-200 rounded mb-2" style="width:72%"></div>
- Image placeholder: <div class="bg-gray-100 rounded-xl flex items-center justify-center text-gray-400 text-xs font-medium py-8">Image</div>
- Button: <div class="bg-gray-800 text-white rounded-xl px-4 py-3 text-sm font-medium text-center">Button Label</div>
- Card: <div class="bg-white rounded-2xl border border-gray-200 p-5">
- Show ALL required elements from the spec — every button, field, and section must be visible
- Label elements clearly (real text for button labels, field labels, section headings)

Output ONLY raw HTML starting with <div. No markdown. No JSON."""
        raw = await llm_chat(WIREFRAME_SYSTEM, prompt, model)
        html = _extract_html(raw)
        if not html or len(html) < 100:
            html = _fallback_html(screen_plan, design_system, "wireframe")
        return {"html": html, "design_notes": f"{screen_name} wireframe", "components_used": [], "model_used": model}

    # ── HIFI ───────────────────────────────────────────────────────────────────
    model = select_model(9, "ui")

    # ── Determine screen type and canvas dimensions ────────────────────────────
    _type_to_w = {
        "mobile": 390, "tablet": 768,
        "web_dashboard": 1440, "website": 1440, "desktop_app": 1280,
    }
    screen_type  = screen_plan.get("screen_type", "")
    canvas_size  = screen_plan.get("canvas_size", {})
    # Derive canvas_w: prefer explicit canvas_size, then infer from screen_type, fallback 1440
    canvas_w = canvas_size.get("width") or _type_to_w.get(screen_type, 1440)

    # Only infer screen_type when it's genuinely missing
    mobile_layouts = {"centered", "form", "onboarding", "confirmation", "detail", "list"}
    if not screen_type:
        if canvas_w >= 1000 or layout_type in {"dashboard", "sidebar", "landing"} or any(
            w in user_prompt.lower() for w in ("website", "web app", "dashboard", "portal", "admin", "landing page", "desktop")
        ):
            screen_type = "web_dashboard" if "dashboard" in layout_type else "website"
            canvas_w = 1440
        elif layout_type in mobile_layouts or any(
            w in user_prompt.lower() for w in ("mobile", "ios", "android", "phone")
        ):
            screen_type = "mobile"
            canvas_w = 390
        else:
            # Default to web_dashboard when screen type is truly ambiguous
            screen_type = "web_dashboard"
            canvas_w = 1440

    is_mobile  = screen_type in ("mobile",)
    is_tablet  = screen_type == "tablet"
    is_desktop = screen_type in ("web_dashboard", "website", "desktop_app")

    if is_mobile:
        outer_wrap  = f'<div class="w-full flex flex-col" style="min-height:100vh;background:{bg};font-family:{font_fam};-webkit-font-smoothing:antialiased;">'
        layout_hint = "MOBILE (390px wide): full-width elements, 16px side padding (px-4), single column, touch targets min 44px, bottom safe area pb-8"
    elif is_tablet:
        outer_wrap  = f'<div class="w-full flex flex-col" style="min-height:100vh;background:{bg};font-family:{font_fam};-webkit-font-smoothing:antialiased;">'
        layout_hint = "TABLET (768px wide): max-w-2xl mx-auto px-6, can use 2-column grid, comfortable spacing"
    else:  # desktop / web dashboard / website
        outer_wrap  = f'<div class="w-full min-h-screen" style="background:{bg};font-family:{font_fam};-webkit-font-smoothing:antialiased;">'
        if is_core:
            # Exact-pixel shell from the mined layout template — never the generic
            # 240px-sidebar guess used by other design systems.
            layout_hint = (
                f"CORE 2.0 SHELL — see the locked PAGE LAYOUT TEMPLATE below for exact shell "
                f"dimensions (sidebar/navbar widths, content region). Do not use a 240px sidebar "
                f"or invent your own shell — reuse the mined template's numbers exactly."
            )
        elif layout_type == "sidebar" or "sidebar" in layout_type or screen_type == "web_dashboard":
            layout_hint = (
                "WEB DASHBOARD (1440px wide): use a fixed sidebar (240px wide) + main content area. "
                "Sidebar: left-fixed, full height, nav links. Main: flex-1, scrollable, px-8 py-6. "
                "Grid metrics 3-4 columns. Tables full width. Typography: heading 24px, body 14px."
            )
        else:
            layout_hint = (
                "WEBSITE (1440px wide): max-w-7xl mx-auto px-8, use hero section, feature grids, "
                "full-width sections with alternating bg. Large typography: hero 56-72px, section headers 36px."
            )

    # Fill in the effects toolkit with actual color values — core-2 gets the flat,
    # gradient-free toolkit; every other design system keeps the existing modern effects.
    if is_core:
        focus_default = shadows.get("focus_default", "0 0 0 2px #96B6EA")
        shadow_sm = shadows.get("sm", "0 2px 5px rgba(184,184,184,0.5)")
        shadow_md = shadows.get("md", "0 5px 18px -2px rgba(196,196,196,0.45)")
        shadow_lg = shadows.get("lg", "0 8px 29px 1px rgba(217,217,217,0.4)")
        effects = CORE_FLAT_EFFECTS.replace("{primary}", primary).replace("{surface}", surface) \
            .replace("{text1}", text1).replace("{text2}", text2).replace("{border}", border) \
            .replace("{success_light}", success_light).replace("{success}", success) \
            .replace("{warning_light}", warning_light).replace("{warning}", warning) \
            .replace("{error_light}", error_light).replace("{error}", error) \
            .replace("{primary_light}", primary_light) \
            .replace("{shadow_sm}", shadow_sm).replace("{shadow_md}", shadow_md) \
            .replace("{shadow_lg}", shadow_lg).replace("{focus_default}", focus_default) \
            .replace("{surface_subtle}", colors.get("surface_subtle", "#F5F5F5"))
    else:
        effects = MODERN_EFFECTS.replace("{primary}", primary).replace("{primary_dark}", primary_dark) \
            .replace("{bg}", bg).replace("{surface}", surface) \
            .replace("{text1}", text1).replace("{text2}", text2) \
            .replace("{border}", border).replace("{success}", success) \
            .replace("{error}", error).replace("{warning}", warning)

    image_note = ""
    if image_analysis:
        image_note = f"\nREFERENCE (match this closely):\n{_json.dumps(image_analysis, indent=2)[:500]}\n"

    # ── CORE 2.0: flat, exact-shell construction rules — skip the generic
    # gradient-hero/decorative-orb rules entirely for this design system.
    if is_core:
        logo_snippet = design_system.get("logo_snippet", "")
        screen_construction_rules = f"""Reuse the exact shell from the PAGE LAYOUT TEMPLATE above (sidebar/navbar widths,
content region offsets) — do not resize or reposition it.

BRAND MARK (mandatory — place in the shell header/navbar, do not invent a different logo):
{logo_snippet}

FLAT CARD (content grouping):
<div style="background:{surface};border:1px solid {border};border-radius:8px;padding:24px;box-shadow:{shadows.get('sm','0 2px 5px rgba(184,184,184,0.5)')};">

PAGE HEADER (within the content region, NOT a new shell):
<div style="display:flex;align-items:center;justify-content:space-between;padding:16px 24px;border-bottom:1px solid {border};">
  <h1 style="font-size:24px;font-weight:700;color:{text1};margin:0;">Page Title</h1>
  <button style="background:{primary};color:#FFFFFF;border-radius:8px;padding:10px 20px;font-weight:600;border:none;">Primary Action</button>
</div>

DATA TABLE ROW (flat, dense — use the real table variants from COMPONENT VARIANTS above: Small
40px or Regular 48px row height, Filter/Sort/Search header toggles, Checkbox column states):
<div style="display:flex;align-items:center;padding:14px 16px;border-bottom:1px solid {border};gap:16px;">
  <div style="flex:1;font-size:14px;color:{text2};">Row Label</div>
  <span style="font-size:12px;font-weight:600;padding:3px 10px;border-radius:16px;background:{success_light};color:{success};">Active</span>
</div>

FORM FIELD (label above input, no floating labels):
<div style="margin-bottom:16px;">
  <label style="display:block;font-size:14px;font-weight:500;color:{text1};margin-bottom:8px;">Field Label</label>
  <input style="width:100%;border:1.5px solid {border};border-radius:4px;padding:10px 14px;font-size:14px;color:{text1};background:{surface};" />
</div>

DENSITY REQUIREMENT — this is an enterprise admin surface, not a marketing page. Build AT LEAST
3 distinct content sections in the content region (e.g. a stat/metric row + a primary data
table or list + a secondary panel — mirroring how the real product's Dashboard and Payroll
screens are composed), and use 8-12 realistic data rows in any table/list, not 2-3. A single
sparse table with no header stats or side panel is NOT acceptable output.

NEVER use gradients, decorative circles/blobs, backdrop-filter, or colored box-shadow glows anywhere in this screen."""

        quality_checklist = f"""☑ Shell matches the PAGE LAYOUT TEMPLATE exactly (sidebar/navbar width, content offset) — not resized or repositioned
☑ The BRAND MARK markup appears verbatim in the shell header — not a different logo or wordmark
☑ At least 3 distinct content sections present (stat row + table/list + secondary panel, or equivalent) — not a single sparse block
☑ Tables/lists use 8-12 realistic rows, not 2-3
☑ Table/badge/accordion markup matches the COMPONENT VARIANTS spec (real sizes/states), not a generic approximation
☑ Zero gradients anywhere (no linear-gradient, radial-gradient, conic-gradient)
☑ Zero decorative blobs/orbs/blur shapes
☑ Zero backdrop-filter / glassmorphism
☑ Box-shadows are neutral grey/black only (Shadow1/2/3) — never a colored glow
☑ Primary color ({primary}) appears only on primary buttons, active/selected states, links, focus rings
☑ Typography uses Open Sans; body 14px, page title 24px
☑ All text is realistic retirement/401k/enterprise domain content — no lorem ipsum, no "Label" placeholders
☑ Tables/forms are dense and functional, not spaced out for marketing effect"""

    elif is_desktop:
        screen_construction_rules = f"""TOP NAVIGATION BAR (desktop — logo left, nav links center, user menu right):
<div style="display:flex;align-items:center;justify-content:space-between;padding:0 32px;height:60px;background:{surface};border-bottom:1px solid {border};position:sticky;top:0;z-index:10;">
  <div style="display:flex;align-items:center;gap:8px;">
    <div style="width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,{primary} 0%,{primary_dark} 100%);"></div>
    <span style="font-size:16px;font-weight:700;color:{text1};">AppName</span>
  </div>
  <nav style="display:flex;align-items:center;gap:4px;">
    <a style="padding:8px 16px;border-radius:8px;font-size:14px;font-weight:500;color:{text2};text-decoration:none;">Overview</a>
    <a style="padding:8px 16px;border-radius:8px;background:{primary}12;font-size:14px;font-weight:600;color:{primary};text-decoration:none;">Active Section</a>
    <a style="padding:8px 16px;border-radius:8px;font-size:14px;font-weight:500;color:{text2};text-decoration:none;">Settings</a>
  </nav>
  <div style="display:flex;align-items:center;gap:12px;">
    <button style="padding:8px 20px;border-radius:8px;background:linear-gradient(135deg,{primary} 0%,{primary_dark} 100%);color:white;font-size:14px;font-weight:600;border:none;">Action</button>
    <div style="width:36px;height:36px;border-radius:50%;background:{primary}20;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:{primary};">U</div>
  </div>
</div>

DESKTOP SIDEBAR + MAIN LAYOUT:
<div style="display:flex;min-height:calc(100vh - 60px);">
  <!-- Sidebar (240px) -->
  <aside style="width:240px;flex-shrink:0;background:{surface};border-right:1px solid {border};padding:20px 12px;">
    <div style="margin-bottom:24px;padding:0 8px;">
      <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{text2};margin-bottom:8px;">MAIN MENU</div>
    </div>
    <!-- Nav item (active) -->
    <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:10px;background:{primary}12;margin-bottom:2px;">
      <div style="width:18px;height:18px;border-radius:5px;background:{primary};"></div>
      <span style="font-size:14px;font-weight:600;color:{primary};">Dashboard</span>
    </div>
    <!-- Nav item (inactive) -->
    <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:10px;margin-bottom:2px;">
      <div style="width:18px;height:18px;border-radius:5px;background:{border};"></div>
      <span style="font-size:14px;font-weight:500;color:{text2};">Transactions</span>
    </div>
  </aside>
  <!-- Main content area -->
  <main style="flex:1;padding:32px;overflow-y:auto;">
    <!-- Page header -->
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:28px;">
      <div>
        <h1 style="font-size:24px;font-weight:700;color:{text1};margin:0 0 4px;">Page Title</h1>
        <p style="font-size:14px;color:{text2};margin:0;">Supporting description</p>
      </div>
      <button style="padding:10px 24px;border-radius:10px;background:linear-gradient(135deg,{primary} 0%,{primary_dark} 100%);color:white;font-size:14px;font-weight:600;border:none;box-shadow:0 4px 12px {primary}40;">Primary Action</button>
    </div>
    <!-- Metric tiles (3-4 column grid) -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;">
      <!-- repeat this tile 4x -->
      <div style="border-radius:16px;padding:20px;background:{surface};box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:{text2};margin-bottom:8px;">METRIC LABEL</div>
        <div style="font-size:32px;font-weight:800;color:{text1};line-height:1;margin-bottom:6px;">$0.00</div>
        <div style="font-size:12px;color:{success};font-weight:600;">↑ 4.2% vs last month</div>
      </div>
    </div>
    <!-- Content card -->
    <div style="border-radius:16px;background:{surface};box-shadow:0 2px 12px rgba(0,0,0,0.06);overflow:hidden;margin-bottom:20px;">
      <div style="padding:20px 24px;border-bottom:1px solid {border};display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:16px;font-weight:600;color:{text1};">Section Header</span>
        <button style="font-size:13px;font-weight:600;color:{primary};background:none;border:none;cursor:pointer;">View All →</button>
      </div>
      <div style="padding:0;"><!-- table rows go here --></div>
    </div>
  </main>
</div>

DATA ROW (inside a desktop content card or table):
<div style="display:flex;align-items:center;padding:16px 24px;border-bottom:1px solid {border};gap:16px;">
  <div style="flex:1;">
    <div style="font-size:14px;font-weight:500;color:{text1};">Row Label</div>
    <div style="font-size:13px;color:{text2};margin-top:2px;">Sub-label</div>
  </div>
  <span style="font-size:15px;font-weight:700;color:{text1};">Value</span>
  <span style="font-size:12px;font-weight:600;padding:4px 10px;border-radius:8px;background:{success}15;color:{success};">Active</span>
</div>

FORM FIELD (desktop):
<div style="margin-bottom:20px;">
  <div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{text2};margin-bottom:8px;">FIELD LABEL</div>
  <div style="border:1.5px solid {border};border-radius:10px;padding:12px 16px;background:{surface};font-size:15px;color:{text2};">Placeholder text</div>
</div>

STATUS BADGE patterns:
  Success: <span style="font-size:12px;font-weight:700;padding:4px 12px;border-radius:8px;background:{success}15;color:{success};">✓ Active</span>
  Warning: <span style="font-size:12px;font-weight:700;padding:4px 12px;border-radius:8px;background:{warning}15;color:{warning};">⚠ Pending</span>
  Primary: <span style="font-size:12px;font-weight:700;padding:4px 12px;border-radius:8px;background:{primary}15;color:{primary};">In Progress</span>"""

        quality_checklist = f"""☑ Screen uses a DESKTOP top nav bar (logo + nav links + user avatar) — NO mobile back button
☑ Layout uses sidebar (240px) + main content area — NOT single-column mobile stack
☑ Metric tiles use 3-4 column grid — NOT 2-column mobile grid
☑ Typography: page heading 24px, body 14-15px, labels 12-13px
☑ CTA buttons are inline/header-level — NOT full-width bottom buttons
☑ Spacing uses 24px-32px padding — NOT 16px mobile padding
☑ At least one metric displays in large bold text (28px+)
☑ Primary color appears 4-5 times (active nav, buttons, badges, key numbers)
☑ All text is realistic domain-specific content (real numbers, dates, names)
☑ Status badges use colored backgrounds with rounded corners
☑ Cards have box-shadow, not just borders"""
    else:
        # Mobile / tablet construction rules
        screen_construction_rules = f"""NAVIGATION BAR (mobile — back button + centered title):
<div style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:{surface};border-bottom:1px solid {border};position:sticky;top:0;z-index:10;">
  <button style="width:36px;height:36px;border-radius:10px;background:{bg};border:1px solid {border};display:flex;align-items:center;justify-content:center;color:{text2};font-size:18px;">←</button>
  <span style="font-size:16px;font-weight:600;color:{text1};">{screen_name}</span>
  <div style="width:36px;"></div>
</div>

HERO SUMMARY CARD (for financial summary screens — use gradient + decorative orbs):
<div style="margin:16px;border-radius:24px;padding:24px;background:linear-gradient(135deg,{primary} 0%,{primary_dark} 100%);color:white;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;border-radius:50%;background:rgba(255,255,255,0.08);"></div>
  <div style="position:absolute;bottom:-30px;left:10px;width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,0.06);"></div>
  <div style="position:relative;">
    <div style="font-size:12px;font-weight:600;opacity:0.8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Balance Label</div>
    <div style="font-size:36px;font-weight:800;line-height:1;margin-bottom:4px;">$12,450.00</div>
    <div style="font-size:13px;opacity:0.75;">Supporting detail text</div>
  </div>
</div>

CONTENT CARD (for grouped information):
<div style="margin:0 16px 12px;border-radius:20px;background:{surface};box-shadow:0 2px 12px rgba(0,0,0,0.06);overflow:hidden;">
  <div style="padding:16px;border-bottom:1px solid {border};display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:14px;font-weight:600;color:{text1};">Section Header</span>
    <span style="font-size:12px;font-weight:600;color:{primary};">View All</span>
  </div>
</div>

DATA ROW (inside a content card):
<div style="padding:14px 16px;border-bottom:1px solid {border};display:flex;justify-content:space-between;align-items:center;">
  <div>
    <div style="font-size:14px;font-weight:500;color:{text1};">Row Label</div>
    <div style="font-size:12px;color:{text2};margin-top:2px;">Sub-label</div>
  </div>
  <span style="font-size:15px;font-weight:700;color:{text1};">Value</span>
</div>

PRIMARY CTA BUTTON (at bottom of screen):
<div style="padding:16px;padding-bottom:32px;">
  <button style="width:100%;padding:16px;border-radius:20px;background:linear-gradient(135deg,{primary} 0%,{primary_dark} 100%);color:white;font-size:16px;font-weight:700;letter-spacing:0.01em;border:none;box-shadow:0 4px 16px {primary}40;">Primary Action</button>
</div>

METRIC TILES (for stat grids — 2 per row on mobile):
<div style="margin:0 16px 12px;display:grid;grid-template-columns:1fr 1fr;gap:10px;">
  <div style="border-radius:20px;padding:18px;background:{surface};box-shadow:0 2px 10px rgba(0,0,0,0.06);">
    <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:{text2};margin-bottom:6px;">LABEL</div>
    <div style="font-size:28px;font-weight:800;color:{text1};line-height:1;">$0.00</div>
    <div style="font-size:11px;color:{success};margin-top:6px;font-weight:600;">↑ 4.2%</div>
  </div>
</div>

FORM FIELD:
<div style="margin-bottom:16px;">
  <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{text2};margin-bottom:8px;">FIELD LABEL</div>
  <div style="border:1.5px solid {border};border-radius:14px;padding:14px 16px;background:{surface};font-size:15px;color:{text2};">Placeholder text</div>
</div>

STATUS BADGE patterns:
  Success: <span style="font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;background:{success}18;color:{success};">✓ On Track</span>
  Warning: <span style="font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;background:{warning}18;color:{warning};">⚠ Due Soon</span>
  Primary: <span style="font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;background:{primary}18;color:{primary};">Active</span>"""

        quality_checklist = """☑ Screen has a navigation bar (back button + centered title)
☑ Hero/summary area uses gradient (not flat white)
☑ At least one metric displays in large bold text (24px+)
☑ Cards have box-shadow, not just borders
☑ Primary color appears at least 4-5 times (buttons, badges, active states, numbers)
☑ All text is realistic domain-specific content (real numbers, dates, names)
☑ Bottom primary CTA button has gradient + shadow
☑ Decorative orbs or accent elements add depth
☑ Status badges use colored backgrounds
☑ Typography hierarchy: 3+ distinct font-size/weight levels"""
    # ────────────────────────────────────────────────────────────────────────

    _opening = (
        "Build a COMPLETE, production-quality hi-fidelity UI screen. This must be "
        "INDISTINGUISHABLE from this company's own existing product screens — reuse "
        "their exact shell and flat visual language, do not invent a new look."
        if is_core else
        "Build a COMPLETE, production-quality hi-fidelity UI screen. This must look "
        "like it was designed by a senior product designer at Stripe, Linear, or Coinbase."
    )
    prompt = f"""{_opening}

════════════ WHAT TO BUILD ════════════
SCREEN: {screen_name}
PURPOSE: {purpose}
USER'S PRIMARY ACTION: {primary_action}
MUST INCLUDE THESE ELEMENTS: {', '.join(elements) if elements else 'appropriate elements for this screen'}
LAYOUT: {layout_type} · {layout_hint}
USER REQUEST: {user_prompt[:200]}
{image_note}

════════════ DESIGN SYSTEM ════════════
{ds_prompt_block}

PRIMARY COLOR = {primary}  (use for: primary buttons/CTAs, active states, key numbers, progress fills, gradient starts)
DARK VARIANT  = {primary_dark}  (use as gradient end color)
BACKGROUND    = {bg}
SURFACE       = {surface}  (cards, panels)
TEXT PRIMARY  = {text1}
TEXT MUTED    = {text2}
BORDER        = {border}
SUCCESS       = {success}   ERROR = {error}   WARNING = {warning}

════════════ LAYOUT BLUEPRINT ════════════
{layout_template}

════════════ MODERN DESIGN EFFECTS ════════════
{effects}

════════════ DOMAIN PATTERNS ════════════
{domain_comps if domain_comps else "Use appropriate financial/enterprise component patterns."}

════════════ SCREEN CONSTRUCTION RULES ════════════

OUTER WRAPPER (start with EXACTLY this):
{outer_wrap}

{screen_construction_rules}

════════════ QUALITY CHECKLIST ════════════
Before finishing, ensure:
{quality_checklist}

════════════ OUTPUT ════════════
Output ONLY the complete raw HTML.
Start with: {outer_wrap}
End with: </div>
No markdown. No JSON. No HTML comments. No explanation."""

    raw = await llm_chat(CORE_HIFI_SYSTEM if is_core else HIFI_SYSTEM, prompt, model)
    html = _extract_html(raw)

    if html and len(html) > 300:
        return {
            "html": html,
            "design_notes": f"{screen_name} — HIFI, {design_system.get('name','DS')} ({model})",
            "components_used": elements,
            "model_used": model,
        }

    return {
        "html": _fallback_html(screen_plan, design_system, fidelity),
        "design_notes": f"Fallback — LLM output too short ({len(html) if html else 0} chars)",
        "components_used": [],
        "model_used": model,
    }


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _darken_hex(hex_color: str, amount: float = 0.15) -> str:
    """Darken a hex color by a given amount (0.0-1.0)."""
    try:
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, int(r * (1 - amount)))
        g = max(0, int(g * (1 - amount)))
        b = max(0, int(b * (1 - amount)))
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _extract_html(raw: str) -> str:
    """Extract clean HTML from a raw LLM response."""
    if not raw:
        return ""
    text = raw.strip()
    # Strip deepseek <think> blocks
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    # If it returned JSON with an html field, extract it
    if text.lstrip().startswith("{"):
        try:
            obj = json.loads(text)
            if isinstance(obj, dict) and obj.get("html"):
                return obj["html"]
        except Exception:
            m = re.search(r'"html"\s*:\s*"(.*?)(?:"\s*[,}])', text, re.DOTALL)
            if m:
                return m.group(1).replace("\\n", "\n").replace('\\"', '"')

    # Strip markdown fences
    if "```" in text:
        m = re.search(r"```(?:html)?\s*([\s\S]*?)```", text)
        if m:
            text = m.group(1).strip()

    # Find the outermost HTML element
    m = re.search(r"(<(?:div|section|main|article|html|!DOCTYPE)[\s\S]*)", text)
    if m:
        return m.group(1)

    if text.startswith("<"):
        return text
    return ""


def _build_vision_prompt(mode: str, user_prompt: str) -> str:
    if mode == "recreate":
        return f"""You are transcribing a UI screenshot for pixel-faithful recreation — this is NOT
a general description task. Every piece of visible text must be copied character-for-character,
never paraphrased, summarized, or replaced with a similar-sounding word. If you are not certain
of an exact word, transcribe your best literal reading rather than substituting a different word
that seems more common or more familiar.
USER WANTS: {user_prompt}

Return ONLY valid JSON, with exact_title_text and exact_labels filled in FIRST and treated as
mandatory — these two fields control what the recreated screen is named and must NEVER be
generic, invented, or a "similar" screen name from the same product family:
{{
  "exact_title_text": "The literal, verbatim text of the largest/primary heading on the screen — copy it exactly, do not paraphrase or generalize it (e.g. if it says 'Manage Year End Process', that is the value — never 'Plans' or any other related-sounding label)",
  "exact_labels": ["every other visible text label verbatim — column headers, button labels, filter/field labels, nav items, status badges — one string per label, in reading order"],
  "what_to_recreate": "Specific recreation instructions — MUST reference exact_title_text and MUST describe the actual layout/components seen, not a generic template",
  "screen_type": "dashboard | form | list | detail | landing | other",
  "layout_description": "Overall layout structure",
  "color_palette": ["#hex1", "#hex2", "#hex3"],
  "typography_style": "Description",
  "components_detected": [{{"type": "header | button | input | card | nav | table", "content": "text", "position": "top | center | etc"}}],
  "design_pattern": "Material | iOS | minimal | corporate"
}}"""
    if mode == "improve":
        return f"""Analyze this UI screenshot and suggest improvements.
USER REQUEST: {user_prompt}
Return ONLY valid JSON:
{{
  "current_state": {{"what_works": [], "issues_found": []}},
  "ux_improvements": [{{"issue": "problem", "fix": "solution", "impact": "high | medium | low"}}],
  "ui_improvements": [{{"issue": "visual problem", "fix": "visual fix", "impact": "high | medium | low"}}],
  "accessibility_issues": [],
  "redesign_direction": "Overall direction"
}}"""
    return f"Analyze this image as design inspiration. User wants: {user_prompt}. Return JSON with visual_style, color_inspiration, layout_principles, elements_to_borrow."


def _fallback_plan(prompt: str, screen_count: int, image_analysis) -> dict:
    base = [
        ("Overview", "Entry point and summary", "detail"),
        ("Details", "Core information view", "detail"),
        ("Action", "User performs main task", "form"),
        ("Confirmation", "Success state", "confirmation"),
        ("History", "Past transactions/records", "list"),
        ("Settings", "Configuration options", "form"),
    ]
    return {
        "flow_name": prompt[:60],
        "flow_purpose": prompt,
        "user_goal": "Complete the requested task",
        "screens": [
            {
                "screen_number": i + 1, "screen_id": f"screen-{i+1}",
                "name": base[i % len(base)][0], "purpose": base[i % len(base)][1],
                "entry_action": "Previous screen", "primary_action": "Continue",
                "exit_action": "Next screen", "content_elements": ["Header", "Content", "CTA"],
                "layout_type": base[i % len(base)][2],
            }
            for i in range(screen_count)
        ],
        "design_decisions": ["Fallback flow plan"],
        "accessibility_notes": ["Apply WCAG 2.1 AA"],
    }


def _fallback_html(screen_plan, design_system, fidelity) -> str:
    """Styled fallback screen using full design system tokens."""
    tokens   = design_system.get("tokens", {})
    colors   = tokens.get("colors", {})
    primary  = colors.get("primary",        "#5B5EF4")
    bg       = colors.get("background",     "#F8F9FC")
    surface  = colors.get("surface",        "#FFFFFF")
    text1    = colors.get("text_primary",   "#0F172A")
    text2    = colors.get("text_secondary", "#64748B")
    border   = colors.get("border",         "#E2E8F0")
    success  = colors.get("success",        "#22C55E")
    primary_dark = _darken_hex(primary, 0.15)

    name    = screen_plan.get("name", "Screen")
    purpose = screen_plan.get("purpose", "")
    elems   = screen_plan.get("content_elements", [])

    if fidelity == "wireframe":
        rows = "".join(f'<div style="height:12px;background:#E2E8F0;border-radius:6px;width:{65+i*8}%;margin-bottom:10px;"></div>' for i in range(4))
        return f"""<div style="min-height:100vh;background:white;font-family:Inter,sans-serif;">
  <div style="height:56px;background:white;border-bottom:1px solid #E2E8F0;display:flex;align-items:center;padding:0 16px;gap:12px;">
    <div style="width:24px;height:24px;border-radius:6px;background:#E2E8F0;"></div>
    <div style="height:14px;background:#E2E8F0;border-radius:6px;width:120px;"></div>
  </div>
  <div style="padding:16px;">
    <div style="border-radius:20px;background:#F1F5F9;padding:20px;margin-bottom:12px;">{rows}</div>
    <div style="border-radius:20px;background:white;border:1px solid #E2E8F0;padding:16px;margin-bottom:12px;">
      {"".join(f'<div style="display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid #F1F5F9;"><div style="height:12px;background:#E2E8F0;border-radius:6px;width:40%;"></div><div style="height:12px;background:#E2E8F0;border-radius:6px;width:25%;"></div></div>' for _ in range(4))}
    </div>
    <div style="border-radius:16px;background:#1E293B;padding:16px;text-align:center;"><div style="height:16px;background:rgba(255,255,255,0.3);border-radius:6px;width:60%;margin:0 auto;"></div></div>
  </div>
</div>"""

    elem_rows = "".join(
        f'<div style="padding:14px 16px;border-bottom:1px solid {border};display:flex;justify-content:space-between;align-items:center;"><div><div style="font-size:14px;font-weight:500;color:{text1};">{e}</div><div style="font-size:12px;color:{text2};margin-top:2px;">—</div></div><span style="font-size:14px;font-weight:600;color:{primary};">View →</span></div>'
        for e in (elems[:5] if elems else ["Loading data..."])
    )

    return f"""<div style="min-height:100vh;background:{bg};font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased;">
  <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:{surface};border-bottom:1px solid {border};position:sticky;top:0;z-index:10;">
    <div style="width:36px;height:36px;border-radius:10px;background:{bg};border:1px solid {border};display:flex;align-items:center;justify-content:center;color:{text2};font-size:18px;">←</div>
    <span style="font-size:16px;font-weight:600;color:{text1};">{name}</span>
    <div style="width:36px;"></div>
  </div>
  <div style="margin:16px;border-radius:24px;padding:24px;background:linear-gradient(135deg,{primary} 0%,{primary_dark} 100%);color:white;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;border-radius:50%;background:rgba(255,255,255,0.08);"></div>
    <div style="position:relative;">
      <div style="font-size:11px;font-weight:600;opacity:0.8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">{name.upper()}</div>
      <div style="font-size:13px;opacity:0.75;margin-bottom:12px;">{purpose[:80]}</div>
      <span style="font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;background:rgba(255,255,255,0.2);">Loading...</span>
    </div>
  </div>
  <div style="margin:0 16px 12px;border-radius:20px;background:{surface};box-shadow:0 2px 12px rgba(0,0,0,0.06);overflow:hidden;">
    <div style="padding:14px 16px;border-bottom:1px solid {border};display:flex;justify-content:space-between;align-items:center;">
      <span style="font-size:14px;font-weight:600;color:{text1};">Details</span>
    </div>
    {elem_rows}
  </div>
  <div style="padding:16px;padding-bottom:32px;">
    <button style="width:100%;padding:16px;border-radius:20px;background:linear-gradient(135deg,{primary} 0%,{primary_dark} 100%);color:white;font-size:16px;font-weight:700;border:none;box-shadow:0 4px 16px {primary}40;">Continue</button>
  </div>
</div>"""


def _parse_json(raw: str):
    """Strip think blocks + markdown, parse JSON."""
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
