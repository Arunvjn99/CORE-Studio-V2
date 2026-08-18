# CORE Studio V2

AI-powered digital product office — a virtual design studio where specialized AI agents collaborate across Design, Analyst, QA, and Engineering departments.

**Repository:** [github.com/Arunvjn99/CORE-Studio-V2](https://github.com/Arunvjn99/CORE-Studio-V2)

## Overview

CORE Studio V2 turns product requirements into designs, documents, and code through a multi-agent pipeline with human-in-the-loop approvals. It supports cloud AI (Anthropic Claude, OpenAI, Gemini) and local AI via Ollama, with a RAG knowledge base backed by ChromaDB.

## Architecture

```
core-studio-v2/
├── packages/
│   ├── backend/          # FastAPI + SQLite/Postgres, agent orchestration
│   └── frontend/         # Next.js 15 + Turbopack, React 18
├── knowledge/            # RAG seed documents (company, domain, design systems)
├── docker-compose.yml    # Full stack (Postgres, Redis, Celery, backend, frontend)
└── Makefile              # Dev shortcuts
```

## Features

### AI Departments
- **Design** — Planner, UX, UI, Review, Accessibility, Screenshot→Design, Code Export
- **Analyst** — Research, BA, Personas, User Stories, PRD, Competitor Analysis
- **QA** — Test cases, WCAG accessibility checks, compliance
- **Engineering** — Code generation, API design, architecture, tech docs

### AI Backend
- Multi-provider routing: Anthropic, OpenAI, Gemini, Ollama
- Complexity-based model selection (fast / standard / advanced)
- `AI_BACKEND_MODE`: `auto` | `cloud` | `ollama`

### Knowledge & RAG
- ChromaDB vector store with automatic seeding from `knowledge/`
- Document upload and indexing (PDF, DOCX, images, text)
- Company standards, domain guidelines, layout references, design systems

### Frontend
- Auth (login / register) with JWT
- Studio sidebar with department navigation
- Design canvas (Fabric.js), flow canvas, agent streaming panel
- Projects, documents, knowledge, and settings pages
- CORE branding with transparent logo asset

### Backend
- Local dev server (`server_local.py`) — SQLite, no Docker required
- Production-ready FastAPI app (`app/main.py`) with Alembic migrations
- WebSocket support for real-time agent updates
- Design system registry and token builder (V1 design system integration)

## Installing on a new machine (from GitHub)

This section walks through everything needed to go from a bare machine to a running app,
cloned fresh from git. Two paths are documented — pick one:

- **Path A — Local, no Docker** (recommended for trying it out / development). Uses SQLite,
  no Postgres/Redis install needed. This is the path verified end-to-end while building this app.
- **Path B — Docker** (closer to production topology: Postgres + Redis + Celery).

### 1. System requirements

| Requirement | Version | Why |
|---|---|---|
| **Git** | any recent version | to clone the repo |
| **Python** | 3.11 or newer (3.13 tested) | backend (FastAPI) |
| **Node.js** | 18 or newer (tested with 20+) | frontend (Next.js) + the Figma plugin build |
| **npm** | bundled with Node | frontend/plugin package installs |
| **~2 GB free disk** | | Python venv + node_modules + (optional) local AI models |

Optional, only if you want the corresponding feature:

| Optional requirement | Needed for |
|---|---|
| **Docker + Docker Compose** | Path B (full stack: Postgres, Redis, Celery) |
| **[Ollama](https://ollama.ai)** | Running AI 100% locally instead of a cloud API key |
| **An API key** for Anthropic, OpenAI, or Gemini | Cloud AI (recommended — much higher quality than local models) |
| **Figma desktop app** | Only for the "Copy to Figma" plugin (`packages/figma-plugin/`) — not required to run the app itself |

You need **either** a cloud API key **or** Ollama running locally — the app auto-detects
which is available (`AI_BACKEND_MODE=auto`). Cloud is strongly recommended for design/vision
quality; local Ollama models work but are noticeably weaker, especially for image-based
"recreate" requests.

### 2. Clone the repository

```bash
git clone https://github.com/Arunvjn99/CORE-Studio-V2.git
cd CORE-Studio-V2
```

### 3. Path A — Local setup (no Docker)

**Backend:**
```bash
cd packages/backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements-local.txt
cp .env.example .env
```
Edit `packages/backend/.env` and set **one** of these AI options:
- Cloud: fill in `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY` / `GEMINI_API_KEY`)
- Local: install [Ollama](https://ollama.ai), then pull the 3 models this app uses:
  ```bash
  ollama pull deepseek-r1:8b       # planning / reasoning
  ollama pull qwen2.5-coder:7b     # UI/code generation
  ollama pull llava:7b             # vision (image analysis, "recreate from screenshot")
  ```
Also set `JWT_SECRET` to any random string.

**Frontend** (new terminal tab):
```bash
cd packages/frontend
npm install
cp .env.example .env.local
```

**Run both:**
```bash
# from repo root
make dev-local
```
Or run each manually in separate terminals:
```bash
cd packages/backend  && source .venv/bin/activate && python3 server_local.py
cd packages/frontend && npm run dev
```

- Frontend → http://localhost:3000
- Backend → http://localhost:8000
- API docs → http://localhost:8000/docs
- Health check → http://localhost:8000/api/health (confirm `"status":"healthy"`)

The local backend uses **SQLite** — a `core_studio_local.db` file is created automatically
on first run, no database setup needed.

### 4. Path B — Docker (full stack)

Requires Docker + Docker Compose installed and running.

```bash
cp .env.example .env
# edit .env — set ANTHROPIC_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY and JWT_SECRET
make dev              # full stack: Postgres, Redis, Celery, backend, frontend
# or, a lighter stack with no Postgres:
make dev-docker
```
This runs Alembic-backed Postgres instead of SQLite — matches the production deployment path.

### 5. (Optional) Copy-to-Figma plugin

Only needed if you want to use the "Figma" export button's companion plugin:
```bash
cd packages/figma-plugin
npm install
npm run build          # compiles code.ts -> code.js
```
Then in the Figma desktop app: **Plugins → Development → Import plugin from manifest…**,
select `packages/figma-plugin/manifest.json`. See `packages/figma-plugin/README.md` for details.

### Troubleshooting

- **"Address already in use" on port 8000** — something else is already running there;
  either stop it or run uvicorn on a different port (`uvicorn server_local:app --port 8010`).
- **Ollama responses seem cut off / errors mentioning context size** — make sure you're on a
  current version of this repo; earlier versions had a bug where Ollama silently capped
  context at 4096 tokens. This is fixed as of the code you just cloned.
- **`ModuleNotFoundError` on backend start** — you're probably not inside the venv; re-run
  `source .venv/bin/activate` in `packages/backend` before starting the server.
- **No AI response / "No vision backend available"** — you need at least one of: a cloud API
  key in `.env`, or Ollama running (`ollama serve`) with the 3 models pulled above.

## Environment

See `packages/backend/.env.example` for all backend variables. Key settings:

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GEMINI_API_KEY` | Cloud AI provider keys (set at least one, or use Ollama) |
| `ANTHROPIC_MODEL` | Default model (e.g. `claude-sonnet-4-6`) |
| `OLLAMA_BASE_URL` | Local Ollama server (default `http://localhost:11434`) |
| `AI_BACKEND_MODE` | `auto`, `cloud`, or `ollama` |
| `JWT_SECRET` | Auth signing secret — set to any long random string |

Frontend env (`packages/frontend/.env.local`):

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend URL |
| `NEXT_PUBLIC_WS_URL` | WebSocket URL |

## Development

```bash
make dev-backend     # Backend only
make dev-frontend    # Frontend only
make stop            # Stop local processes
make lint            # Run linters
make type-check      # TypeScript check
```

### Running tests

```bash
cd packages/backend
pip install pytest pytest-asyncio   # if not already installed
pytest tests/test_core_design_system.py -v
```

## License

Private project — All rights reserved.
