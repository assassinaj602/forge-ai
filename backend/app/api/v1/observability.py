from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.db.models import User
from app.db.models_usage import UsageLog
from app.api.deps import get_current_user
from app.schemas.eval import ObservabilityMetricsResponse

router = APIRouter(prefix="/observability", tags=["Observability"])

from app.db.models_cache import SemanticCacheEntry

@router.get("/metrics", response_model=ObservabilityMetricsResponse)
async def get_observability_metrics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UsageLog)
        .where(UsageLog.user_id == current_user.id)
    )
    logs = result.scalars().all()

    # Query Cache Hits
    cache_result = await db.execute(
        select(func.sum(SemanticCacheEntry.hit_count))
        .where(SemanticCacheEntry.user_id == current_user.id)
    )
    total_cache_hits = cache_result.scalar() or 0

    total_requests = len(logs) + total_cache_hits
    total_prompt = sum(l.prompt_tokens for l in logs)
    total_completion = sum(l.completion_tokens for l in logs)
    total_tokens = sum(l.total_tokens for l in logs)
    total_cost = sum(l.estimated_cost for l in logs)
    avg_latency = (sum(l.latency_ms for l in logs) / len(logs)) if len(logs) > 0 else 0.0

    # Provider breakdown
    provider_breakdown = {}
    for l in logs:
        p = l.provider
        if p not in provider_breakdown:
            provider_breakdown[p] = {"requests": 0, "total_tokens": 0, "cost": 0.0}
        provider_breakdown[p]["requests"] += 1
        provider_breakdown[p]["total_tokens"] += l.total_tokens
        provider_breakdown[p]["cost"] += l.estimated_cost

    return ObservabilityMetricsResponse(
        total_requests=total_requests,
        total_prompt_tokens=total_prompt,
        total_completion_tokens=total_completion,
        total_tokens=total_tokens,
        total_estimated_cost_usd=round(total_cost, 6),
        avg_latency_ms=round(avg_latency, 2),
        provider_breakdown=provider_breakdown
    )
