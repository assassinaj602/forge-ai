import pytest
import io

@pytest.mark.asyncio
async def test_knowledge_collection_crud(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "raguser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "raguser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Collection
    res = await client.post(
        "/api/v1/knowledge/collections",
        headers=headers,
        json={"name": "Machine Learning Notes", "description": "Lecture notes and papers"}
    )
    assert res.status_code == 201
    col_data = res.json()
    assert col_data["name"] == "Machine Learning Notes"
    assert "id" in col_data

    # 2. List Collections
    list_res = await client.get("/api/v1/knowledge/collections", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1
    assert list_res.json()[0]["name"] == "Machine Learning Notes"

@pytest.mark.asyncio
async def test_document_ingestion_and_rag_query(client):
    await client.post("/api/v1/auth/register", json={"email": "raguser2@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "raguser2@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Collection
    col_id = (await client.post(
        "/api/v1/knowledge/collections",
        headers=headers,
        json={"name": "Architecture Docs"}
    )).json()["id"]

    # Upload Text Document
    file_content = b"ForgeAI is an advanced production workspace using FastAPI, PostgreSQL, and RAG retrieval pipelines."
    files = {"file": ("architecture.txt", io.BytesIO(file_content), "text/plain")}

    upload_res = await client.post(
        f"/api/v1/knowledge/collections/{col_id}/documents",
        headers=headers,
        files=files
    )
    assert upload_res.status_code == 200
    doc_data = upload_res.json()
    assert doc_data["status"] == "ready"
    assert doc_data["chunk_count"] > 0

    # RAG Query with Citation Verification
    query_res = await client.post(
        "/api/v1/knowledge/query",
        headers=headers,
        json={"query": "What technologies does ForgeAI use?", "collection_id": col_id, "provider": "mock"}
    )
    assert query_res.status_code == 200
    q_data = query_res.json()
    assert "answer" in q_data
    assert q_data["retrieved_chunks_count"] > 0
    assert len(q_data["sources"]) > 0
    assert q_data["sources"][0]["filename"] == "architecture.txt"
