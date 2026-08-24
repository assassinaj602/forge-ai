import pytest
from app.services.llm.compression import PromptCompressionService

def test_prompt_compression_service():
    long_prompt = "Please explain the concept of vector search in machine learning and why embeddings are important for artificial intelligence."
    res = PromptCompressionService.compress_prompt(long_prompt, target_ratio=0.5)
    assert "compressed_prompt" in res
    assert res["original_tokens"] > res["compressed_tokens"]
    assert res["tokens_saved"] > 0

@pytest.mark.asyncio
async def test_prompt_compression_endpoint(client):
    res = await client.post(
        "/api/v1/system/compress",
        json={"prompt": "This is a test prompt with extra unnecessary words that can be compressed.", "target_ratio": 0.5}
    )
    assert res.status_code == 200
    data = res.json()
    assert "compressed_prompt" in data

@pytest.mark.asyncio
async def test_system_export_endpoint(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "exportuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "exportuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.get("/api/v1/system/export", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "conversations" in data
    assert "knowledge_collections" in data
