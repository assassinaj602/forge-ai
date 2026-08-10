from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class VectorChunk(BaseModel):
    chunk_id: str
    document_id: str
    collection_id: str
    user_id: str
    content: str
    vector: List[float]
    metadata: Dict[str, Any] = {}

class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = {}

class BaseVectorStore(ABC):
    @abstractmethod
    async def upsert(self, chunks: List[VectorChunk]) -> bool:
        pass

    @abstractmethod
    async def search(
        self,
        query_vector: List[float],
        user_id: str,
        collection_id: Optional[str] = None,
        top_k: int = 4
    ) -> List[SearchResult]:
        pass

    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        pass

class BaseEmbeddingProvider(ABC):
    @abstractmethod
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        pass

    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        pass
