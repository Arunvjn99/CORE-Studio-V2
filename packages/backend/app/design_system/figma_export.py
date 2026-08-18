"""
HTML -> Figma auto-layout node tree converter.

Turns a generated screen's self-contained HTML (always inline-styled, always flexbox-based —
true for every screen produced by flow_generator.py) into a plain JSON tree that a companion
Figma plugin (packages/figma-plugin/) can walk to build real auto-layout frames via Figma's
official Plugin API (figma.createFrame, layoutMode, itemSpacing, etc.).

Deliberately uses only the stdlib html.parser — no BeautifulSoup/lxml dependency needed for
the well-formed, always-inline-styled HTML this app itself generates.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Optional


# ── CSS value parsing helpers ──────────────────────────────────────────────

_PX = re.compile(r"(-?\d+(?:\.\d+)?)px")


def _px(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    m = _PX.search(value)
    return float(m.group(1)) if m else None


def _parse_style(style_str: str) -> dict:
    """'color:#fff; padding: 4px 8px' -> {'color': '#fff', 'padding': '4px 8px'}"""
    out = {}
    for decl in style_str.split(";"):
        if ":" not in decl:
            continue
        k, v = decl.split(":", 1)
        out[k.strip().lower()] = v.strip()
    return out


def _parse_padding(style: dict) -> dict:
    """Returns {top, right, bottom, left} in px, defaulting missing sides to 0."""
    if "padding" in style:
        parts = [p for p in style["padding"].replace("px", "px ").split() if p]
        vals = [(_px(p) or 0) for p in parts]
        if len(vals) == 1:
            t = r = b = l = vals[0]
        elif len(vals) == 2:
            t = b = vals[0]; r = l = vals[1]
        elif len(vals) == 3:
            t = vals[0]; r = l = vals[1]; b = vals[2]
        else:
            t, r, b, l = (vals + [0, 0, 0, 0])[:4]
        return {"top": t, "right": r, "bottom": b, "left": l}
    return {
        "top": _px(style.get("padding-top")) or 0,
        "right": _px(style.get("padding-right")) or 0,
        "bottom": _px(style.get("padding-bottom")) or 0,
        "left": _px(style.get("padding-left")) or 0,
    }


_ALIGN_MAP = {
    "flex-start": "MIN", "start": "MIN", "left": "MIN", "top": "MIN",
    "center": "CENTER",
    "flex-end": "MAX", "end": "MAX", "right": "MAX", "bottom": "MAX",
    "space-between": "SPACE_BETWEEN",
}


def _rgb_to_figma_color(value: str) -> Optional[dict]:
    """'#RRGGBB' or 'rgb(r,g,b)' -> {r,g,b} floats 0-1 for a Figma SOLID fill."""
    value = value.strip()
    if value.startswith("#"):
        hexv = value.lstrip("#")
        if len(hexv) == 3:
            hexv = "".join(c * 2 for c in hexv)
        if len(hexv) != 6:
            return None
        r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4))
        return {"r": r, "g": g, "b": b}
    m = re.match(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)", value)
    if m:
        r, g, b = (float(x) / 255 for x in m.groups())
        return {"r": r, "g": g, "b": b}
    return None


class _Node:
    __slots__ = ("tag", "style", "text", "children")

    def __init__(self, tag: str, style: dict):
        self.tag = tag
        self.style = style
        self.text = ""
        self.children: list["_Node"] = []


class _TreeBuilder(HTMLParser):
    """Builds a lightweight DOM of _Node from raw generated HTML, skipping <script>/<style>."""

    _VOID_TAGS = {"br", "hr", "img", "input", "meta", "link"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Node("root", {})
        self._stack = [self.root]
        self._skip_depth = 0  # inside <script>/<style>/<head>

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag in ("script", "style", "head"):
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        node = _Node(tag, _parse_style(attrs_d.get("style", "")))
        self._stack[-1].children.append(node)
        if tag not in self._VOID_TAGS:
            self._stack.append(node)

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return
        if len(self._stack) > 1 and self._stack[-1].tag == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self._skip_depth:
            return
        text = data.strip()
        if text and self._stack[-1] is not self.root:
            self._stack[-1].text += (" " if self._stack[-1].text else "") + text


def _convert(node: "_Node") -> dict:
    style = node.style
    is_flex = style.get("display", "").startswith("flex")
    direction = style.get("flex-direction", "row")
    padding = _parse_padding(style)

    spec = {
        "type": "TEXT" if (node.text and not node.children) else "FRAME",
        "tag": node.tag,
        "layout": {
            "mode": "NONE",
        },
        "style": {},
        "children": [],
    }

    # Figma has no concept of free/absolute positioning for a frame's children outside
    # auto-layout — a non-flex wrapper <div> would leave every child stacked at (0,0),
    # overlapping. Our generator never actually relies on absolute positioning (every
    # screen in this app is built from nested flexbox), so any non-leaf, non-flex node
    # is treated as a pass-through wrapper and defaults to vertical auto-layout instead
    # of leaving layoutMode "NONE".
    if is_flex or node.children:
        spec["layout"]["mode"] = (
            "VERTICAL" if not is_flex or direction in ("column", "column-reverse") else "HORIZONTAL"
        )
        gap = _px(style.get("gap"))
        if gap is not None:
            spec["layout"]["itemSpacing"] = gap
        spec["layout"]["paddingTop"] = padding["top"]
        spec["layout"]["paddingRight"] = padding["right"]
        spec["layout"]["paddingBottom"] = padding["bottom"]
        spec["layout"]["paddingLeft"] = padding["left"]
        if "justify-content" in style:
            spec["layout"]["primaryAxisAlignItems"] = _ALIGN_MAP.get(style["justify-content"], "MIN")
        if "align-items" in style:
            spec["layout"]["counterAxisAlignItems"] = _ALIGN_MAP.get(style["align-items"], "MIN")

    width = style.get("width", "")
    if width == "100%" or "flex" in style and style.get("flex", "").strip() in ("1", "1 1 0%", "1 1 auto"):
        spec["layout"]["sizingHorizontal"] = "FILL"
    elif _px(width) is not None:
        spec["layout"]["sizingHorizontal"] = "FIXED"
        spec["layout"]["width"] = _px(width)
    else:
        spec["layout"]["sizingHorizontal"] = "HUG"

    height = style.get("height", "")
    h_px = _px(height)
    if h_px is not None:
        spec["layout"]["sizingVertical"] = "FIXED"
        spec["layout"]["height"] = h_px
    elif height == "100%":
        spec["layout"]["sizingVertical"] = "FILL"
    else:
        spec["layout"]["sizingVertical"] = "HUG"

    if "background" in style or "background-color" in style:
        fill = _rgb_to_figma_color(style.get("background-color") or style.get("background", ""))
        if fill:
            spec["style"]["fill"] = fill
    if "border-radius" in style:
        r = _px(style["border-radius"])
        if r is not None:
            spec["style"]["cornerRadius"] = r
    if "border" in style or "border-bottom" in style or "border-top" in style:
        border_decl = style.get("border") or style.get("border-bottom") or style.get("border-top", "")
        color_match = re.search(r"(#[0-9a-fA-F]{3,6}|rgba?\([^)]+\))", border_decl)
        if color_match:
            stroke = _rgb_to_figma_color(color_match.group(1))
            if stroke:
                spec["style"]["stroke"] = stroke
        width_match = _PX.search(border_decl)
        if width_match:
            spec["style"]["strokeWeight"] = float(width_match.group(1))

    if node.text and not node.children:
        spec["type"] = "TEXT"
        spec["text"] = node.text
        spec["style"]["fontSize"] = _px(style.get("font-size")) or 14
        weight = style.get("font-weight", "400").strip()
        spec["style"]["fontWeight"] = int(weight) if weight.isdigit() else (700 if weight == "bold" else 400)
        color = _rgb_to_figma_color(style.get("color", "#000000"))
        if color:
            spec["style"]["textColor"] = color
        font_family = style.get("font-family", "")
        spec["style"]["fontFamily"] = font_family.split(",")[0].strip().strip("'\"") or "Open Sans"
    else:
        for child in node.children:
            spec["children"].append(_convert(child))

    return spec


def html_to_figma_tree(html: str) -> dict:
    """Convert one screen's generated HTML string into a Figma-plugin-consumable node tree."""
    builder = _TreeBuilder()
    builder.feed(html)
    # The generator always wraps output in a single outer div — find the first real element.
    body_children = builder.root.children
    if len(body_children) == 1:
        return _convert(body_children[0])
    # Multiple top-level nodes (e.g. a full <html><body>...): wrap in a synthetic vertical frame.
    wrapper = _Node("div", {"display": "flex", "flex-direction": "column"})
    wrapper.children = body_children
    return _convert(wrapper)
