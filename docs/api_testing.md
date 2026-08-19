# ForgeAI API & Testing Guide

Comprehensive reference for testing ForgeAI endpoints via `curl` and automated scripts.

---

## 1. Authentication Endpoints

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@example.com",
    "password": "password123"
  }'
```

### Login & Obtain JWT Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=developer@example.com&password=password123"
```

---

## 2. Multi-Model Chat & SSE Streaming Endpoints

### Standard Synchronous Chat Completion
```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain vector search and semantic embeddings.",
    "provider": "mock",
    "model": "mock-v1"
  }'
```

### Multimodal Vision Chat Completion
```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze this architecture diagram image",
    "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "provider": "mock",
    "model": "mock-v1"
  }'
```

---

## 3. RAG Knowledge Collections

### Create Knowledge Collection
```bash
curl -X POST http://localhost:8000/api/v1/rag/collections \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering Docs",
    "description": "System architecture and guidelines"
  }'
```

---

## 4. ReAct Autonomous Agents

### Execute Agent Loop
```bash
curl -X POST http://localhost:8000/api/v1/agents/executest \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Calculate 42 * 10 and tell me the current datetime",
    "max_steps": 5
  }'
```
