"""UI Builder — creates UI element dicts using design-system tokens & components."""
from typing import Any, Dict, List, Optional
from app.design_system.tokens import DESIGN_TOKENS, COMPONENTS, get_component


class UIBuilder:
    """Build UI screens from the design system."""

    def __init__(self) -> None:
        self.tokens = DESIGN_TOKENS
        self.components = COMPONENTS

    # ── Leaf elements ────────────────────────────────────────────────────────

    def create_heading(self, text: str, level: int = 2, **kw) -> Dict[str, Any]:
        level = max(1, min(6, level))
        styles = ["display_lg", "heading_lg", "heading_md", "heading_sm", "body_lg", "body_md"]
        style_key = styles[level - 1]
        return {
            "id": kw.get("id", f"h{level}-{text[:20].lower().replace(' ', '-')}"),
            "type": "heading",
            "level": level,
            "text": text,
            "style": self.tokens["typography"][style_key],
            "accessible": {"role": "heading", "aria_level": level},
            **kw,
        }

    def create_text(self, content: str, variant: str = "body_md", **kw) -> Dict[str, Any]:
        return {
            "id": kw.get("id", f"text-{len(content) // 10}"),
            "type": "text",
            "content": content,
            "style": self.tokens["typography"].get(variant, self.tokens["typography"]["body_md"]),
            "accessible": {"role": "paragraph"},
            **kw,
        }

    def create_button(self, label: str, variant: str = "primary", **kw) -> Dict[str, Any]:
        spec = get_component("button", variant)
        return {
            "id": kw.get("id", f"btn-{label.lower().replace(' ', '-')}"),
            "type": "button",
            "label": label,
            "variant": variant,
            "spec": spec,
            "accessible": {"label": label, "role": "button", "aria_pressed": "false"},
            **kw,
        }

    def create_input(self, label: str, input_type: str = "text", **kw) -> Dict[str, Any]:
        spec = get_component("input", input_type if input_type in ("text", "textarea") else "text")
        return {
            "id": kw.get("id", f"input-{label.lower().replace(' ', '-')}"),
            "type": "input",
            "input_type": input_type,
            "label": label,
            "placeholder": kw.get("placeholder", f"Enter {label.lower()}"),
            "required": kw.get("required", False),
            "spec": spec,
            "accessible": {
                "label": label,
                "aria_required": kw.get("required", False),
                "aria_describedby": f"{label.lower().replace(' ', '-')}-help",
            },
            **kw,
        }

    def create_card(self, children: List[Dict], variant: str = "default", **kw) -> Dict[str, Any]:
        spec = get_component("card", variant)
        return {
            "id": kw.get("id", f"card-{len(children)}"),
            "type": "card",
            "children": children,
            "spec": spec,
            "accessible": {"role": "region"},
            **kw,
        }

    def create_badge(self, label: str, variant: str = "default", **kw) -> Dict[str, Any]:
        spec = get_component("badge", variant)
        return {
            "id": kw.get("id", f"badge-{label.lower().replace(' ', '-')}"),
            "type": "badge",
            "label": label,
            "spec": spec,
            "accessible": {"role": "status", "aria_label": label},
            **kw,
        }

    # ── Screen ───────────────────────────────────────────────────────────────

    def create_screen(self, name: str, elements: List[Dict], **kw) -> Dict[str, Any]:
        return {
            "id": kw.get("id", f"screen-{name.lower().replace(' ', '-')}"),
            "name": name,
            "description": kw.get("description", ""),
            "background": kw.get("background", self.tokens["colors"]["background"]),
            "padding": kw.get("padding", self.tokens["spacing"]["6"]),  # 24px
            "elements": elements,
            "accessible": {"lang": "en"},
            **kw,
        }

    # ── Helpers ──────────────────────────────────────────────────────────────

    def elements_from_wireframe_sections(self, sections: List[Dict]) -> List[Dict]:
        """Convert wireframe section list → element list."""
        elements: List[Dict] = []
        for sec in sections:
            stype = sec.get("type", "text")
            if stype == "header":
                elements.append(self.create_heading(sec.get("content", ""), level=1))
            elif stype in ("heading", "section_title"):
                elements.append(self.create_heading(sec.get("content") or sec.get("title", ""), level=2))
            elif stype in ("description", "text"):
                elements.append(self.create_text(sec.get("content", "")))
            elif stype == "cta_button":
                elements.append(self.create_button(sec.get("label", "Get Started"), "primary"))
            elif stype == "button":
                v = "primary" if sec.get("style") == "primary" else "secondary"
                elements.append(self.create_button(sec.get("label", "Button"), v))
            elif stype == "button_group":
                for btn in sec.get("buttons") or []:
                    v = "primary" if btn.get("style") == "primary" else "secondary"
                    elements.append(self.create_button(btn.get("label", "Button"), v))
            elif stype == "form":
                for field in sec.get("fields") or []:
                    elements.append(self.create_input(
                        field.get("label", "Field"),
                        field.get("type", "text"),
                        required=field.get("required", False),
                    ))
            elif stype == "form_group":
                for field in sec.get("fields") or []:
                    elements.append(self.create_input(
                        field.get("label", "Field"),
                        field.get("type", "text"),
                    ))
            elif stype == "success_message":
                elements.append(self.create_badge(sec.get("title") or "✓ Success", "success"))
            elif stype == "card":
                elements.append(self.create_card([self.create_text("Card content")]))
            elif stype in ("progress", "progress_indicator"):
                elements.append({
                    "id": "progress",
                    "type": "progress",
                    "value": sec.get("value", 50),
                    "label": sec.get("label", ""),
                    "accessible": {"role": "progressbar"},
                })
        return elements


# Global instance
ui_builder = UIBuilder()
