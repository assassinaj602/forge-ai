from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models_cache import SemanticCacheEntry
from app.services.vector.embeddings import MockEmbeddingProvider
import math

class SemanticCacheService:
    SIMILARITY_THRESHOLD = 0.90

    @staticmethod
    def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    @staticmethod
    async def get_cached_response(
        db: AsyncSession,
        user_id: str,
        prompt: str,
        provider: str,
        model: str
    ) -> Optional[SemanticCacheEntry]:
        result = await db.execute(
            select(SemanticCacheEntry)
            .where(
                SemanticCacheEntry.user_id == user_id,
                SemanticCacheEntry.provider == provider,
                SemanticCacheEntry.model == model
            )
        )
        entries = result.scalars().all()
        if not entries:
            return None

        embedder = MockEmbeddingProvider()
        query_vec = await embedder.embed_query(prompt)

        best_entry = None
        best_similarity = 0.0

        for entry in entries:
            entry_vec = await embedder.embed_query(entry.prompt)
            sim = SemanticCacheService._cosine_similarity(query_vec, entry_vec)
            if sim > best_similarity:
                best_similarity = sim
                best_entry = entry

        if best_entry and best_similarity >= SemanticCacheService.SIMILARITY_THRESHOLD:
            best_entry.hit_count += 1
            await db.commit()
            await db.refresh(best_entry)
            return best_entry

        return None

    @staticmethod
    async def cache_response(
        db: AsyncSession,
        user_id: str,
        prompt: str,
        response_content: str,
        provider: str,
        model: str
    ) -> SemanticCacheEntry:
        entry = SemanticCacheEntry(
            user_id=user_id,
            prompt=prompt,
            response_content=response_content,
            provider=provider,
            model=model
        )
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry
