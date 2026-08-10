import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db.models import User
from app.db.models_rag import KnowledgeCollection, Document, DocumentChunk
from app.api.deps import get_current_user
from app.schemas.knowledge import CollectionCreate, CollectionResponse, DocumentResponse, RAGQueryRequest
from app.services.rag.chunker import DocumentChunker
from app.services.vector.embeddings import MockEmbeddingProvider
from app.services.vector.memory_store import global_vector_store, VectorChunk
from app.services.vector.base import VectorChunk
from app.services.rag.rag_service import RAGPipeline
from app.services.llm.factory import get_llm_provider

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

@router.get("/collections", response_model=List[CollectionResponse])
async def list_collections(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(KnowledgeCollection)
        .where(KnowledgeCollection.user_id == current_user.id)
        .options(selectinload(KnowledgeCollection.documents))
        .order_by(KnowledgeCollection.created_at.desc())
    )
    cols = result.scalars().all()
    out = []
    for c in cols:
        res = CollectionResponse.model_validate(c)
        res.document_count = len(c.documents)
        out.append(res)
    return out

@router.post("/collections", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(
    col_in: CollectionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    collection = KnowledgeCollection(
        user_id=current_user.id,
        name=col_in.name,
        description=col_in.description
    )
    db.add(collection)
    await db.commit()
    await db.refresh(collection)
    return collection

@router.post("/collections/{collection_id}/documents", response_model=DocumentResponse)
async def upload_document(
    collection_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify collection ownership
    res = await db.execute(
        select(KnowledgeCollection)
        .where(KnowledgeCollection.id == collection_id, KnowledgeCollection.user_id == current_user.id)
    )
    col = res.scalar_one_or_none()
    if not col:
        raise HTTPException(status_code=404, detail="Collection not found")

    file_bytes = await file.read()
    file_type = file.filename.split(".")[-1].lower()
    if file_type not in ["pdf", "txt", "md"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Supported: pdf, txt, md")

    doc = Document(
        collection_id=col.id,
        user_id=current_user.id,
        filename=file.filename,
        file_type=file_type,
        file_size=len(file_bytes),
        status="processing"
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    # Ingestion Pipeline
    try:
        pages = DocumentChunker.extract_text(file_bytes, file_type)
        raw_chunks = DocumentChunker.split_text_with_overlap(pages)

        doc_chunks = []
        vector_chunks = []
        embedder = MockEmbeddingProvider()

        texts = [c["content"] for c in raw_chunks]
        embeddings = await embedder.embed_texts(texts)

        for idx, c in enumerate(raw_chunks):
            chunk_id = str(uuid.uuid4())
            d_chunk = DocumentChunk(
                id=chunk_id,
                document_id=doc.id,
                chunk_index=c["chunk_index"],
                content=c["content"],
                page_number=c["page_number"]
            )
            doc_chunks.append(d_chunk)

            vector_chunks.append(
                VectorChunk(
                    chunk_id=chunk_id,
                    document_id=doc.id,
                    collection_id=col.id,
                    user_id=current_user.id,
                    content=c["content"],
                    vector=embeddings[idx],
                    metadata={"filename": file.filename, "page_number": c["page_number"]}
                )
            )

        db.add_all(doc_chunks)
        await global_vector_store.upsert(vector_chunks)

        doc.status = "ready"
        doc.chunk_count = len(doc_chunks)
        await db.commit()
        await db.refresh(doc)
        return doc
    except Exception as e:
        doc.status = "failed"
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")

@router.post("/query")
async def query_knowledge(
    req: RAGQueryRequest,
    current_user: User = Depends(get_current_user)
):
    embedder = MockEmbeddingProvider()
    pipeline = RAGPipeline(vector_store=global_vector_store, embedding_provider=embedder)
    llm_provider = get_llm_provider(req.provider)

    result = await pipeline.retrieve_and_generate(
        query=req.query,
        user_id=current_user.id,
        llm_provider=llm_provider,
        collection_id=req.collection_id,
        top_k=req.top_k or 4,
        model=req.model or "mock-v1"
    )
    return result
