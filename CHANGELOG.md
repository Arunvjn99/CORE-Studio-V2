# Changelog

All notable changes to CORE Studio V2 are documented in this file. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.3.1] — 2026-08-18

### Fixed
- Production Docker images (`packages/backend/Dockerfile`,
  `packages/frontend/Dockerfile`) failed to build:
  - `requirements.txt` pinned `anthropic==0.40.0` and `langchain-core==0.3.24`, which
    conflict with `langchain-anthropic==0.3.3`'s own requirements
    (`anthropic>=0.41.0`, `langchain-core>=0.3.30`). Loosened both to compatible ranges.
  - `packages/frontend/package-lock.json` had drifted out of sync with `package.json`
    (missing optional platform packages), which `npm ci` correctly rejects. Regenerated
    inside a `node:20-alpine` container so it matches the platform the image actually
    builds on.
  - `autoprefixer` is required by `postcss.config.js` but was never listed in
    `package.json` — added it as a dev dependency.
- Verified: both `core-studio-backend:2.3.1` and `core-studio-frontend:2.3.1` build
  cleanly end-to-end.

## [2.3.0] — 2026-08-18

### Added
- **Per-screen Edit UI with version history.** A new "Edit screen" (pencil icon) button
  next to Refine/Code on each canvas card opens a modal scoped to exactly that screen —
  replacing the old blind `window.prompt()` refine flow.
  - Instruction textarea + live preview, with a version rail (V1, V2, V3…) — each entry
    carries a real HTML snapshot, the instruction that produced it, a timestamp, and a
    change summary (the instruction itself, never a hardcoded string).
  - Selecting an older version previews it without touching the live screen.
  - "Restore this version" instantly reverts (no LLM call, deterministic) and is recorded
    as a new version — history is append-only, so nothing is ever lost, even when
    restoring a restore.
- Backend: `POST /api/v1/design/restore-screen-version` endpoint.

### Changed
- `regenerate_screen()` now snapshots full HTML per version (not just the refinement
  instruction text) so any prior version can be viewed or restored.

## [2.2.0] — 2026-08-18

### Added
- `VISION_PROVIDER` environment variable (`auto` | `anthropic` | `openai` | `gemini` |
  `ollama`) and `resolve_vision_provider()` — image analysis (the "recreate"/"redesign
  from screenshot" flow) is now resolved independently of `AI_BACKEND_MODE`, so it always
  prefers the best available cloud vision key even when text generation is routed to
  local Ollama.
- `vision_backend_label()` and `vision_provider`/`vision_backend` fields on
  `/api/v1/ai/status` for transparent, non-hardcoded status reporting.

### Fixed
- The "recreate from screenshot" progress message was hardcoded to
  `"Reading reference image with llava:7b..."` regardless of which backend actually ran.
  It now reflects the real resolved provider/model.
- Two upload endpoints (`/api/v1/knowledge/upload` handwritten-OCR path, legacy
  `/api/v1/design/generate`) incorrectly required Ollama to be running even when a cloud
  vision key was fully configured.

## [2.1.0] — 2026-08-18

### Added
- **Figma export pipeline**: `app/design_system/figma_export.py` converts generated
  screen HTML into a real Figma auto-layout node tree (not a flat HTML dump), and a
  companion Figma plugin (`packages/figma-plugin/`) imports it — built on Figma's
  official, documented Plugin API (no reverse-engineered clipboard format, no
  third-party service).
- **Module-wise retirement knowledge base** (`knowledge/domain/retirement/modules/`, 21
  modules) replacing the general-purpose domain selector.
- Real CORE brand mark (exact Figma SVG/colors) embedded in generated screens and the
  frontend (`packages/frontend/public/brand/`).
- README: full "Installing on a new machine (from GitHub)" section — system
  requirements, local (no-Docker) and Docker setup paths, environment variable
  reference, troubleshooting, test instructions.
- Recreate-from-screenshot accuracy overhaul: verbatim title/label transcription in the
  vision prompt, fixed a truncation bug that silently dropped image analysis fields, and
  fixed a severe HTML-truncation bug in screen generation (~20K chars → ~3K chars),
  bringing recreate fidelity to the 80–90%+ target verified against ground-truth
  Chrome-rendered screenshots.
- Per-design dollar cost display (accurate per-model pricing) alongside token counts.

### Changed
- `core-2` design system tokens, layout grammar (7 mined page-shell templates), and
  component variants rebuilt from the real company Figma file (exact colors, spacing
  scale, shadows, Open Sans typography) instead of approximated values.
- Studio UI: `core-2` is now the default design system with other systems hidden behind
  an explicit "Use a different style" toggle; the general-purpose domain selector was
  removed in favor of the fixed retirement domain; QA/Engineering departments hidden
  from navigation (frontend-only, reversible).
- `get_system_prompt_injection()` no longer silently truncates the design-system prompt
  block, which had been cutting off newly-added layout grammar sections.

### Fixed
- Ollama context size silently capped at 4096 tokens regardless of model capability;
  now explicitly set to 32K (text) / 8K (vision).
- Cloud-vision routing checked `ANTHROPIC_API_KEY` specifically as its gate regardless of
  the actually configured `CLOUD_PROVIDER`.

## [2.0.0] — 2026-08-18

### Added
- Initial release of CORE Studio V2 — an AI-powered digital product office with
  Design, Analyst, QA, and Engineering department agents.
- Multi-provider AI routing (Anthropic, OpenAI, Gemini, Ollama) with complexity-based
  model selection.
- RAG knowledge base (ChromaDB) seeded from `knowledge/`.
- Next.js 15 + Turbopack frontend; FastAPI backend with both a local SQLite dev server
  (`server_local.py`) and a production app (`app/main.py`, Postgres + Alembic).
- Design system registry and token builder, design canvas, flow canvas, WebSocket
  streaming agent updates.

[Unreleased]: https://github.com/Arunvjn99/CORE-Studio-V2/compare/v2.3.1...HEAD
[2.3.1]: https://github.com/Arunvjn99/CORE-Studio-V2/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/Arunvjn99/CORE-Studio-V2/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/Arunvjn99/CORE-Studio-V2/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/Arunvjn99/CORE-Studio-V2/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/Arunvjn99/CORE-Studio-V2/releases/tag/v2.0.0
