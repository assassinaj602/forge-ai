# Deployment & Setup Guide — ForgeAI

This guide outlines containerized deployment with Docker Compose and Nginx, environment configuration, and production best practices.

---

## 1. Environment Configuration

Copy `.env.example` to `.env` and configure key secrets:

```ini
ENVIRONMENT=production
SECRET_KEY=generate-a-secure-random-32-char-key-here
DATABASE_URL=postgresql+asyncpg://postgres:postgrespassword@db:5432/forgeai

# Provider API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# System Safeguards
MAX_AGENT_ITERATION_LIMIT=10
DEFAULT_CACHE_SIMILARITY_THRESHOLD=0.92
```

---

## 2. Docker Compose Deployment

Start all backend services, PostgreSQL database, and Nginx reverse proxy:

```bash
docker compose up -d --build
```

### Access Points
- **Frontend Dashboard**: `http://localhost:80`
- **Backend REST API**: `http://localhost:8000/api/v1`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 3. Database Migration Execution

To manually trigger Alembic database migrations inside the backend container:

```bash
docker compose exec backend alembic upgrade head
```
