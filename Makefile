.PHONY: setup dev dev-backend dev-frontend dev-docker dev-docker-down dev-docker-logs build down logs clean install

# ─── Setup ───────────────────────────────────────────────────────────────────
setup: ## First-time setup
	@cp .env.example .env
	@echo "✓ .env created — add your API keys"
	@$(MAKE) install

install: ## Install all dependencies
	@echo "Installing backend dependencies..."
	@cd packages/backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	@cd packages/frontend && npm install
	@echo "✓ Dependencies installed"

# ─── Development ─────────────────────────────────────────────────────────────
dev: ## Start full stack with Docker
	docker compose up --build

dev-local: ## Start backend + frontend locally (NO Docker needed)
	@echo "Starting CORE Studio V2 locally..."
	@cd packages/backend && python3 server_local.py &
	@sleep 2
	@cd packages/frontend && npm run dev
	@echo ""
	@echo "  Backend → http://localhost:8000"
	@echo "  Frontend → http://localhost:3000"
	@echo "  API Docs → http://localhost:8000/docs"

dev-docker: ## Start full stack with Docker (same flow as dev-local, no Postgres needed)
	docker compose -f docker-compose.dev.yml up --build

dev-docker-down: ## Stop Docker dev stack
	docker compose -f docker-compose.dev.yml down

dev-docker-logs: ## Tail Docker dev logs
	docker compose -f docker-compose.dev.yml logs -f

dev-backend: ## Run local backend (SQLite, no Docker)
	cd packages/backend && python3 server_local.py

dev-frontend: ## Run frontend locally
	cd packages/frontend && npm run dev

stop: ## Stop all local dev processes
	@-pkill -f "server_local.py" 2>/dev/null
	@-pkill -f "next dev" 2>/dev/null
	@echo "Stopped"

# ─── Database ────────────────────────────────────────────────────────────────
migrate: ## Run DB migrations
	cd packages/backend && alembic upgrade head

migrate-create: ## Create new migration (usage: make migrate-create NAME=add_something)
	cd packages/backend && alembic revision --autogenerate -m "$(NAME)"

db-reset: ## Reset database (DESTRUCTIVE)
	docker compose exec postgres psql -U core_user -c "DROP DATABASE IF EXISTS core_studio; CREATE DATABASE core_studio;"
	@$(MAKE) migrate

# ─── Docker ──────────────────────────────────────────────────────────────────
build: ## Build all Docker images
	docker compose build

down: ## Stop all services
	docker compose down

logs: ## Show all logs
	docker compose logs -f

logs-backend: ## Show backend logs
	docker compose logs -f backend

# ─── Quality ─────────────────────────────────────────────────────────────────
lint: ## Run all linters
	cd packages/backend && ruff check .
	cd packages/frontend && npm run lint

type-check: ## Run type checks
	cd packages/frontend && npm run type-check

# ─── Utilities ───────────────────────────────────────────────────────────────
clean: ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	cd packages/frontend && rm -rf .next

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
