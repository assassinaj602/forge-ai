from typing import List, Dict, Any, Optional
from app.services.vector.base import BaseVectorStore, BaseEmbeddingProvider
from app.services.llm.base import BaseLLMProvider, LLMMessage, LLMResponse

class RAGPipeline:
    def __init__(self, vector_store: BaseVectorStore, embedding_provider: BaseEmbeddingProvider):
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider

    async def retrieve_and_generate(
        self,
        query: str,
        user_id: str,
        llm_provider: BaseLLMProvider,
        collection_id: Optional[str] = None,
        top_k: int = 4,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Embed query
        query_vector = await self.embedding_provider.embed_query(query)

        # 2. Perform vector search
        search_results = await self.vector_store.search(
            query_vector=query_vector,
            user_id=user_id,
            collection_id=collection_id,
            top_k=top_k
        )

        if not search_results:
            # Fallback if no relevant documents retrieved
            res = await llm_provider.generate([LLMMessage(role="user", content=query)], model=model)
            return {
                "answer": res.content,
                "sources": [],
                "retrieved_chunks_count": 0
            }

        # 3. Construct Context & Citations
        context_parts = []
        sources = []
        for idx, res in enumerate(search_results):
            filename = res.metadata.get("filename", "document.pdf")
            page_num = res.metadata.get("page_number", 1)
            context_parts.append(f"Source [{idx+1}] ({filename}, Page {page_num}):\n{res.content}\n")
            sources.append({
                "source_id": idx + 1,
                "filename": filename,
                "page_number": page_num,
                "score": round(res.score, 4)
            })

        context_str = "\n".join(context_parts)
        system_instruction = (
            f"You are a Knowledge Assistant. Answer the user question using strictly the retrieved context below.\n"
            f"Always cite your sources inline (e.g. [1], [2]). Do NOT pretend you retrieved information that is missing.\n\n"
            f"Retrieved Context:\n{context_str}"
        )

        messages = [LLMMessage(role="user", content=query)]
        llm_response = await llm_provider.generate(messages=messages, system_prompt=system_instruction, model=model)

        return {
            "answer": llm_response.content,
            "sources": sources,
            "retrieved_chunks_count": len(search_results)
        }
