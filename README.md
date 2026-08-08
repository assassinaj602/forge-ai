# ForgeAI — Production AI Workspace

ForgeAI is a production-grade AI Engineering workspace featuring FastAPI, PostgreSQL, JWT Authentication, Multi-tenant Data Isolation, Alembic Migrations, and Docker containerization.

---

## Milestone 1 Overview & Architecture

Milestone 1 establishes the production architecture core:

1. **Backend Framework**: FastAPI application with CORS middleware (`app/main.py`).
2. **Database & ORM**: PostgreSQL default with async SQLAlchemy 2.0 (`User`, `Conversation`, `Message` models in `app/db/models.py`). SQLite in-memory engine is dedicated to automated unit tests.
3. **Database Schema Migrations**: Managed exclusively via Alembic (`alembic/versions/`). Schema creation on app startup (`Base.metadata.create_all`) is explicitly disabled.
4. **Authentication & Security Core**:
   - Bearer Token JWT authentication with `HS256` and configurable `SECRET_KEY` validation.
   - Password hashing via `pbkdf2_sha256` / `bcrypt` with passlib.
   - Minimum 8-character password policy enforcement.
   - Profile & user state management (`/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/me`).
5. **Multi-Tenant Data Isolation**: Strict user-level tenant isolation enforced across endpoints.
6. **Containerization & Deployment**: `docker-compose.yml` orchestrating PostgreSQL 15 and FastAPI backend service with automated migration execution on boot.

---

## Local Development & Installation

### Option 1: Docker Compose (Recommended)

1. Copy environment template:
   ```bash
   cp .env.example .env
   ```
2. Start containers:
   ```bash
   docker compose up --build
   ```
   The backend API will be available at `http://localhost:8000`. OpenAPI documentation is accessible at `http://localhost:8000/api/v1/openapi.json`.

### Option 2: Local Python Environment

1. Navigate to backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. Install package in editable mode with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Set required environment variables:
   ```bash
   export ENVIRONMENT=development
   export SECRET_KEY=change-this-to-a-secure-random-secret-key-min-32-chars
   export DATABASE_URL=postgresql+asyncpg://postgres:postgrespassword@localhost:5432/forgeai
   ```
5. Apply database migrations:
   ```bash
   alembic upgrade head
   ```
6. Start dev server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

---

## Running Automated Tests

Run the full async pytest suite:
```bash
cd backend
python -m pytest
```

---

## Features Roadmap
- [x] Repository Foundation & Architecture
- [x] Milestone 1: Authentication Core, Alembic Migrations, Docker & User Tenant Isolation
- [ ] Milestone 2: Multi-Model AI Chat & Streaming Engine
- [ ] Milestone 3: Document Processing & RAG Knowledge Engine
- [ ] Milestone 4: Tool Calling & Dynamic Tool Framework
- [ ] Milestone 5: Autonomous AI Agents Framework
- [ ] Milestone 6: AI Evaluation, Observability & Cost Tracking
- [ ] Milestone 7: Full Stack UI Dashboard & Production Packaging
