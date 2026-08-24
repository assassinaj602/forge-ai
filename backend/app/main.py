from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.rate_limit import RateLimitMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.conversations import router as conv_router
from app.api.v1.chat import router as chat_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.tools import router as tools_router
from app.api.v1.agents import router as agents_router
from app.api.v1.evaluations import router as eval_router
from app.api.v1.observability import router as obs_router
from app.api.v1.mcp import router as mcp_router
from app.api.v1.ws import router as ws_router
from app.api.v1.audio import router as audio_router
from app.api.v1.finetuning import router as finetuning_router
from app.api.v1.system import router as system_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lifespan hook - Database schema management is strictly handled by Alembic migrations
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, max_requests=500, window_seconds=60)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(conv_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(knowledge_router, prefix=settings.API_V1_STR)
app.include_router(tools_router, prefix=settings.API_V1_STR)
app.include_router(agents_router, prefix=settings.API_V1_STR)
app.include_router(eval_router, prefix=settings.API_V1_STR)
app.include_router(obs_router, prefix=settings.API_V1_STR)
app.include_router(mcp_router, prefix=settings.API_V1_STR)
app.include_router(ws_router, prefix=settings.API_V1_STR)
app.include_router(audio_router, prefix=settings.API_V1_STR)
app.include_router(finetuning_router, prefix=settings.API_V1_STR)
app.include_router(system_router, prefix=settings.API_V1_STR)
