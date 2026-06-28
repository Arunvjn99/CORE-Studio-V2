"""Design System Tokens — single source of truth for all generated designs."""
from typing import Any, Dict, Optional

DESIGN_TOKENS: Dict[str, Any] = {
    "colors": {
        # Brand
        "primary":           "#5B5EF4",
        "primary_hover":     "#4A4DD6",
        "primary_subtle":    "#5B5EF408",  # 3% tint — for selected state backgrounds
        "primary_light":     "#5B5EF415",  # 8% tint — for badges, tags

        # Semantic
        "success":           "#34C759",
        "success_light":     "#34C75912",
        "success_border":    "#34C75930",
        "warning":           "#FF9500",
        "warning_light":     "#FF950012",
        "warning_border":    "#FF950030",
        "danger":            "#FF3B30",
        "danger_light":      "#FF3B3012",
        "danger_border":     "#FF3B3030",
        "info":              "#0A84FF",
        "info_light":        "#0A84FF12",
        "info_border":       "#0A84FF30",

        # Surface hierarchy (5 levels — use in order, never skip)
        "background":        "#FFFFFF",    # page canvas
        "surface":           "#F7F7F7",    # inset sections, sidebar, card background
        "surface_subtle":    "#F0F0F0",    # hover fills, secondary panels
        "surface_muted":     "#E8E8E8",    # pressed states, divider fills
        "surface_raised":    "#FFFFFF",    # card on surface (border + shadow differentiates)
        "surface_overlay":   "#FFFFFF",    # modal, popover (shadow differentiates)

        # Text hierarchy (5 levels — use exactly these)
        "text_primary":      "#171717",    # headings, strong labels
        "text_secondary":    "#525252",    # body copy, descriptions
        "text_tertiary":     "#8A8A8A",    # captions, metadata, disabled labels
        "text_soft":         "#B0B0B0",    # very muted, de-emphasized labels
        "text_faint":        "#CCCCCC",    # placeholders, ghost states

        # Borders (3 levels)
        "border":            "#E5E5EA",    # standard border
        "border_strong":     "#D1D1D6",    # emphasized border (focus rings, active states)
        "border_soft":       "#F0F0F4",    # subtle section dividers

        # Inverse (text/elements on dark/primary backgrounds)
        "on_primary":        "#FFFFFF",
        "on_primary_muted":  "rgba(255,255,255,0.72)",

        # Interaction overlays
        "selection_overlay": "rgba(91,94,244,0.15)",
        "focus_ring":        "rgba(91,94,244,0.25)",
        "overlay_scrim":     "rgba(0,0,0,0.45)",
    },

    "typography": {
        "font_family":        "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        "font_mono":          "JetBrains Mono, Menlo, Monaco, 'Courier New', monospace",
        "font_import":        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",

        # Sizes — use these specific values, not arbitrary numbers
        # Large display — hero headings, stat callouts
        "display_2xl": {"size": 56, "weight": 800, "line_height": 1.05, "letter_spacing": "-0.04em"},
        "display_xl":  {"size": 48, "weight": 800, "line_height": 1.08, "letter_spacing": "-0.03em"},
        "display_lg":  {"size": 40, "weight": 700, "line_height": 1.1,  "letter_spacing": "-0.02em"},
        "display_md":  {"size": 32, "weight": 700, "line_height": 1.15, "letter_spacing": "-0.02em"},

        # Section headings
        "heading_lg":  {"size": 24, "weight": 700, "line_height": 1.3,  "letter_spacing": "-0.01em"},
        "heading_md":  {"size": 20, "weight": 600, "line_height": 1.35, "letter_spacing": "-0.01em"},
        "heading_sm":  {"size": 17, "weight": 600, "line_height": 1.4,  "letter_spacing": "0"},

        # Body copy
        "body_lg":     {"size": 18, "weight": 400, "line_height": 1.65, "letter_spacing": "0"},
        "body_md":     {"size": 16, "weight": 400, "line_height": 1.6,  "letter_spacing": "0"},
        "body_sm":     {"size": 14, "weight": 400, "line_height": 1.55, "letter_spacing": "0"},

        # UI labels (buttons, inputs, nav)
        "label_lg":    {"size": 16, "weight": 600, "line_height": 1.0,  "letter_spacing": "0"},
        "label_md":    {"size": 14, "weight": 500, "line_height": 1.0,  "letter_spacing": "0"},
        "label_sm":    {"size": 12, "weight": 500, "line_height": 1.0,  "letter_spacing": "0.01em"},

        # Captions, metadata
        "caption":     {"size": 11, "weight": 400, "line_height": 1.4,  "letter_spacing": "0.02em"},
        "overline":    {"size": 11, "weight": 600, "line_height": 1.0,  "letter_spacing": "0.08em", "transform": "uppercase"},

        # Exact UI sizes for agent HTML generation
        "ui_sizes": [9, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 15, 16, 17, 18, 20, 24],
    },

    "spacing": {
        # 4px base grid — all values are multiples of 4
        "1":   4,   # micro gaps (icon-to-label)
        "2":   8,   # tight internal padding
        "3":   12,  # compact elements
        "4":   16,  # standard internal padding
        "5":   20,  # comfortable padding
        "6":   24,  # section internal padding
        "8":   32,  # card padding, section gaps
        "10":  40,  # generous section padding
        "12":  48,  # major section separation
        "16":  64,  # hero sections, large breathing zones
        "20":  80,  # page-level vertical rhythm
        "24":  96,  # maximum section padding
    },

    "radius": {
        "none":   0,
        "xs":     4,    # tags, tiny badges
        "sm":     6,    # subtle (chips, small tags)
        "md":     10,   # buttons, inputs
        "lg":     16,   # cards, panels
        "xl":     20,   # large cards, sheets
        "2xl":    28,   # hero cards, prominent containers
        "control": 8,   # interactive controls standard
        "card":   12,   # card default
        "panel":  16,   # panel/modal default
        "full":   9999, # pills, avatars
    },

    "shadows": {
        # Minimal — shadows are for separation, not decoration
        "xs":  "0 1px 2px rgba(0,0,0,0.06)",
        "sm":  "0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)",
        "md":  "0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04)",
        "lg":  "0 8px 24px rgba(0,0,0,0.10), 0 4px 8px rgba(0,0,0,0.04)",
        "xl":  "0 16px 48px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.06)",
        "none": "none",
        # Brand shadow
        "brand": "0 4px 16px rgba(91,94,244,0.25)",
        "brand_sm": "0 2px 8px rgba(91,94,244,0.15)",
    },

    "motion": {
        # Duration
        "instant":  "80ms",
        "fast":     "120ms",
        "normal":   "200ms",
        "slow":     "300ms",
        "gentle":   "400ms",
        # Easing
        "ease_out":      "cubic-bezier(0.0, 0, 0.2, 1)",
        "ease_in":       "cubic-bezier(0.4, 0, 1, 1)",
        "ease_in_out":   "cubic-bezier(0.4, 0, 0.2, 1)",
        "spring":        "cubic-bezier(0.34, 1.56, 0.64, 1)",
        # Compound transitions
        "interaction":   "background 120ms ease, border-color 120ms ease, color 120ms ease, box-shadow 120ms ease",
        "transform":     "transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1)",
        "opacity":       "opacity 150ms ease",
    },

    "breakpoints": {
        "mobile":  390,   # iPhone 14 Pro
        "tablet":  768,   # iPad mini
        "desktop": 1024,  # laptop
        "wide":    1440,  # desktop monitor
    },

    # Layout composition guides — referenced by UI agent
    "layout_canvases": {
        "hero_centered": {
            "description": "Single focal point, centered, minimal surrounding content",
            "max_width": "480px for content block",
            "vertical_rhythm": "top-third placement for focal point",
            "use_for": "onboarding, landing, empty states, confirmation screens",
        },
        "app_shell": {
            "description": "Persistent nav + scrollable main content",
            "nav_height": "56px sticky top",
            "content_padding": "16-24px horizontal",
            "use_for": "main app screens, dashboards, settings",
        },
        "editorial": {
            "description": "Large type, intentional whitespace, image zones",
            "headline_size": "display_lg or display_xl",
            "use_for": "feature showcases, marketing screens, detail pages",
        },
        "form_wizard": {
            "description": "Single column, step indicator, one decision at a time",
            "content_width": "420px max",
            "use_for": "multi-step onboarding, configuration flows",
        },
        "data_dashboard": {
            "description": "Metric cards in grid, scannable headers, data tables",
            "grid": "2-col mobile, 3-4 col desktop",
            "use_for": "analytics, portfolio overview, activity feeds",
        },
        "split_screen": {
            "description": "Two columns, equal or 60/40 weight",
            "split": "60/40 default, 50/50 for comparisons",
            "use_for": "product detail + list, comparison, side-by-side content",
        },
        "feed_list": {
            "description": "Repeated row/card pattern, vertically scannable",
            "item_height": "56-80px for rows, auto for cards",
            "use_for": "activity feed, search results, file lists",
        },
        "modal_focus": {
            "description": "Overlay on context, minimal content, single decision",
            "max_width": "480px",
            "use_for": "confirmation dialogs, quick forms, alerts",
        },
    },

    # Component design rules — for agent HTML/CSS generation
    "component_rules": {
        "button": {
            "primary":   "background: var(--primary); color: white; border-radius: var(--radius-control); padding: 10px 20px; font-weight: 600; font-size: 14px; border: none; transition: var(--motion-interaction);",
            "secondary": "background: transparent; color: var(--text-primary); border: 1px solid var(--border); border-radius: var(--radius-control); padding: 9px 20px; font-weight: 500; font-size: 14px;",
            "ghost":     "background: transparent; color: var(--text-secondary); border: none; border-radius: var(--radius-control); padding: 8px 14px; font-weight: 500; font-size: 14px;",
            "danger":    "background: var(--danger); color: white; border-radius: var(--radius-control); padding: 10px 20px; font-weight: 600; font-size: 14px;",
        },
        "input": {
            "default": "background: var(--background); border: 1px solid var(--border); border-radius: var(--radius-control); padding: 10px 14px; font-size: 14px; color: var(--text-primary); transition: border-color 120ms ease, box-shadow 120ms ease;",
            "focus":   "border-color: var(--primary); box-shadow: 0 0 0 3px var(--focus-ring);",
            "error":   "border-color: var(--danger); box-shadow: 0 0 0 3px var(--danger-light);",
        },
        "card": {
            "default":  "background: var(--surface-raised); border: 1px solid var(--border); border-radius: var(--radius-card); padding: 20px 24px; box-shadow: var(--shadow-sm);",
            "elevated": "background: var(--surface-raised); border: none; border-radius: var(--radius-card); padding: 20px 24px; box-shadow: var(--shadow-lg);",
            "flat":     "background: var(--surface); border: 1px solid var(--border-soft); border-radius: var(--radius-card); padding: 20px 24px;",
        },
        "badge": {
            "default":  "background: var(--primary-light); color: var(--primary); border-radius: 999px; padding: 3px 10px; font-size: 11px; font-weight: 600;",
            "success":  "background: var(--success-light); color: var(--success); border-radius: 999px; padding: 3px 10px; font-size: 11px; font-weight: 600;",
            "danger":   "background: var(--danger-light); color: var(--danger); border-radius: 999px; padding: 3px 10px; font-size: 11px; font-weight: 600;",
            "warning":  "background: var(--warning-light); color: var(--warning); border-radius: 999px; padding: 3px 10px; font-size: 11px; font-weight: 600;",
            "info":     "background: var(--info-light); color: var(--info); border-radius: 999px; padding: 3px 10px; font-size: 11px; font-weight: 600;",
        },
    },
}


COMPONENTS: Dict[str, Any] = {
    "button": {
        "primary": {
            "background": "primary",
            "text_color": "white",
            "padding": {"top": 12, "bottom": 12, "left": 24, "right": 24},
            "border_radius": "md",
            "font_size": 16,
            "font_weight": 600,
            "states": {
                "default":  {"opacity": 1},
                "hover":    {"opacity": 0.9},
                "active":   {"opacity": 0.8},
                "disabled": {"opacity": 0.5},
            },
        },
        "secondary": {
            "background": "surface",
            "text_color": "primary",
            "border": "1px solid border",
            "padding": {"top": 12, "bottom": 12, "left": 24, "right": 24},
            "border_radius": "md",
            "font_size": 16,
            "font_weight": 600,
        },
        "ghost": {
            "background": "transparent",
            "text_color": "text_secondary",
            "border": "none",
            "padding": {"top": 8, "bottom": 8, "left": 14, "right": 14},
            "border_radius": "md",
            "font_size": 14,
            "font_weight": 500,
        },
        "tertiary": {
            "background": "transparent",
            "text_color": "primary",
            "padding": {"top": 8, "bottom": 8, "left": 16, "right": 16},
            "border_radius": "md",
            "font_size": 16,
            "text_decoration": "underline",
        },
        "danger": {
            "background": "danger",
            "text_color": "white",
            "padding": {"top": 12, "bottom": 12, "left": 24, "right": 24},
            "border_radius": "md",
            "font_size": 14,
            "font_weight": 600,
        },
    },
    "input": {
        "text": {
            "background": "white",
            "border": "1px solid border",
            "padding": {"top": 10, "bottom": 10, "left": 14, "right": 14},
            "border_radius": "control",
            "font_size": 14,
            "states": {
                "focus": {
                    "border":     "1px solid primary",
                    "box_shadow": "0 0 0 3px rgba(91,94,244,0.15)",
                },
                "error":    {"border": "1px solid danger", "box_shadow": "0 0 0 3px rgba(255,59,48,0.12)"},
                "disabled": {"background": "surface", "opacity": 0.5},
            },
        },
        "textarea": {
            "background": "white",
            "border": "1px solid border",
            "padding": {"top": 10, "bottom": 10, "left": 14, "right": 14},
            "border_radius": "control",
            "font_size": 14,
            "min_height": 120,
        },
    },
    "card": {
        "default": {
            "background":    "white",
            "border":        "1px solid border",
            "border_radius": "card",
            "padding":       {"top": 20, "bottom": 20, "left": 24, "right": 24},
            "shadow":        "sm",
        },
        "elevated": {
            "background":    "white",
            "border":        "none",
            "border_radius": "card",
            "padding":       {"top": 20, "bottom": 20, "left": 24, "right": 24},
            "shadow":        "lg",
        },
        "flat": {
            "background":    "surface",
            "border":        "1px solid border_soft",
            "border_radius": "card",
            "padding":       {"top": 20, "bottom": 20, "left": 24, "right": 24},
            "shadow":        "none",
        },
    },
    "badge": {
        "default": {
            "background":    "primary_light",
            "text_color":    "primary",
            "padding":       {"top": 3, "bottom": 3, "left": 10, "right": 10},
            "border_radius": "full",
            "font_size":     11,
            "font_weight":   600,
        },
        "success": {
            "background":    "success_light",
            "text_color":    "success",
            "padding":       {"top": 3, "bottom": 3, "left": 10, "right": 10},
            "border_radius": "full",
            "font_size":     11,
            "font_weight":   600,
        },
        "danger": {
            "background":    "danger_light",
            "text_color":    "danger",
            "padding":       {"top": 3, "bottom": 3, "left": 10, "right": 10},
            "border_radius": "full",
            "font_size":     11,
            "font_weight":   600,
        },
        "warning": {
            "background":    "warning_light",
            "text_color":    "warning",
            "padding":       {"top": 3, "bottom": 3, "left": 10, "right": 10},
            "border_radius": "full",
            "font_size":     11,
            "font_weight":   600,
        },
        "info": {
            "background":    "info_light",
            "text_color":    "info",
            "padding":       {"top": 3, "bottom": 3, "left": 10, "right": 10},
            "border_radius": "full",
            "font_size":     11,
            "font_weight":   600,
        },
    },
    "header": {
        "default": {
            "background":    "white",
            "border_bottom": "1px solid border",
            "padding":       {"top": 0, "bottom": 0, "left": 24, "right": 24},
            "height":        56,
            "sticky":        True,
        },
    },
    "navigation": {
        "bottom_tab": {
            "height":     56,
            "background": "white",
            "border_top": "1px solid border",
            "items": {
                "active_color":   "primary",
                "inactive_color": "text_tertiary",
                "font_size":      11,
                "font_weight":    500,
            },
        },
        "sidebar": {
            "width":      240,
            "background": "surface",
            "border_right": "1px solid border",
            "padding":    {"top": 16, "bottom": 16, "left": 12, "right": 12},
            "item": {
                "padding":        {"top": 8, "bottom": 8, "left": 12, "right": 12},
                "border_radius":  "sm",
                "font_size":      13,
                "font_weight":    500,
                "default_color":  "text_secondary",
                "active_bg":      "primary_light",
                "active_color":   "primary",
            },
        },
    },
    "tooltip": {
        "default": {
            "background":    "#171717",
            "text_color":    "#FFFFFF",
            "border_radius": "xs",
            "padding":       {"top": 5, "bottom": 5, "left": 8, "right": 8},
            "font_size":     11,
            "font_weight":   500,
            "shadow":        "md",
        },
    },
}


def get_component(component_type: str, variant: str = "default") -> Optional[Dict]:
    """Return component spec from design system, or None if not found."""
    variants = COMPONENTS.get(component_type)
    if not variants:
        return None
    return variants.get(variant) or variants.get("default")


def apply_token(token_path: str) -> Any:
    """Resolve a dot-separated token path, e.g. 'colors.primary' → '#5B5EF4'."""
    value: Any = DESIGN_TOKENS
    for part in token_path.split("."):
        if not isinstance(value, dict):
            return token_path
        value = value.get(part, token_path)
    return value
