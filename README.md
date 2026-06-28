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

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- (Optional) Ollama for local AI
- (Optional) Docker for full stack

### Setup

```bash
make setup
# Edit packages/backend/.env with your API keys
cp packages/backend/.env.example packages/backend/.env
cp packages/frontend/.env.example packages/frontend/.env.local
```

### Run locally (recommended)

```bash
make dev-local
```

- Frontend → http://localhost:3000
- Backend → http://localhost:8000
- API Docs → http://localhost:8000/docs

### Run with Docker

```bash
make dev              # Full stack (Postgres, Redis, Celery)
make dev-docker       # Lightweight Docker dev stack
```

## Environment

See `packages/backend/.env.example` for all backend variables. Key settings:

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API key |
| `ANTHROPIC_MODEL` | Default model (e.g. `claude-sonnet-4-6`) |
| `AI_BACKEND_MODE` | `auto`, `cloud`, or `ollama` |
| `JWT_SECRET` | Auth signing secret |

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

## License

Private project — All rights reserved.
