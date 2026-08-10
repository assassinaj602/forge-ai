from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.services.tools.base import BaseTool
from app.services.vector.memory_store import global_vector_store
from app.services.vector.embeddings import MockEmbeddingProvider

class DocumentSearchArgs(BaseModel):
    query: str = Field(..., description="Natural language search query to locate relevant knowledge documents")
    user_id: str = Field(..., description="Authenticated User ID")
    collection_id: Optional[str] = Field(None, description="Optional Knowledge Collection ID filter")
    top_k: Optional[int] = Field(3, description="Number of document chunks to retrieve")

class DocumentSearchTool(BaseTool):
    name = "document_search"
    description = "Searches uploaded user documents and knowledge bases for relevant text chunks."
    args_schema = DocumentSearchArgs

    async def execute(
        self,
        query: str,
        user_id: str,
        collection_id: Optional[str] = None,
        top_k: int = 3
    ) -> Dict[str, Any]:
        embedder = MockEmbeddingProvider()
        query_vector = await embedder.embed_query(query)
        results = await global_vector_store.search(
            query_vector=query_vector,
            user_id=user_id,
            collection_id=collection_id,
            top_k=top_k
        )
        
        matches = [
            {
                "chunk_id": r.chunk_id,
                "content": r.content,
                "score": round(r.score, 4),
                "metadata": r.metadata
            }
            for r in results
        ]
        return {"query": query, "matches_found": len(matches), "chunks": matches}
