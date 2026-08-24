# ForgeAI — Enterprise AI Engineering Workspace

![CI/CD Pipeline Status](https://github.com/assassinaj602/forge-ai/actions/workflows/ci.yml/badge.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

ForgeAI is a production-grade AI Engineering workspace featuring FastAPI, PostgreSQL, JWT Authentication, Multi-tenant Data Isolation, Alembic Migrations, Docker containerization, SSE Streaming, RAG Vector Search, ReAct Autonomous Agents, Model Context Protocol (MCP), Semantic Cache, and Multimodal Vision.

---

## 🌟 Enterprise Feature Matrix

| Feature Module | Technical Highlights | Status |
|---|---|---|
| **Auth & Security** | JWT (HS256), Password Hashing (`bcrypt`), Multi-Tenant Row Isolation | ✅ Production |
| **Multi-Model LLM Engine** | Unified Provider Abstraction (OpenAI, Anthropic, Mock), SSE Token Streaming | ✅ Production |
| **RAG Knowledge Engine** | Document Ingestion (PDF/TXT), Semantic Vector Search & Cosine Scoring | ✅ Production |
| **Tool Calling Framework** | Dynamic Registry, Extensible Custom Tools (`calculator`, `datetime`) | ✅ Production |
| **ReAct Autonomous Agents** | Multi-step Thought-Action-Observation Loop, Iteration Limit Safeguards | ✅ Production |
| **AI Evaluation & Metrics** | Multi-Assertion Evaluators, Token/Cost Usage Logs, Real-time Dashboard | ✅ Production |
| **Full Stack Dashboard** | Glassmorphism SPA (Vanilla JS + Custom CSS), Docker + Nginx Packaging | ✅ Production |
| **Model Context Protocol** | Native MCP Client, MCP Tool Adapter, Stdio & SSE JSON-RPC Transport | ✅ Production |
| **Semantic Prompt Cache** | Prompt Similarity Lookup (<10ms latency, $0 LLM cost) | ✅ Production |
| **Multimodal Vision** | GPT-4 Vision & Base64/URL Image Analysis Support | ✅ Production |
| **CI/CD Pipeline** | GitHub Actions Workflow (`pytest`, Alembic dry-run, Docker build, `pip-audit`) | ✅ Production |
| **Architecture Visualizations**| Complete Mermaid sequence, state, flowchart, and component diagrams | ✅ Production |

---

## 📚 Comprehensive Documentation Index

- [Architecture & Diagrams](docs/architecture.md): Sequence diagrams, ReAct state machines, and system flowcharts.
- [API Reference & Testing Guide](docs/api_testing.md): Complete `curl` request examples for every endpoint module.
- [Deployment & Setup Guide](docs/deployment.md): Docker Compose, environment configuration, and production Nginx packaging.

---

## 🚀 Quickstart & Installation

### Option 1: Docker Compose (Recommended)

1. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```
2. Launch services:
   ```bash
   docker compose up --build -d
   ```
3. Access points:
   - **Frontend UI**: `http://localhost:80`
   - **Backend API**: `http://localhost:8000`
   - **Swagger Docs**: `http://localhost:8000/docs`

---

## 🧪 Local Test Verification

Execute the local CI test suite runner:
```bash
python scripts/test_ci_locally.py
```

---

## 📜 Roadmap Progress
- [x] Milestone 1: Authentication Core, Alembic Migrations, Docker & Tenant Isolation
- [x] Milestone 2: Multi-Model AI Chat & Streaming Engine
- [x] Milestone 3: Document Processing & RAG Knowledge Engine
- [x] Milestone 4: Tool Calling & Dynamic Tool Framework
- [x] Milestone 5: Autonomous AI Agents Framework
- [x] Milestone 6: AI Evaluation, Observability & Cost Tracking
- [x] Milestone 7: Full Stack UI Dashboard & Production Packaging
- [x] Milestone 8: Model Context Protocol (MCP) Integration
- [x] Milestone 9: Semantic Prompt Caching Engine
- [x] Milestone 10: Multimodal Vision & Image Understanding
- [x] Milestone 11: GitHub Actions CI/CD Pipeline
- [x] Milestone 12: Architectural Visualizations & Complete System Documentation Polish
- [x] Milestone 13: Advanced Features Engine (WebSocket Real-time Streaming, Speech-to-Text Audio, Fine-Tuning Management, Redis Cache Abstraction)
- [x] Milestone 14: Rate Limiting Middleware, Text-to-Speech Synthesis, and OAuth2 Social Authentication
- [x] Milestone 15: Prompt Compression Engine & System Data Export/Backup Service
