import math
from typing import List, Optional
from app.services.vector.base import BaseVectorStore, VectorChunk, SearchResult

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

class MemoryVectorStore(BaseVectorStore):
    def __init__(self):
        self._chunks: List[VectorChunk] = []

    async def upsert(self, chunks: List[VectorChunk]) -> bool:
        for chunk in chunks:
            # Replace existing chunk if id exists
            self._chunks = [c for c in self._chunks if c.chunk_id != chunk.chunk_id]
            self._chunks.append(chunk)
        return True

    async def search(
        self,
        query_vector: List[float],
        user_id: str,
        collection_id: Optional[str] = None,
        top_k: int = 4
    ) -> List[SearchResult]:
        scored_results = []
        for chunk in self._chunks:
            # Enforce multi-tenant user_id and collection_id isolation filters
            if chunk.user_id != user_id:
                continue
            if collection_id and chunk.collection_id != collection_id:
                continue

            score = cosine_similarity(query_vector, chunk.vector)
            scored_results.append(
                SearchResult(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    content=chunk.content,
                    score=score,
                    metadata=chunk.metadata
                )
            )

        scored_results.sort(key=lambda x: x.score, reverse=True)
        return scored_results[:top_k]

    async def delete_document(self, document_id: str) -> bool:
        self._chunks = [c for c in self._chunks if c.document_id != document_id]
        return True

# Global singleton repository instance
global_vector_store = MemoryVectorStore()
