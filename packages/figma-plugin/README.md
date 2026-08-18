# CORE Studio Import (Figma plugin)

Companion plugin that turns a screen exported from CORE Studio into a real, editable
auto-layout Figma design — using Figma's official, documented Plugin API only (no
reverse-engineered clipboard format).

## How it works

1. In CORE Studio, generate a screen and click the **Figma** button in the canvas header.
   This downloads `core-studio-figma.json` — a structured node tree (not a flat HTML dump),
   produced by `packages/backend/app/design_system/figma_export.py`.
2. In the Figma desktop app: **Plugins → Development → Import plugin from manifest…**, select
   this folder's `manifest.json`.
3. Run the plugin (**Plugins → Development → CORE Studio Import**), paste the exported JSON's
   contents into the textarea, click **Import**.
4. Real Figma frames appear on the canvas: correct auto-layout (`layoutMode`, `itemSpacing`,
   padding, alignment), correct sizing (fixed/hug/fill), and editable text nodes — not a
   rasterized image.

## Development

```bash
npm install
npm run build     # compiles code.ts -> code.js (tsc, one-shot)
npm run watch     # recompiles on save
```

## Why no clipboard-paste "magic"?

Figma's own copy/paste between Figma tabs relies on an undocumented, proprietary binary
payload embedded in the clipboard. There's no supported way to author that format ourselves,
so third parties either reverse-engineer it (fragile, breaks silently on Figma updates) or
pay a vendor API to do it for them. This plugin instead uses Figma's official Plugin API
directly — same end result (a real, editable, auto-layout design), stable and unofficial-format-free.
