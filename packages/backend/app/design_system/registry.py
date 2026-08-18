"""
Design System Registry — token sets and DESIGN.md loader for all design systems.
Python dicts cover the most-used systems for fast prompt injection.
get_design_md_content() loads the full DESIGN.md from knowledge/ for any system.
"""
import os
from pathlib import Path

# Path to the knowledge/design-systems directory — walk up from __file__ to find it
def _find_knowledge_dir() -> Path:
    this = Path(__file__).resolve()
    for parent in this.parents:
        candidate = parent / "knowledge" / "design-systems"
        if candidate.exists():
            return candidate
    # Docker fallback: knowledge mounted at /knowledge
    return Path("/knowledge/design-systems")

_KNOWLEDGE_DIR = _find_knowledge_dir()


DESIGN_SYSTEMS = {
    "core-2": {
        "name": "CORE 2.0 Design System",
        "description": "CORE Enterprise Platform — extracted from the company's real Figma component library and reference screens (retirement/401k domain). Tokens and layout grammar below are ground truth, not stylistic approximation.",
        "tokens": {
            "colors": {
                # Primary (Brand/background/*, Brand/Text/*, Brand/Borders/* in Figma)
                "primary": "#004DCB", "primary_hover": "#00368E", "primary_active": "#002F7C",
                "primary_light": "#E6EDFA", "primary_border": "#004DCB", "primary_disabled": "#96B6EA",
                # Backgrounds & surfaces (Neutral/Surfaces/*)
                "background": "#FFFFFF", "surface": "#FFFFFF",
                "surface_subtle": "#F5F5F5", "surface_muted": "#E6E6E6",
                # Text (Neutral/Text/*)
                "text_primary": "#292929", "text_secondary": "#3D3D3D",
                "text_tertiary": "#575757", "text_placeholder": "#A8A8A8",
                "text_on_color": "#FFFFFF",
                # Borders & dividers (Neutral/border/*)
                "border": "#E0E0E0", "border_strong": "#B8B8B8", "border_soft": "#D9D9D9",
                # Semantic — Success (Semantics/Success/*)
                "success": "#105F27", "success_light": "#E8F3EB", "success_strong": "#178737", "success_border": "#105F27",
                # Semantic — Warning (Semantics/Warning/*)
                "warning": "#A56811", "warning_light": "#FDF4E8", "warning_strong": "#A56811", "warning_border": "#A56811",
                # Semantic — Critical/Error (Semantics/Critical/*)
                "error": "#9C2227", "error_light": "#FCEAEB", "error_strong": "#C92830", "error_border": "#9C2227",
                # Semantic — Highlight/Info (Semantics/Highlights/*)
                "info": "#037EA0", "info_light": "#E6F2F6",
                # Disabled (Semantics/Disabled/*)
                "disabled_text": "#A8A8A8", "disabled_background": "#F5F5F5", "disabled_border": "#B8B8B8",
            },
            "typography": {
                "font_family": '"Open Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                "heading_size": 24,   # Titles/PageTitle
                "body_size": 14,      # BodyText/Small
                "scale": {
                    "h2": {"size": 32, "weight": 600, "line_height": 24, "letter_spacing": 1},
                    "page_title": {"size": 24, "weight": 700, "line_height": 32},
                    "heading": {"size": 22, "weight": 700, "line_height": 24, "letter_spacing": 1},
                    "h6": {"size": 18, "weight": 600, "line_height": 24, "letter_spacing": 1},
                    "body_large": {"size": 16, "weight": 500, "line_height": 16},
                    "body_regular": {"size": 14, "weight": 400, "line_height": 16},
                    "body_small": {"size": 14, "weight": 600, "line_height": 16},
                    "extra_small": {"size": 12, "weight": 500, "line_height": 16},
                },
            },
            "spacing": {
                "base": 4,
                "scale": [4, 8, 12, 16, 24, 32, 48],
                "tokens": {"xs": 4, "s": 8, "sm": 12, "m": 16, "l": 24, "xl": 32, "xxl": 48},
            },
            "radius": {
                "xs": 2, "sm": 4, "md": 8, "lg": 16, "full": 9999,
                "control": 4,   # inputs, selects, checkboxes
                "card": 8,      # cards, containers
                "button": 8,    # buttons
                "badge": 16,
            },
            "shadows": {
                # Reconciled against the formal "Shadows" style-guide page added to the
                # Figma file (Elevation-01/02/03 spec table: X/Y/Blur/Spread/Opacity/Color) —
                # this supersedes the earlier raw Shadow1/2/3 effect-token values, which
                # used a single flatter layer per level. The style-guide page is the
                # design team's authored source of truth.
                "xs": "none",
                "sm": "0 2px 4px -1px rgba(0,0,0,0.05)",      # Elevation-01
                "md": "0 5px 5px -3px rgba(0,0,0,0.06)",      # Elevation-02
                "lg": "0 8px 10px -5px rgba(0,0,0,0.08)",     # Elevation-03
                # Focus rings (Focus Shadow/Default|Error|Success)
                "focus_default": "0 0 0 2px #96B6EA",
                "focus_error": "0 0 0 2px #F2AAAD",
                "focus_success": "0 0 0 2px #A0CEAD",
            },
        },
        "component_style": (
            "Flat, restrained enterprise UI extracted directly from the company Figma library. "
            "NO gradients, NO decorative blobs/orbs, NO glassmorphism — every surface is a flat fill "
            "with a hairline border and at most a soft ambient drop-shadow (Shadow1/2/3). "
            "Open Sans typography. Single strong primary blue (#004DCB) used sparingly for CTAs, "
            "active/selected states, links, and focus rings. Semantic status colours (green/amber/"
            "red/teal) with tinted light backgrounds. 4px spacing grid. WCAG 2.1 AA. "
            "Retirement/401k plan administration domain: employee/plan/payroll tables, "
            "investment selection, contribution forms, wizard-style questionnaires."
        ),
        "css_framework": "Tailwind CSS with CORE 2.0 enterprise tokens",
        "design_system_id": "core-2",
        # ── LAYOUT GRAMMAR — mined from real screens in the company Figma file ──
        # Each entry is a locked structural skeleton (verified across 3-9 duplicate
        # screens each). Generation must REUSE these dimensions exactly and only
        # vary slot CONTENT, never the shell/section order/spacing.
        "layout_templates": {
            "shell_sidebar": {
                "source": "Payroll File Info (4 consistent samples)",
                "canvas": {"width": 1440, "height": 900},
                "structure": (
                    "Fixed left sidebar 'Side Menu bar - Light', width=100px, full height. "
                    "Top navbar 'Navbar - Top', height=66px, spans remaining width (1340px), "
                    "positioned at x=100,y=0. Content area below navbar: x=100, y=66, "
                    "width=1340, height=834 — this is the ONLY slot that varies per screen."
                ),
            },
            "shell_topnav": {
                "source": "Dashboard-enrolled (3 consistent samples)",
                "canvas": {"width": 1440, "height": 1024},
                "structure": (
                    "Full-width top 'Navbar', height=72px, x=0,y=0,width=1440. "
                    "Slim icon-rail 'Menubar', width=96px, below navbar (x=0,y=72,height=952). "
                    "Content area: x=96, y=72, width=1344, height=952 — the varying slot. "
                    "This is a DISTINCT shell from shell_sidebar — do not mix the two navbar heights "
                    "(66px vs 72px) or sidebar widths (100px vs 96px) on the same screen."
                ),
            },
            "split_wizard": {
                "source": "Questionnaire-1..6 (4+ consistent samples per step)",
                "canvas": {"width": 1440, "height": 1024},
                "structure": (
                    "Left rail fixed width=592px, full height (step indicator / illustration / "
                    "context). Right form panel width=848px, x=592. Inner content padded "
                    "x=84,y=72 relative to the panel, width=680, height~=649. Use for any "
                    "multi-step form / questionnaire / onboarding flow."
                ),
            },
            "panel_header_body_footer": {
                "source": "Choose Investment (9 samples) + Risk level acknowledgement (7 samples)",
                "canvas": {"width": 1100, "height": 1024},
                "structure": (
                    "This is an embedded panel/drawer, NOT a full page shell (no sidebar/navbar). "
                    "Header height=61px (title, left-aligned, ~24px padding). "
                    "Body height=890px (scrollable primary content). "
                    "Footer height=73px (right-aligned action buttons, ~24px right margin). "
                    "Use for modal-like selection/review/acknowledgement steps embedded within "
                    "a larger flow."
                ),
            },
            "auth_split": {
                "source": "Login with password (5 consistent samples)",
                "canvas": {"width": 1441, "height": 1019},
                "structure": (
                    "Two-column split, NO app shell (no sidebar/navbar — auth screens are shell-free). "
                    "Left decorative/illustration column width=638px. Right form column width=803px."
                ),
            },
            "shell_appbar": {
                "source": "Admin Dashborad (4 samples) + Employee details (1 sample, same shell)",
                "canvas": {"width": 1440, "height": 900},
                "structure": (
                    "Icon rail 'App Bar', width=96px, full height (x=0,y=0). Top 'Navbar - Top', "
                    "height=64px, spans x=98..1440. Content area: x=98,y=67, width=1342, "
                    "height=833 — the varying slot. DISTINCT from shell_topnav (72px navbar) and "
                    "shell_sidebar (100px sidebar/66px navbar) — this shell uses a 96px rail with "
                    "a 64px navbar. Use for admin/record-detail dashboards."
                ),
            },
            "shell_config_nested": {
                "source": "Plan -Sponsor, Plan - Basic Details, Confg - Plan details (3 consistent samples)",
                "canvas": {"width": 1440, "height": 900},
                "structure": (
                    "Same outer shell as shell_appbar (96px App Bar rail + 64px Navbar-Top), PLUS a "
                    "secondary in-page 'Plan details-sidemenu' panel, width=317px, full content "
                    "height (836px), positioned immediately after the rail/navbar. Remaining content "
                    "area: ~1025px wide. Use this for any settings/configuration/multi-section-form "
                    "screen (e.g. plan setup, admin configuration) — the secondary side menu is the "
                    "key structural signal, not a generic tab bar or accordion."
                ),
            },
        },
        # Map generic layout_type strings (used elsewhere in the pipeline) to the
        # closest mined template above, so existing callers keep working.
        "layout_type_map": {
            "dashboard": "shell_topnav",
            "sidebar": "shell_sidebar",
            "list": "shell_sidebar",
            "detail": "shell_appbar",
            "form": "split_wizard",
            "centered": "auth_split",
            "confirmation": "panel_header_body_footer",
            "settings": "shell_config_nested",
        },
        "layout_grammar_gaps": (
            "NOT YET VERIFIED (fewer than 2 consistent reference samples) — treat cautiously "
            "and prefer the closest template above rather than inventing new structure: "
            "full data-table/list page, multi-tab content page, empty/error states."
        ),
        # The real Logo component — exact vector paths and exact colors pulled directly from
        # Figma's Dev Mode MCP asset server (get_design_context succeeded on this specific
        # node and returned real asset URLs; each SVG path was downloaded and verified by
        # rendering). This is the pixel-accurate "CORE" wordmark with a red target/crosshair
        # ring replacing the "O" — navy #292670 letters/center, red #BA141A ring/ticks.
        # Also saved as a standalone asset at packages/frontend/public/brand/core-logo.svg.
        "logo_snippet": (
            '<svg width="108" height="40" viewBox="0 0 400 148" xmlns="http://www.w3.org/2000/svg">'
            '<g transform="translate(0,19)"><path fill="#292670" d="M103.666 23.583L92.8668 31.883L91.7807 30.4823C87.6658 25.1092 82.5901 20.8233 76.4909 17.8754C70.3081 14.9066 63.6658 13.5895 56.8146 13.5895C49.107 13.5895 41.859 15.4084 35.1332 19.2135C28.658 22.8722 23.436 27.8271 19.718 34.2664C15.9373 40.8312 14.2454 48.0023 14.2454 55.5706C14.2454 67.2157 18.1097 77.2092 26.4648 85.3838C35.0287 93.7466 45.5144 97.3426 57.4204 97.3426C71.3943 97.3426 82.7363 91.7813 91.8224 81.2024L92.9086 79.9271L103.708 88.1226L102.601 89.5443C97.3159 96.2763 90.7363 101.44 82.9661 105.036C74.7154 108.883 65.859 110.493 56.7937 110.493C39.7285 110.493 24.6266 105.162 13.3264 92.074C4.13577 81.3906 0 68.721 0 54.6507C0 39.4304 5.30548 26.3845 16.2089 15.7638C27.4047 4.87131 41.1488 0 56.6893 0C65.9217 0 74.9034 1.73527 83.1958 5.81212C91.0287 9.65899 97.5666 15.1157 102.663 22.1822L103.666 23.583Z"/></g>'
            '<g transform="translate(102.68,-2.63) scale(0.819,0.834)">'
            '<path fill="#BA141A" transform="translate(10,10)" d="M20.9561 83C22.4556 113.264 46.717 137.554 76.998 139.068V160C35.1745 158.458 1.54165 124.825 0.000976562 83H20.9561ZM160 83C158.459 124.825 124.825 158.458 83.002 160V139.068C113.283 137.554 137.544 113.264 139.044 83H160ZM83.002 0.000976562C124.825 1.54342 158.458 35.1763 160 77H139.041C137.516 46.7394 113.244 22.4965 83.002 20.9834V0.000976562ZM76.998 20.9834C46.7339 22.4952 22.4831 46.7385 20.959 77H0C1.5183 35.1755 35.1509 1.54139 76.998 0V20.9834Z"/>'
            '<path fill="#292670" transform="translate(50,50)" d="M79.7793 43C78.3238 62.7659 62.5995 78.536 42.8896 80V43H79.7793ZM36.8896 43V79.999C17.1806 78.5334 1.45691 62.7461 0 43H36.8896ZM42.8896 0C62.5991 1.46396 78.3222 17.2347 79.7783 37H42.8896V0ZM36.8896 37H0C1.45757 17.2544 17.181 1.46657 36.8896 0.000976562V37Z"/>'
            '<rect fill="#BA141A" x="87" y="0" width="6" height="10"/>'
            '<rect fill="#BA141A" x="87" y="170" width="6" height="10"/>'
            '<rect fill="#BA141A" x="170" y="87" width="10" height="6"/>'
            '<rect fill="#BA141A" x="0" y="87" width="10" height="6"/>'
            '</g>'
            '<g transform="translate(255.96,21.5)"><path fill="#292670" d="M13.7441 13.5268V44.5944L29.5143 44.7199C33.859 44.7617 39.812 44.5317 43.906 42.901C46.7467 41.772 49.0235 39.974 50.6945 37.4025C52.3655 34.7891 53.1593 31.9458 53.1593 28.8515C53.1593 25.82 52.3655 23.0603 50.6945 20.5306C49.0861 18.0845 46.9556 16.3074 44.2402 15.2202C40.3968 13.694 34.0261 13.5477 29.9321 13.5477H13.7441V13.5268ZM33.859 58.0167L70.496 105.371H53.4308L16.8355 58.1003H13.7232V105.371H0V0H22.0365C26.7989 0 31.6031 0.0627209 36.3446 0.355418C39.2898 0.522673 42.5065 0.773557 45.389 1.44258C51.6553 2.88515 56.9608 5.97938 61.0966 10.9552C65.3785 16.0983 67.1749 22.245 67.1749 28.8933C67.1749 34.4337 65.9216 39.7231 62.9973 44.4481C60.1148 49.1103 56.0209 52.4554 51.0287 54.6716C45.9321 56.9295 39.6867 57.7867 33.859 58.0167Z"/></g>'
            '<g transform="translate(338.16,21.5)"><path fill="#292670" d="M13.7233 13.5268V41.8765H61.4517V55.4033H13.7233V91.865H61.4517V105.371H0V0H61.8486V13.5268H13.7233Z"/></g>'
            '</svg>'
        ),
        "logo_note": (
            "EXACT — real logo vector paths and exact colors (#292670 navy, #BA141A red) "
            "pulled directly from Figma's Dev Mode MCP asset server and verified by rendering. "
            "Use this exact markup verbatim in the shell header — do not invent a different "
            "logotype or color for it."
        ),
        # Precise component variants mined from the real Figma component library —
        # for higher-fidelity reproduction instead of generic Tailwind approximations.
        "component_variants": {
            "table": (
                "Two size variants: Small (40px row height) and Regular (48px row height). "
                "Header cells support independent Filter / Sort / Search / More-Option toggles "
                "and a Checkbox column (states: Default, Unselected, Selected, Group). "
                "Reuse these exact toggle combinations rather than inventing new header controls."
            ),
            "badge": (
                "5 semantic variants only: Success (#E8F3EB bg/#105F27 text), "
                "Warning (#FDF4E8 bg/#A56811 text), Critical (#FCEAEB bg/#9C2227 text), "
                "Highlight (#E6F2F6 bg/#037EA0 text), Neutral (#F5F5F5 bg/#3D3D3D text). "
                "Never invent a 6th color or use raw Tailwind color classes for badges."
            ),
            "accordion": (
                "Header (16px padding, 14px 600-weight text) + collapsible panel "
                "(16px padding, #F5F5F5 background). Supports a 'summary' variant where the "
                "collapsed header shows a right-aligned muted summary value (e.g. a running total)."
            ),
        },
    },
    "company": {
        "name": "Company Design System",
        "description": "Your organization's custom design system",
        "tokens": {
            "colors": {
                "primary": "#5B5EF4", "primary_hover": "#4A4DD6",
                "background": "#FFFFFF", "surface": "#F7F7F7",
                "surface_subtle": "#F0F0F0",
                "text_primary": "#171717", "text_secondary": "#525252",
                "text_tertiary": "#8A8A8A",
                "border": "#E5E5EA", "border_strong": "#D1D1D6", "border_soft": "#F0F0F4",
                "error": "#FF3B30", "error_light": "#FF3B3012",
                "success": "#34C759", "success_light": "#34C75912",
                "warning": "#FF9500", "warning_light": "#FF950012",
                "info": "#0A84FF", "info_light": "#0A84FF12",
            },
            "typography": {"font_family": "Inter, -apple-system, sans-serif", "heading_size": 28, "body_size": 14},
            "spacing": {"base": 4, "scale": [4,8,12,16,20,24,32,40,48,64,80,96]},
            "radius": {"xs": 4, "sm": 6, "md": 10, "lg": 16, "xl": 20, "full": 9999, "control": 8, "card": 12},
            "shadows": {"xs": "0 1px 2px rgba(0,0,0,0.06)", "sm": "0 1px 3px rgba(0,0,0,0.08)", "md": "0 4px 12px rgba(0,0,0,0.08)", "lg": "0 8px 24px rgba(0,0,0,0.10)"},
        },
        "component_style": "Clean and professional with subtle depth. Blue-purple brand on white.",
        "css_framework": "Tailwind CSS",
    },
    "linear": {
        "name": "Linear App",
        "description": "Ultra-minimal, dark-native, precision engineering aesthetic",
        "tokens": {
            "colors": {
                "primary": "#5E6AD2", "primary_accent": "#7170FF",
                "background": "#08090A", "surface": "#0F1011",
                "surface_raised": "#191A1B", "surface_hover": "#28282C",
                "text_primary": "#F7F8F8", "text_secondary": "#D0D6E0",
                "text_tertiary": "#8A8F98", "text_muted": "#62666D",
                "border": "rgba(255,255,255,0.05)", "border_standard": "rgba(255,255,255,0.08)",
                "border_solid": "#23252A",
                "error": "#F03E3E", "success": "#27A644",
            },
            "typography": {"font_family": "Inter Variable, -apple-system, sans-serif", "heading_size": 24, "body_size": 13, "font_features": "\"cv01\", \"ss03\""},
            "spacing": {"base": 4, "scale": [2,4,6,8,10,12,16,20,24,32]},
            "radius": {"sm": 4, "md": 6, "lg": 8, "xl": 10, "full": 9999, "control": 6, "card": 8},
            "shadows": {"sm": "0 1px 2px rgba(0,0,0,0.4)", "md": "0 2px 8px rgba(0,0,0,0.5)", "lg": "0 4px 12px rgba(0,0,0,0.6)"},
        },
        "component_style": "Ultra-clean, dense, keyboard-first. Dark canvas with semi-transparent borders. No decorative elements.",
        "css_framework": "Tailwind CSS with compact dark-mode tokens",
        "design_system_id": "linear-app",
    },
    "stripe": {
        "name": "Stripe Design",
        "description": "Trusted, enterprise-grade financial design with blue-tinted shadows",
        "tokens": {
            "colors": {
                "primary": "#533AFD", "primary_hover": "#4B35E0",
                "background": "#FFFFFF", "surface": "#F6F9FC",
                "text_primary": "#061B31", "text_secondary": "#425466",
                "text_tertiary": "#697386",
                "border": "#E6EBF1", "border_strong": "#CBD5E0",
                "error": "#EA2261", "success": "#00D924",
            },
            "typography": {"font_family": "sohne-var, -apple-system, sans-serif", "heading_size": 28, "body_size": 15},
            "spacing": {"base": 8, "scale": [4,8,12,16,20,24,32,40,48,64]},
            "radius": {"sm": 4, "md": 6, "lg": 8, "xl": 12, "full": 9999, "control": 6, "card": 8},
            "shadows": {"sm": "0 2px 5px rgba(50,50,93,0.1),0 1px 1px rgba(0,0,0,0.07)", "md": "0 4px 6px rgba(50,50,93,0.11),0 1px 3px rgba(0,0,0,0.08)", "lg": "0 7px 14px rgba(50,50,93,0.1),0 3px 6px rgba(0,0,0,0.08)"},
        },
        "component_style": "Polished, trustworthy, financial precision. Blue-tinted shadow system. Clean cards.",
        "css_framework": "Tailwind CSS with Stripe tokens",
        "design_system_id": "stripe",
    },
    "notion": {
        "name": "Notion",
        "description": "Warm neutral canvas with analog warmth, ultra-thin borders",
        "tokens": {
            "colors": {
                "primary": "#0075DE",
                "background": "#FFFFFF", "surface": "#F6F5F4",
                "text_primary": "rgba(0,0,0,0.95)", "text_secondary": "#615D59",
                "text_tertiary": "#A39E98",
                "border": "rgba(0,0,0,0.1)", "border_strong": "rgba(0,0,0,0.18)",
                "error": "#E03E3E", "success": "#0F7B6C",
            },
            "typography": {"font_family": "NotionInter, Inter, -apple-system, sans-serif", "heading_size": 32, "body_size": 16, "letter_spacing_display": "-2.125px"},
            "spacing": {"base": 8, "scale": [4,8,12,16,24,32,48,64]},
            "radius": {"sm": 3, "md": 6, "lg": 8, "xl": 12, "full": 9999, "control": 4, "card": 6},
            "shadows": {"sm": "rgba(15,15,15,0.05) 0 0 0 1px,rgba(15,15,15,0.1) 0 3px 6px,rgba(15,15,15,0.2) 0 9px 24px", "md": "rgba(15,15,15,0.08) 0 0 0 1px,rgba(15,15,15,0.12) 0 8px 20px", "lg": "rgba(15,15,15,0.1) 0 0 0 1px,rgba(15,15,15,0.15) 0 16px 40px"},
        },
        "component_style": "Minimal, warm, document-first. Whisper-weight borders. Analog paper feel.",
        "css_framework": "Tailwind CSS with Notion warm-neutral tokens",
        "design_system_id": "notion",
    },
    "vercel": {
        "name": "Vercel / Geist",
        "description": "Developer infrastructure aesthetic — gallery-like emptiness, Geist type",
        "tokens": {
            "colors": {
                "primary": "#171717", "primary_accent": "#0070F3",
                "background": "#FFFFFF", "surface": "#FAFAFA",
                "surface_secondary": "#F5F5F5",
                "text_primary": "#171717", "text_secondary": "#888888",
                "text_tertiary": "#AAAAAA",
                "border": "rgba(0,0,0,0.08)", "border_strong": "rgba(0,0,0,0.15)",
                "error": "#FF5B4F", "success": "#0070F3",
            },
            "typography": {"font_family": "Geist, -apple-system, sans-serif", "font_mono": "Geist Mono, monospace", "heading_size": 40, "body_size": 15, "letter_spacing_display": "-2.4px"},
            "spacing": {"base": 8, "scale": [4,8,16,24,32,40,48,64,96]},
            "radius": {"sm": 4, "md": 6, "lg": 8, "xl": 12, "full": 9999, "control": 6, "card": 8},
            "shadows": {"sm": "0 0 0 1px rgba(0,0,0,0.08)", "md": "0 0 0 1px rgba(0,0,0,0.08),0 2px 8px rgba(0,0,0,0.06)", "lg": "0 0 0 1px rgba(0,0,0,0.08),0 8px 32px rgba(0,0,0,0.1)"},
        },
        "component_style": "Engineering minimalism. Shadow-as-border technique. Gallery white. No ornament.",
        "css_framework": "Tailwind CSS with Geist tokens",
        "design_system_id": "vercel",
    },
    "github": {
        "name": "GitHub / Primer",
        "description": "Dense, information-first developer tool design. Primer design system.",
        "tokens": {
            "colors": {
                "primary": "#0969DA",
                "background": "#FFFFFF", "surface": "#F6F8FA",
                "surface_overlay": "#FFFFFF",
                "text_primary": "#1F2328", "text_secondary": "#636C76",
                "text_tertiary": "#9198A1",
                "border": "#D0D7DE", "border_strong": "#AFB8C1",
                "error": "#CF222E", "success": "#1A7F37", "warning": "#9A6700",
            },
            "typography": {"font_family": "system-ui,-apple-system,sans-serif", "font_mono": "SFMono,Menlo,Consolas,monospace", "heading_size": 20, "body_size": 14},
            "spacing": {"base": 4, "scale": [4,8,12,16,20,24,32,40,48,64]},
            "radius": {"sm": 3, "md": 6, "lg": 8, "xl": 12, "full": 9999, "control": 6, "card": 6},
            "shadows": {"sm": "0 1px 0 rgba(31,35,40,0.04)", "md": "0 1px 3px rgba(31,35,40,0.12),0 8px 24px rgba(66,74,83,0.12)", "lg": "0 8px 24px rgba(66,74,83,0.12),0 40px 64px rgba(66,74,83,0.12)"},
        },
        "component_style": "Dense, information-first. Hairline borders. System fonts. Power-user focus.",
        "css_framework": "Tailwind CSS with Primer tokens",
        "design_system_id": "github",
    },
    "shadcn": {
        "name": "shadcn/ui",
        "description": "Beautifully designed accessible components built on Radix UI primitives",
        "tokens": {
            "colors": {
                "primary": "#18181B", "primary_hover": "#09090B",
                "background": "#FFFFFF", "surface": "#FAFAFA",
                "text_primary": "#09090B", "text_secondary": "#71717A",
                "text_tertiary": "#A1A1AA",
                "border": "#E4E4E7", "border_strong": "#D4D4D8",
                "error": "#EF4444", "success": "#22C55E",
                "accent": "#F4F4F5", "ring": "#18181B",
            },
            "typography": {"font_family": "Inter, sans-serif", "heading_size": 30, "body_size": 14},
            "spacing": {"base": 4, "scale": [2,4,6,8,12,16,24,32,48]},
            "radius": {"sm": 4, "md": 6, "lg": 8, "xl": 12, "full": 9999, "control": 6, "card": 8},
            "shadows": {"sm": "0 1px 2px rgba(0,0,0,0.05)", "md": "0 1px 3px rgba(0,0,0,0.1),0 1px 2px rgba(0,0,0,0.06)", "lg": "0 4px 6px rgba(0,0,0,0.07),0 2px 4px rgba(0,0,0,0.06)"},
        },
        "component_style": "Minimal, accessible, highly composable. Radix UI primitives. Clean neutrals.",
        "css_framework": "Tailwind CSS with CSS variables",
    },
    "material": {
        "name": "Material Design 3",
        "description": "Google's Material You design system — expressive, rounded, dynamic color",
        "tokens": {
            "colors": {
                "primary": "#6750A4", "secondary": "#625B71",
                "background": "#FFFBFE", "surface": "#FEF7FF",
                "text_primary": "#1C1B1F", "text_secondary": "#49454F",
                "border": "#CAC4D0",
                "error": "#B3261E", "tertiary": "#7D5260",
            },
            "typography": {"font_family": "Google Sans, Roboto, sans-serif", "heading_size": 32, "body_size": 16},
            "spacing": {"base": 8, "scale": [4,8,12,16,24,32,48,64]},
            "radius": {"sm": 4, "md": 12, "lg": 16, "xl": 28, "full": 9999, "control": 12, "card": 16},
            "shadows": {"sm": "0 1px 2px rgba(0,0,0,0.1)", "md": "0 4px 8px rgba(0,0,0,0.1)", "lg": "0 8px 16px rgba(0,0,0,0.12)"},
        },
        "component_style": "Rounded, expressive, Material You dynamic color. Motion-rich interactions.",
        "css_framework": "Tailwind CSS with Material-inspired tokens",
    },
    "apple": {
        "name": "Apple HIG",
        "description": "Apple Human Interface Guidelines — iOS/macOS native aesthetic",
        "tokens": {
            "colors": {
                "primary": "#007AFF", "secondary": "#34C759",
                "background": "#FFFFFF", "surface": "#F2F2F7",
                "surface_secondary": "#FFFFFF",
                "text_primary": "#000000", "text_secondary": "#3C3C43",
                "text_tertiary": "#3C3C4399",
                "border": "#C6C6C8", "separator": "#C6C6C8",
                "error": "#FF3B30", "success": "#34C759", "warning": "#FF9500",
                "fill": "rgba(120,120,128,0.2)",
            },
            "typography": {"font_family": "SF Pro Display, -apple-system, Helvetica Neue, sans-serif", "heading_size": 34, "body_size": 17},
            "spacing": {"base": 8, "scale": [4,8,12,16,20,24,32,44,64]},
            "radius": {"sm": 6, "md": 10, "lg": 14, "xl": 20, "full": 9999, "control": 10, "card": 14},
            "shadows": {"sm": "0 1px 3px rgba(0,0,0,0.1)", "md": "0 4px 16px rgba(0,0,0,0.12)", "lg": "0 8px 30px rgba(0,0,0,0.15)"},
        },
        "component_style": "SF symbols, vibrancy, blur, native iOS feel. Large touch targets. System color palette.",
        "css_framework": "Tailwind CSS with Apple-inspired tokens",
    },
    "ant": {
        "name": "Ant Design",
        "description": "Alibaba's enterprise-grade design system for complex data applications",
        "tokens": {
            "colors": {
                "primary": "#1677FF", "secondary": "#52C41A",
                "background": "#FFFFFF", "surface": "#FAFAFA",
                "text_primary": "#000000D9", "text_secondary": "#00000073",
                "border": "#D9D9D9",
                "error": "#FF4D4F", "warning": "#FAAD14",
            },
            "typography": {"font_family": "-apple-system, BlinkMacSystemFont, Segoe UI, PingFang SC, sans-serif", "heading_size": 24, "body_size": 14},
            "spacing": {"base": 8, "scale": [4,8,12,16,20,24,32,40,48,64]},
            "radius": {"sm": 2, "md": 4, "lg": 6, "xl": 8, "full": 9999, "control": 4, "card": 6},
            "shadows": {"sm": "0 1px 2px rgba(0,0,0,0.03),0 1px 6px rgba(0,0,0,0.02)", "md": "0 3px 6px rgba(0,0,0,0.04),0 1px 4px rgba(0,0,0,0.04)", "lg": "0 6px 16px rgba(0,0,0,0.08)"},
        },
        "component_style": "Enterprise-grade, information-dense. Complex forms, data tables, dashboards.",
        "css_framework": "Tailwind CSS with Ant Design tokens",
    },
    "framer": {
        "name": "Framer",
        "description": "Motion-rich, dark-optional, modern product design from Framer",
        "tokens": {
            "colors": {
                "primary": "#0055FF", "primary_hover": "#0044CC",
                "background": "#FFFFFF", "surface": "#F5F5F5",
                "text_primary": "#111111", "text_secondary": "#666666",
                "border": "#E5E5E5",
                "error": "#FF3366", "success": "#00CC66",
            },
            "typography": {"font_family": "Inter, -apple-system, sans-serif", "heading_size": 36, "body_size": 15},
            "spacing": {"base": 8, "scale": [4,8,12,16,24,32,48,64,80]},
            "radius": {"sm": 6, "md": 10, "lg": 16, "xl": 24, "full": 9999, "control": 8, "card": 16},
            "shadows": {"sm": "0 2px 8px rgba(0,0,0,0.08)", "md": "0 8px 24px rgba(0,0,0,0.1)", "lg": "0 24px 64px rgba(0,0,0,0.15)"},
        },
        "component_style": "Motion-first, modern, bold typography. Generous radius. Smooth interactions.",
        "css_framework": "Tailwind CSS with Framer tokens",
        "design_system_id": "framer",
    },
    "resend": {
        "name": "Resend",
        "description": "Dark-first, developer-focused email API. Clean monochrome palette.",
        "tokens": {
            "colors": {
                "primary": "#FFFFFF",
                "background": "#000000", "surface": "#111111",
                "surface_raised": "#1A1A1A",
                "text_primary": "#FFFFFF", "text_secondary": "#888888",
                "text_tertiary": "#555555",
                "border": "#222222", "border_strong": "#333333",
                "error": "#FF4444", "success": "#22C55E",
            },
            "typography": {"font_family": "Inter, -apple-system, sans-serif", "heading_size": 40, "body_size": 15},
            "spacing": {"base": 8, "scale": [4,8,12,16,24,32,48,64]},
            "radius": {"sm": 4, "md": 6, "lg": 8, "xl": 12, "full": 9999, "control": 6, "card": 8},
            "shadows": {"sm": "0 0 0 1px rgba(255,255,255,0.06)", "md": "0 4px 24px rgba(0,0,0,0.8)", "lg": "0 16px 64px rgba(0,0,0,0.9)"},
        },
        "component_style": "Pitch-black canvas, minimal chrome. Developer clarity. White text on dark.",
        "css_framework": "Tailwind CSS with dark-mode tokens",
        "design_system_id": "resend",
    },
    "raycast": {
        "name": "Raycast",
        "description": "macOS-native feel, dark-default, power-user productivity aesthetic",
        "tokens": {
            "colors": {
                "primary": "#FF6363", "primary_hover": "#FF4D4D",
                "background": "#1C1C1E", "surface": "#2C2C2E",
                "surface_raised": "#3A3A3C",
                "text_primary": "#FFFFFF", "text_secondary": "#EBEBF5CC",
                "text_tertiary": "#EBEBF599",
                "border": "rgba(255,255,255,0.1)", "border_strong": "rgba(255,255,255,0.18)",
                "error": "#FF453A", "success": "#30D158",
            },
            "typography": {"font_family": "-apple-system, Helvetica Neue, sans-serif", "heading_size": 20, "body_size": 14},
            "spacing": {"base": 4, "scale": [4,8,12,16,20,24,32,48]},
            "radius": {"sm": 6, "md": 10, "lg": 14, "xl": 20, "full": 9999, "control": 8, "card": 12},
            "shadows": {"sm": "0 1px 4px rgba(0,0,0,0.6)", "md": "0 4px 16px rgba(0,0,0,0.7)", "lg": "0 16px 48px rgba(0,0,0,0.8)"},
        },
        "component_style": "macOS native, dark, keyboard-driven. Red accent on dark surfaces. Blur effects.",
        "css_framework": "Tailwind CSS with macOS dark tokens",
        "design_system_id": "raycast",
    },
}


# ─── DESIGN.md loader ────────────────────────────────────────────────────────

def list_available_design_systems() -> list[str]:
    """Return IDs of all design systems that have a DESIGN.md in knowledge/."""
    if not _KNOWLEDGE_DIR.exists():
        return []
    return sorted([
        d.name for d in _KNOWLEDGE_DIR.iterdir()
        if d.is_dir() and (d / "DESIGN.md").exists()
    ])


def get_design_md_content(ds_id: str) -> str | None:
    """Load the full DESIGN.md for a design system from knowledge/design-systems/.
    Returns the Markdown content string, or None if not found.
    """
    path = _KNOWLEDGE_DIR / ds_id / "DESIGN.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


def get_design_system(ds_id: str) -> dict:
    """Get design system token dict. Falls back to 'company' if not found."""
    return DESIGN_SYSTEMS.get(ds_id, DESIGN_SYSTEMS["company"])


def get_system_prompt_injection(ds_id: str, include_full_design_md: bool = True) -> str:
    """Build design system context string for agent prompts.

    If include_full_design_md is True and a DESIGN.md exists in knowledge/,
    the full document is appended after the token block for richer agent context.
    """
    ds = get_design_system(ds_id)
    tokens = ds["tokens"]
    colors = tokens.get("colors", {})
    typo   = tokens.get("typography", {})
    radius = tokens.get("radius", {})
    spacing = tokens.get("spacing", {})

    p   = colors.get("primary",        "#5B5EF4")
    bg  = colors.get("background",     "#FFFFFF")
    sfc = colors.get("surface",        "#F7F7F7")
    t1  = colors.get("text_primary",   "#171717")
    t2  = colors.get("text_secondary", "#525252")
    t3  = colors.get("text_tertiary",  "#8A8A8A")
    bdr = colors.get("border",         "#E5E5EA")
    bdr_strong = colors.get("border_strong", "#D1D1D6")
    err = colors.get("error",          "#FF3B30")
    suc = colors.get("success",        "#34C759")
    wrn = colors.get("warning",        "#FF9500")
    inf = colors.get("info",           "#0A84FF")

    r_ctrl = radius.get("control", 8)
    r_card = radius.get("card",    12)
    r_lg   = radius.get("lg",      16)

    prompt = f"""DESIGN SYSTEM: {ds["name"]}
Style: {ds["component_style"]} | Framework: {ds["css_framework"]}

TOKEN VALUES (use these EXACT hex codes — do NOT substitute or invent new values):
  Primary:          {p}
  Background:       {bg}
  Surface:          {sfc}
  Text primary:     {t1}
  Text secondary:   {t2}
  Text tertiary:    {t3}
  Border:           {bdr}
  Border strong:    {bdr_strong}
  Error:            {err}
  Success:          {suc}
  Warning:          {wrn}
  Info:             {inf}

Typography: {typo.get("font_family", "Inter, sans-serif")}
  Heading: {typo.get("heading_size", 24)}px font-bold | Body: {typo.get("body_size", 14)}px font-normal
  Weights: 400 body · 500 label · 600 subheading · 700 heading · 800 display
  Line height: 1.5 body · 1.2 headings

Spacing base: {spacing.get("base", 4)}px grid — multiples: {spacing.get("scale", [4,8,12,16,24,32,48,64])}
Border radius: control={r_ctrl}px · card={r_card}px · panel={r_lg}px · full=9999px

COMPONENT SPECS (use inline style="" with exact values — Tailwind cannot resolve arbitrary hex):
  Card:             background:{sfc}; border:1px solid {bdr}; border-radius:{r_card}px; padding:20px 24px; box-shadow:0 1px 3px rgba(0,0,0,0.08)
  Primary button:   background:{p}; color:white; border-radius:{r_ctrl}px; padding:10px 20px; font-weight:600; font-size:14px
  Secondary button: border:1px solid {bdr}; color:{t1}; border-radius:{r_ctrl}px; padding:9px 20px; font-weight:500
  Ghost button:     background:transparent; color:{t2}; border:none; border-radius:{r_ctrl}px; padding:8px 14px; font-weight:500
  Input:            border:1px solid {bdr}; border-radius:{r_ctrl}px; padding:10px 14px; font-size:14px; color:{t1}; background:{bg}
  Nav bar:          background:{sfc}; border-bottom:1px solid {bdr}; height:56px; padding:0 16px
  Section heading:  color:{t1}; font-size:15px; font-weight:600; letter-spacing:-0.01em
  Muted label:      color:{t3}; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.06em
  Success badge:    background:{suc}18; color:{suc}; border-radius:999px; padding:3px 10px; font-size:11px; font-weight:600
  Error badge:      background:{err}18; color:{err}; border-radius:999px; padding:3px 10px; font-size:11px; font-weight:600
  Warning badge:    background:{wrn}18; color:{wrn}; border-radius:999px; padding:3px 10px; font-size:11px; font-weight:600
  Divider:          border-top:1px solid {bdr}

CRITICAL: Use style="" with EXACT hex above — Tailwind only for layout (flex, grid, gap, padding, margin, w-full, overflow-*)."""

    # ── Layout grammar (mined page templates) — injected in full, NEVER truncated.
    # This is what makes generated screens reuse the real shell/composition instead
    # of inventing new layout; it must reach the model even when the DESIGN.md tail
    # below gets cut for length.
    layout_templates = ds.get("layout_templates")
    if layout_templates:
        lt_lines = ["\nPAGE LAYOUT TEMPLATES (locked structural skeletons mined from real product "
                    "screens — REUSE the matching template's exact dimensions/composition; only the "
                    "named content slot may vary. Do NOT invent a new shell, change section order, "
                    "or resize the sidebar/navbar/rail):"]
        for key, tpl in layout_templates.items():
            canvas = tpl.get("canvas", {})
            lt_lines.append(
                f"\n[{key}] canvas {canvas.get('width')}x{canvas.get('height')} "
                f"(source: {tpl.get('source', 'n/a')})\n  {tpl.get('structure', '')}"
            )
        type_map = ds.get("layout_type_map")
        if type_map:
            lt_lines.append(f"\nGeneric layout_type → template mapping: {type_map}")
        gaps = ds.get("layout_grammar_gaps")
        if gaps:
            lt_lines.append(f"\nGAPS — {gaps}")
        prompt += "\n" + "\n".join(lt_lines)

    # ── Brand mark — injected verbatim so every screen carries the same logo,
    # never truncated away (same reasoning as the layout grammar above).
    logo_snippet = ds.get("logo_snippet")
    if logo_snippet:
        prompt += (
            f"\n\nBRAND MARK — {ds.get('logo_note', 'use this exact markup, do not invent a different logo')}:\n"
            f"{logo_snippet}"
        )

    # ── Precise component variants mined from the real component library — for
    # higher-fidelity reproduction instead of generic approximations.
    component_variants = ds.get("component_variants")
    if component_variants:
        cv_lines = ["\nCOMPONENT VARIANTS (reuse these exact variants — do not invent new ones):"]
        for name, spec in component_variants.items():
            cv_lines.append(f"\n[{name}] {spec}")
        prompt += "\n" + "\n".join(cv_lines)

    # Append full DESIGN.md if available — gives agent deep visual context
    design_md_id = ds.get("design_system_id", ds_id)
    if include_full_design_md:
        md_content = get_design_md_content(design_md_id)
        if md_content:
            # Trim to avoid blowing prompt budget on very long files. Raised from 3000
            # to 8000 — the old limit silently cut off newer sections (e.g. layout
            # grammar) appended near the end of a doc.
            trimmed = md_content[:8000]
            if len(md_content) > 8000:
                trimmed += "\n\n[...design doc truncated for length — tokens/layout templates above are canonical...]"
            prompt += f"\n\nDESIGN REFERENCE (from {design_md_id}/DESIGN.md):\n{trimmed}"

    return prompt
