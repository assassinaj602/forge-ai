import os
import hashlib
import httpx
from typing import List
from app.services.vector.base import BaseEmbeddingProvider

class MockEmbeddingProvider(BaseEmbeddingProvider):
    """Deterministic mock embedding provider generating 128-dim vectors from text hashes."""
    def __init__(self, dim: int = 128):
        self.dim = dim

    def _embed_single(self, text: str) -> List[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # Scale bytes to float range [-1, 1]
        raw_vec = [((b / 255.0) * 2.0) - 1.0 for b in digest]
        # Pad to target dimension
        while len(raw_vec) < self.dim:
            raw_vec.extend(raw_vec[:self.dim - len(raw_vec)])
        return raw_vec[:self.dim]

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [self._embed_single(t) for t in texts]

    async def embed_query(self, text: str) -> List[float]:
        return self._embed_single(text)

class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not self.api_key:
            return await MockEmbeddingProvider().embed_texts(texts)

        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.openai.com/v1/embeddings",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"input": texts, "model": self.model},
                timeout=30.0
            )
            res.raise_for_status()
            data = res.json()
            return [item["embedding"] for item in data["data"]]

    async def embed_query(self, text: str) -> List[float]:
        embeddings = await self.embed_texts([text])
        return embeddings[0]
