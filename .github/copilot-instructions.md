<!-- .github/copilot-instructions.md - tailored guidance for AI coding agents -->

# Quick Purpose
Provide focused, actionable context for an AI code assistant to be immediately productive in this repo.

## Big picture (what runs where)
- Backend: `api/` — FastAPI application (entry: `api/main.py`). Uses `sqlmodel` for models and Alembic for migrations (`api/migrations/`, `alembic.ini`).
- Frontend: `web/` — Next.js app (React + TypeScript) served on port 3000 in `docker-compose.yml`.
- Database: PostgreSQL (declared in `docker-compose.yml`, container `sigmatech2-db`, host port `5000`).
- Orchestration: `docker-compose.yml` builds and mounts source directories for local development (volumes mount `./api` and `./web`).

## Key files & directories (where to look first)
- `api/main.py` — FastAPI app & router registration.
- `api/routes/` — Routers split under `crud/` (resource CRUD) and `business/` (higher-level flows, e.g., `auth.py`).
- `api/services/` and `api/services/impl/` — service interfaces and concrete implementations. Prefer changing impl files when adding behavior.
- `api/models/` — SQLModel model definitions (`user.py`, `product.py`, etc.).
- `api/db/` — DB connection code (`engines.py`, `session_context.py`, `transactional.py`). Use these rather than creating ad-hoc engines/sessions.
- `api/utils/` — helpers: `crypto.py`, `jwt.py` (use these for hashing and token handling to remain consistent).
- `api/migrations/` & `alembic.ini` — DB migrations. Use Alembic for schema changes.
- `docker/` — Dockerfiles for `api` and `web` used by `docker-compose.yml`.
- `api/pyproject.toml` — dependency and test group (Poetry-style). Use Poetry if available.

## Typical developer workflows (concrete commands)
- Run full stack locally (recommended):
  - `docker-compose up --build`
    - API → port `8000`; Web → `3000`; DB → `5000` (PostgreSQL on 5432).
- Run API locally (no Docker):
  - `cd api`
  - (preferred) `poetry install` then `poetry run uvicorn main:app --reload --port 8000`
  - (fallback) `python -m venv .venv && . .venv/bin/activate && pip install -e . && uvicorn main:app --reload --port 8000`
- Run migrations:
  - `cd api && alembic upgrade head` (uses `api/alembic.ini` and `api/migrations`).
- Run tests:
  - `cd api && pytest -q`

## Project-specific conventions & patterns
- Service layering: business logic lives behind `services` interfaces; concrete code lives in `services/impl`. When adding behavior, add/extend an impl and update the service wiring.
- Routes separation: `routes/crud/` for resource CRUD handlers, `routes/business/` for composed flows (auth, domain logic). Keep router registration centralized in `api/main.py`.
- DB access: use `db.session_context` or `transactional` helpers. Do not construct bare sessions or connections; follow existing context manager patterns to ensure correct session lifecycle and commits/rollbacks.
- i18n: translations live under `api/lang/*.yml` and are used via `core.i18n` + `i18n.t(...)`. Use `t("common.xxx")` for messages.
- Errors: project exposes custom exceptions under `api/exceptions/` (including subpackages like `auth/` and `models/`). Raise these to keep consistent error handling.
- Passwords and tokens: use `api/utils/crypto.py` and `api/utils/jwt.py` — do not reimplement hashing or JWT logic.

## Integration & external dependencies
- Uses `sqlmodel` + `psycopg2-binary` with PostgreSQL and Alembic for migrations. Confirm DB URL in `api/db/engines.py` before running migrations.
- Authentication/deps: dependencies live in `api/deps/` (e.g., `auth.py`) and are applied application-wide via `main.py` (`dependencies=[*auth_deps]`). Be careful when modifying global dependencies.

## Examples (patterns to follow)
- Add a new CRUD route for `Product`:
  1. Add/extend model in `api/models/product.py`.
  2. Add business logic in `api/services/` or `api/services/impl/product_service_impl.py`.
  3. Add router in `api/routes/crud/product.py` and include it in `api/main.py`'s `routers` list.
- Use DB session pattern:
  - Example: `with session_context() as session: ...` or decorate with `@transactional()` when appropriate.

## What not to change (unless intentionally refactoring)
- Do not change DB session helpers, global dependency wiring, or `utils/` crypto/jwt implementations unless replacing with a fully-compatible implementation.
- Avoid changing `docker-compose.yml` ports or volume mounts without confirming effect on developer workflow.

## Where to look for help/verification
- Run tests in `api/tests/` (see `api/pytest.ini`). Start with `api/tests/test_crypto.py` to confirm crypto utilities.
- Use `docker-compose logs -f api` for API runtime logs when using Docker Compose.

## If you're an AI agent and need clarification
- Ask for the intended runtime (Docker vs local dev) and whether DB schema changes are allowed.
- Ask which service (API or web) to prioritize, or whether to add a migration and tests for any schema change.
