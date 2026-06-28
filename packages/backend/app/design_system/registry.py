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
        "description": "CORE Enterprise Platform — clarity, efficiency, and scale for complex financial and HR workflows",
        "tokens": {
            "colors": {
                # Primary
                "primary": "#2563EB", "primary_hover": "#1D4ED8",
                "primary_light": "#EFF6FF", "primary_border": "#BFDBFE",
                # Backgrounds & surfaces
                "background": "#F5F6F8", "surface": "#FFFFFF",
                "surface_subtle": "#F3F4F6", "surface_muted": "#F9FAFB",
                # Text
                "text_primary": "#111827", "text_secondary": "#374151",
                "text_tertiary": "#6B7280", "text_placeholder": "#9CA3AF",
                # Borders & dividers
                "border": "#E5E7EB", "border_strong": "#D1D5DB", "border_soft": "#F3F4F6",
                # Semantic — Success
                "success": "#16A34A", "success_light": "#DCFCE7", "success_border": "#BBF7D0",
                # Semantic — Warning
                "warning": "#D97706", "warning_light": "#FEF3C7", "warning_border": "#FDE68A",
                # Semantic — Critical/Error
                "error": "#DC2626", "error_light": "#FEE2E2", "error_border": "#FECACA",
                # Semantic — Info
                "info": "#0284C7", "info_light": "#E0F2FE",
            },
            "typography": {
                "font_family": 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                "heading_size": 24,
                "body_size": 14,
            },
            "spacing": {
                "base": 4,
                "scale": [4, 8, 16, 24, 40, 64],
                "tokens": {"xs": 4, "s": 8, "m": 16, "l": 24, "xl": 40, "xxl": 64},
            },
            "radius": {
                "xs": 4, "sm": 4, "md": 8, "lg": 12, "xl": 16, "full": 9999,
                "control": 4,   # inputs, selects, checkboxes
                "card": 12,     # cards, containers, modals
                "button": 8,    # buttons, upload controls
            },
            "shadows": {
                "xs": "none",
                "sm": "0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)",
                "md": "0 4px 12px rgba(0,0,0,0.10), 0 2px 4px rgba(0,0,0,0.06)",
                "lg": "0 20px 40px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.08)",
            },
        },
        "component_style": (
            "Enterprise-grade, accessibility-first. Single strong primary blue on white. "
            "Semantic status colours (green/amber/red/blue) with consistent tinted backgrounds. "
            "4px spacing grid. Clean card elevation. Focus rings on every interactive element. "
            "WCAG 2.1 AA mandatory. Data tables, forms, modals, accordions, badges as primary vocabulary."
        ),
        "css_framework": "Tailwind CSS with CORE 2.0 enterprise tokens",
        "design_system_id": "core-2",
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

    # Append full DESIGN.md if available — gives agent deep visual context
    design_md_id = ds.get("design_system_id", ds_id)
    if include_full_design_md:
        md_content = get_design_md_content(design_md_id)
        if md_content:
            # Trim to first 3000 chars to avoid blowing prompt budget on very long files
            trimmed = md_content[:3000]
            if len(md_content) > 3000:
                trimmed += "\n\n[...design doc truncated for length — tokens above are canonical...]"
            prompt += f"\n\nDESIGN REFERENCE (from {design_md_id}/DESIGN.md):\n{trimmed}"

    return prompt
