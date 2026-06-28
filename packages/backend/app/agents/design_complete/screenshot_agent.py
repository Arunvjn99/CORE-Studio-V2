"""
Screenshot → Design Agent using LLava:7b (vision model).
Also handles: handwritten sketch → design, Figma screenshot → editable spec.

Uses Ollama's vision API with base64-encoded images.
"""
import json
import re
import base64
from pathlib import Path
from typing import Optional


async def run_screenshot_to_design(
    image_path: str,
    mode: str,         # recreate | improve | analyze
    context: str,      # additional instructions
    llm_chat_vision,   # special vision-capable llm caller
    select_model,
    rag_query=None,
) -> dict:
    """
    Analyze a screenshot/sketch and extract design structure.
    Uses LLava:7b for visual understanding.
    """
    # Read and encode image
    try:
        image_data = Path(image_path).read_bytes()
        b64_image = base64.b64encode(image_data).decode("utf-8")
    except Exception as e:
        return {"error": f"Could not read image: {e}"}

    if mode == "recreate":
        prompt = f"""Analyze this UI screenshot and extract its complete design structure.
{f'Additional context: {context}' if context else ''}

Identify every UI element, layout, and design pattern. Return ONLY valid JSON:
{{
  "mode": "recreate",
  "screen_analysis": {{
    "name": "Screen name based on content",
    "type": "dashboard | form | list | detail | onboarding | other",
    "layout": "Description of overall layout",
    "background_color": "#hex",
    "primary_color": "#hex",
    "font_family": "Detected or estimated font"
  }},
  "elements": [
    {{
      "type": "header | button | input | card | text | image | nav | table | icon | badge",
      "content": "Text content if visible",
      "position": "top | middle | bottom | left | right | center",
      "style": {{
        "background": "#hex or transparent",
        "text_color": "#hex",
        "border_radius": "sm | md | lg | full",
        "size": "sm | md | lg",
        "font_weight": "normal | medium | semibold | bold"
      }},
      "notes": "Any special characteristics"
    }}
  ],
  "design_system_hints": {{
    "spacing_pattern": "8px grid | 4px grid | custom",
    "color_palette": ["#primary", "#secondary", "#background"],
    "typography_scale": "compact | standard | large",
    "component_style": "flat | material | neumorphic | glassmorphism | minimal"
  }},
  "recreated_screens": [
    {{
      "id": "screen-1",
      "name": "Recreated screen name",
      "description": "What this screen does",
      "elements": []
    }}
  ],
  "improvement_suggestions": [
    "How to improve this design"
  ]
}}"""
    elif mode == "improve":
        prompt = f"""Analyze this UI screenshot and suggest specific improvements.
Context: {context or 'General UI/UX improvements'}

Return ONLY valid JSON:
{{
  "mode": "improve",
  "current_state": {{
    "strengths": ["What works well"],
    "weaknesses": ["What needs improvement"],
    "accessibility_issues": ["Accessibility problems visible"],
    "ux_issues": ["UX friction points"]
  }},
  "improvements": [
    {{
      "element": "Element to improve",
      "current": "Current state",
      "suggested": "Improved version",
      "reason": "Why this improves UX/design",
      "priority": "high | medium | low"
    }}
  ],
  "redesign_suggestions": {{
    "layout": "Layout improvement",
    "visual_hierarchy": "How to improve hierarchy",
    "color_contrast": "Contrast improvements needed",
    "typography": "Typography improvements",
    "spacing": "Spacing improvements"
  }}
}}"""
    else:  # analyze
        prompt = f"""Analyze this UI screenshot comprehensively.
Context: {context or 'Full design analysis'}

Return ONLY valid JSON:
{{
  "mode": "analyze",
  "design_quality_score": 75,
  "summary": "2-3 sentence analysis",
  "ui_patterns": ["Identified UI pattern"],
  "components_detected": ["Component types found"],
  "accessibility_score": 70,
  "mobile_friendliness": "Optimized | Partially | Not optimized",
  "visual_hierarchy": "Strong | Moderate | Weak",
  "consistency_score": 80,
  "detailed_findings": [
    {{"area": "Typography | Colors | Layout | Spacing | Accessibility", "finding": "Observation", "recommendation": "Suggestion"}}
  ]
}}"""

    result = await llm_chat_vision(b64_image, prompt)
    return _parse_or_fallback(result, mode)


async def run_handwritten_to_design(
    image_path: str,
    context: str,
    llm_chat_vision,
    select_model,
) -> dict:
    """Convert handwritten sketch or whiteboard photo to design spec."""
    try:
        image_data = Path(image_path).read_bytes()
        b64_image = base64.b64encode(image_data).decode("utf-8")
    except Exception as e:
        return {"error": f"Could not read image: {e}"}

    prompt = f"""This is a handwritten UI sketch or whiteboard diagram.
Interpret the sketch and extract the design intent.
{f'Designer notes: {context}' if context else ''}

Return ONLY valid JSON:
{{
  "sketch_type": "wireframe | flowchart | component_sketch | user_flow | architecture",
  "interpretation": "What the sketch is trying to communicate",
  "screens": [
    {{
      "id": "screen-1",
      "name": "Screen name interpreted from sketch",
      "purpose": "What this screen does",
      "elements": [
        {{
          "type": "button | input | card | text | nav | list | other",
          "label": "Text from sketch",
          "position": "where on screen",
          "notes": "Designer annotation if visible"
        }}
      ],
      "connections": ["What this screen connects to"]
    }}
  ],
  "user_flows": [
    {{"step": 1, "action": "User action from sketch", "screen": "screen-1"}}
  ],
  "designer_notes": ["Any text annotations found in sketch"],
  "clarifications_needed": ["Unclear elements that need designer confirmation"],
  "suggested_next_steps": ["Recommended design actions based on sketch"]
}}"""

    result = await llm_chat_vision(b64_image, prompt)
    return _parse_or_fallback(result, "handwritten")


def _parse_or_fallback(raw: str, mode: str) -> dict:
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
    return {"mode": mode, "error": "Parse failed", "raw_analysis": raw[:600]}
