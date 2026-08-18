"use strict";
/// <reference types="@figma/plugin-typings" />
/**
 * CORE Studio Import — builds real Figma auto-layout frames from the node tree
 * produced by the backend's html_to_figma_tree() (see
 * packages/backend/app/design_system/figma_export.py). Uses only the official,
 * documented Figma Plugin API — no reverse-engineered clipboard format.
 */
figma.showUI(__html__, { width: 360, height: 420 });
// Caches the RESOLVED font (which may be a fallback), not just a "loaded" flag — a Set
// caused a real bug: the first failed load correctly fell back to Inter, but every
// subsequent text node with the same weight re-read the cache as "already handled" and
// returned the original (never-loaded) font, throwing "Cannot use unloaded font".
const FONT_CACHE = new Map();
async function ensureFont(family, weight) {
    const style = weight >= 700 ? "Bold" : weight >= 600 ? "Semi Bold" : weight >= 500 ? "Medium" : "Regular";
    const key = `${family}::${style}`;
    const cached = FONT_CACHE.get(key);
    if (cached)
        return cached;
    const fontName = { family, style };
    try {
        await figma.loadFontAsync(fontName);
        FONT_CACHE.set(key, fontName);
        return fontName;
    }
    catch (_a) {
        // Fall back to Inter (always available) if the exact family/style isn't installed locally.
        const fallback = { family: "Inter", style: "Regular" };
        await figma.loadFontAsync(fallback);
        FONT_CACHE.set(key, fallback);
        return fallback;
    }
}
function applyLayout(frame, layout) {
    var _a, _b, _c, _d, _e;
    frame.layoutMode = layout.mode;
    if (layout.mode !== "NONE") {
        frame.itemSpacing = (_a = layout.itemSpacing) !== null && _a !== void 0 ? _a : 0;
        frame.paddingTop = (_b = layout.paddingTop) !== null && _b !== void 0 ? _b : 0;
        frame.paddingRight = (_c = layout.paddingRight) !== null && _c !== void 0 ? _c : 0;
        frame.paddingBottom = (_d = layout.paddingBottom) !== null && _d !== void 0 ? _d : 0;
        frame.paddingLeft = (_e = layout.paddingLeft) !== null && _e !== void 0 ? _e : 0;
        if (layout.primaryAxisAlignItems)
            frame.primaryAxisAlignItems = layout.primaryAxisAlignItems;
        // counterAxisAlignItems doesn't support SPACE_BETWEEN (primary axis only) — clamp to MAX.
        if (layout.counterAxisAlignItems) {
            frame.counterAxisAlignItems = layout.counterAxisAlignItems === "SPACE_BETWEEN"
                ? "MAX"
                : layout.counterAxisAlignItems;
        }
    }
}
function applySizing(node, layout) {
    // layoutSizingHorizontal/Vertical only apply meaningfully once the node has an
    // auto-layout parent; Figma ignores/errors otherwise, so this is best-effort.
    try {
        if (layout.sizingHorizontal === "FIXED" && layout.width) {
            node.resize(layout.width, "height" in node ? node.height : 1);
        }
        if (layout.sizingHorizontal)
            node.layoutSizingHorizontal = layout.sizingHorizontal;
        if (layout.sizingVertical)
            node.layoutSizingVertical = layout.sizingVertical;
    }
    catch (_a) {
        // Node isn't inside an auto-layout parent yet (e.g. the root) — ignore.
    }
}
async function buildNode(spec) {
    var _a;
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
    }
    else {
        frame.fills = [];
    }
    if (spec.style.stroke) {
        frame.strokes = [{ type: "SOLID", color: spec.style.stroke }];
        frame.strokeWeight = (_a = spec.style.strokeWeight) !== null && _a !== void 0 ? _a : 1;
    }
    if (spec.style.cornerRadius) {
        frame.cornerRadius = spec.style.cornerRadius;
    }
    for (const childSpec of spec.children) {
        const child = await buildNode(childSpec);
        frame.appendChild(child);
        if (frame.layoutMode !== "NONE") {
            applySizing(child, childSpec.layout);
        }
    }
    if (spec.layout.width && spec.layout.height) {
        frame.resize(spec.layout.width, spec.layout.height);
    }
    return frame;
}
async function importScreens(payload) {
    const createdFrames = [];
    let xOffset = 0;
    for (const screen of payload.screens) {
        const root = await buildNode(screen.tree);
        if (root.type !== "FRAME")
            continue; // top-level should always be a FRAME
        const frame = root;
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
figma.ui.onmessage = async (msg) => {
    if (msg.type !== "import" || !msg.payload)
        return;
    try {
        const count = await importScreens(msg.payload);
        figma.ui.postMessage({ type: "done", count });
    }
    catch (e) {
        figma.ui.postMessage({ type: "error", message: (e === null || e === void 0 ? void 0 : e.message) || String(e) });
    }
};
