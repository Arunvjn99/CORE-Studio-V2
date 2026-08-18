/// <reference types="@figma/plugin-typings" />

/**
 * CORE Studio Import — builds real Figma auto-layout frames from the node tree
 * produced by the backend's html_to_figma_tree() (see
 * packages/backend/app/design_system/figma_export.py). Uses only the official,
 * documented Figma Plugin API — no reverse-engineered clipboard format.
 */

figma.showUI(__html__, { width: 360, height: 420 });

interface RgbColor {
  r: number;
  g: number;
  b: number;
}

interface NodeLayout {
  mode: "NONE" | "HORIZONTAL" | "VERTICAL";
  itemSpacing?: number;
  paddingTop?: number;
  paddingRight?: number;
  paddingBottom?: number;
  paddingLeft?: number;
  primaryAxisAlignItems?: "MIN" | "CENTER" | "MAX" | "SPACE_BETWEEN";
  counterAxisAlignItems?: "MIN" | "CENTER" | "MAX" | "SPACE_BETWEEN";
  sizingHorizontal?: "FIXED" | "HUG" | "FILL";
  sizingVertical?: "FIXED" | "HUG" | "FILL";
  width?: number;
  height?: number;
}

interface NodeStyle {
  fill?: RgbColor;
  stroke?: RgbColor;
  strokeWeight?: number;
  cornerRadius?: number;
  fontSize?: number;
  fontWeight?: number;
  fontFamily?: string;
  textColor?: RgbColor;
}

interface NodeSpec {
  type: "FRAME" | "TEXT";
  tag: string;
  layout: NodeLayout;
  style: NodeStyle;
  children: NodeSpec[];
  text?: string;
}

interface ScreenSpec {
  title: string;
  width: number;
  height: number;
  tree: NodeSpec;
}

interface ImportPayload {
  version: string;
  screens: ScreenSpec[];
}

// Caches the RESOLVED font (which may be a fallback), not just a "loaded" flag — a Set
// caused a real bug: the first failed load correctly fell back to Inter, but every
// subsequent text node with the same weight re-read the cache as "already handled" and
// returned the original (never-loaded) font, throwing "Cannot use unloaded font".
const FONT_CACHE = new Map<string, FontName>();

async function ensureFont(family: string, weight: number): Promise<FontName> {
  const style = weight >= 700 ? "Bold" : weight >= 600 ? "Semi Bold" : weight >= 500 ? "Medium" : "Regular";
  const key = `${family}::${style}`;
  const cached = FONT_CACHE.get(key);
  if (cached) return cached;

  const fontName: FontName = { family, style };
  try {
    await figma.loadFontAsync(fontName);
    FONT_CACHE.set(key, fontName);
    return fontName;
  } catch {
    // Fall back to Inter (always available) if the exact family/style isn't installed locally.
    const fallback: FontName = { family: "Inter", style: "Regular" };
    await figma.loadFontAsync(fallback);
    FONT_CACHE.set(key, fallback);
    return fallback;
  }
}

function applyLayout(frame: FrameNode, layout: NodeLayout) {
  frame.layoutMode = layout.mode;
  if (layout.mode !== "NONE") {
    frame.itemSpacing = layout.itemSpacing ?? 0;
    frame.paddingTop = layout.paddingTop ?? 0;
    frame.paddingRight = layout.paddingRight ?? 0;
    frame.paddingBottom = layout.paddingBottom ?? 0;
    frame.paddingLeft = layout.paddingLeft ?? 0;
    if (layout.primaryAxisAlignItems) frame.primaryAxisAlignItems = layout.primaryAxisAlignItems;
    // counterAxisAlignItems doesn't support SPACE_BETWEEN (primary axis only) — clamp to MAX.
    if (layout.counterAxisAlignItems) {
      frame.counterAxisAlignItems = layout.counterAxisAlignItems === "SPACE_BETWEEN"
        ? "MAX"
        : layout.counterAxisAlignItems;
    }
  }
}

function applySizing(node: FrameNode | TextNode, layout: NodeLayout) {
  // layoutSizingHorizontal/Vertical only apply meaningfully once the node has an
  // auto-layout parent; Figma ignores/errors otherwise, so this is best-effort.
  try {
    if (layout.sizingHorizontal === "FIXED" && layout.width) {
      node.resize(layout.width, "height" in node ? node.height : 1);
    }
    if (layout.sizingHorizontal) (node as any).layoutSizingHorizontal = layout.sizingHorizontal;
    if (layout.sizingVertical) (node as any).layoutSizingVertical = layout.sizingVertical;
  } catch {
    // Node isn't inside an auto-layout parent yet (e.g. the root) — ignore.
  }
}

async function buildNode(spec: NodeSpec): Promise<SceneNode> {
  if (spec.type === "TEXT") {
    const text = figma.createText();
    const fontName = await ensureFont(spec.style.fontFamily || "Open Sans", spec.style.fontWeight || 400);
    text.fontName = fontName;
    text.fontSize = spec.style.fontSize || 14;
    text.characters = spec.text || "";
    if (spec.style.textColor) {
      text.fills = [{ type: "SOLID", color: spec.style.textColor }];
    }
    applySizing(text, spec.layout);
    return text;
  }

  const frame = figma.createFrame();
  frame.name = spec.tag || "Frame";
  applyLayout(frame, spec.layout);

  if (spec.style.fill) {
    frame.fills = [{ type: "SOLID", color: spec.style.fill }];
  } else {
    frame.fills = [];
  }
  if (spec.style.stroke) {
    frame.strokes = [{ type: "SOLID", color: spec.style.stroke }];
    frame.strokeWeight = spec.style.strokeWeight ?? 1;
  }
  if (spec.style.cornerRadius) {
    frame.cornerRadius = spec.style.cornerRadius;
  }

  for (const childSpec of spec.children) {
    const child = await buildNode(childSpec);
    frame.appendChild(child);
    if (frame.layoutMode !== "NONE") {
      applySizing(child as FrameNode | TextNode, childSpec.layout);
    }
  }

  if (spec.layout.width && spec.layout.height) {
    frame.resize(spec.layout.width, spec.layout.height);
  }

  return frame;
}

async function importScreens(payload: ImportPayload) {
  const createdFrames: FrameNode[] = [];
  let xOffset = 0;

  for (const screen of payload.screens) {
    const root = await buildNode(screen.tree);
    if (root.type !== "FRAME") continue; // top-level should always be a FRAME
    const frame = root as FrameNode;
    frame.name = screen.title || "Screen";
    frame.x = xOffset;
    frame.y = 0;
    if (screen.width && screen.height && frame.layoutMode === "NONE") {
      frame.resize(screen.width, screen.height);
    }
    figma.currentPage.appendChild(frame);
    createdFrames.push(frame);
    xOffset += (screen.width || frame.width) + 100;
  }

  figma.viewport.scrollAndZoomIntoView(createdFrames);
  return createdFrames.length;
}

figma.ui.onmessage = async (msg: { type: string; payload?: ImportPayload }) => {
  if (msg.type !== "import" || !msg.payload) return;
  try {
    const count = await importScreens(msg.payload);
    figma.ui.postMessage({ type: "done", count });
  } catch (e: any) {
    figma.ui.postMessage({ type: "error", message: e?.message || String(e) });
  }
};
