# Architecture Documentation — ForgeAI Enterprise Platform

This document details the core subsystem sequence workflows, architectural component layouts, and data execution flows for **ForgeAI**.

---

## 1. Multi-Model LLM Streaming & SSE Engine Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as Client Application (SPA UI)
    participant API as FastAPI Router (/api/v1/chat/stream)
    participant Cache as Semantic Cache Service
    participant Factory as LLM Provider Factory
    participant Provider as OpenAI / Anthropic / Mock Provider
    participant SSE as Server-Sent Events Engine
    participant DB as Async Database (PostgreSQL)

    User->>API: POST /api/v1/chat/stream (prompt, provider, model)
    API->>DB: Fetch or create Conversation context
    API->>Cache: Lookup prompt embedding in vector cache
    alt Cache Hit (similarity >= threshold)
        Cache-->>API: Return cached response string
        API->>SSE: Stream cached response tokens via SSE
        SSE-->>User: event: message (cached tokens)
        SSE-->>User: event: end [DONE]
    else Cache Miss
        API->>Factory: Get provider instance (provider_name)
        Factory-->>API: Return LLMProvider instance
        API->>Provider: generate_stream(history, system_prompt)
        loop Token Generation Stream
            Provider-->>SSE: Yield token chunk
            SSE-->>User: event: message {content: token}
        end
        API->>DB: Save complete Assistant Message & UsageLog
        API->>Cache: Store (prompt, response) in SemanticCacheEntries
        SSE-->>User: event: end [DONE]
    end
```

---

## 2. RAG Knowledge & Vector Search Pipeline Workflow

```mermaid
graph TD
    subgraph Ingestion["1. Document Ingestion Pipeline"]
        A[User Uploads PDF/TXT File] --> B[RAG Service Document Processor]
        B --> C[Chunking Engine: 500 Tokens / 50 Overlap]
        C --> D[Embedding Generator: Mock/OpenAI Embeddings]
        D --> E[(Vector Knowledge Collection)]
    end

    subgraph Retrieval["2. Query Retrieval & Context Augmentation"]
        F[User Query Prompt] --> G[Generate Query Embedding Vector]
        G --> H[Cosine Similarity Search against Collection]
        H --> I[Extract Top-K Most Relevant Chunks]
        I --> J[Construct System Prompt with Injected RAG Context]
        J --> K[LLM Provider Generation Endpoint]
    end

---

## 3. Vector Database Storage Abstraction

```mermaid
classDiagram
    class KnowledgeCollection {
        +String id
        +String user_id
        +String name
        +String description
        +List~DocumentChunk~ chunks
    }
    class DocumentChunk {
        +String id
        +String collection_id
        +String content
        +List~float~ embedding
        +Dict metadata
    }
    class RAGService {
        +create_collection(name, user_id)
        +ingest_document(collection_id, file_content)
        +query_similar_chunks(collection_id, query_text, top_k)
    }

    RAGService --> KnowledgeCollection : Manages
    KnowledgeCollection "1" *-- "many" DocumentChunk : Contains
```

---

## 4. ReAct Autonomous Agent Loop State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle: Agent Initialized
    Idle --> Reason: Execution Triggered (Goal Prompt)
    
    state ReAct_Iteration_Loop {
        Reason --> Action: Formulate Thought & Pick Tool Call
        Action --> Observe: Execute Registered Tool
        Observe --> SafeguardCheck: Check Iteration Count (< max_steps)
        SafeguardCheck --> Reason: Continue Reasoning (< max_steps)
    }

    SafeguardCheck --> Terminated: Exceeded Safeguard Max Steps
    Reason --> Completed: Final Answer Produced
    Completed --> [*]
    Terminated --> [*]
```

---

## 5. Semantic Prompt Caching & Similarity Lookup Engine

```mermaid
flowchart TD
    In[Incoming User Prompt] --> Hash[Generate SHA256 & Embedding Vector]
    Hash --> Lookup[Query SemanticCacheEntries for (user_id, provider, model)]
    Lookup --> Compare{Similarity Score >= Threshold (0.92)?}
    Compare -- Yes (Cache Hit) --> HitReturn[Return Cached Response (<10ms Latency, $0 LLM Cost)]
    Compare -- No (Cache Miss) --> LLM[Invoke External LLM Provider]
    LLM --> StoreCache[Store Prompt + Response + Embedding in DB]
    StoreCache --> OutReturn[Return Fresh LLM Response to User]
```
```
