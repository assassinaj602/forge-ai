import pytest

@pytest.mark.asyncio
async def test_semantic_prompt_caching_and_hit(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "cacheuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "cacheuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    prompt_text = "What is vector search in machine learning?"

    # 1. First Call: Cache Miss (invokes LLM, caches response)
    res1 = await client.post(
        "/api/v1/chat/completions",
        headers=headers,
        json={"message": prompt_text, "provider": "mock", "model": "mock-v1"}
    )
    assert res1.status_code == 200
    data1 = res1.json()
    assert "cached" not in data1 or data1.get("cached") is False

    # 2. Second Call: Cache Hit (semantically identical prompt)
    res2 = await client.post(
        "/api/v1/chat/completions",
        headers=headers,
        json={"message": prompt_text, "provider": "mock", "model": "mock-v1"}
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2.get("cached") is True
    assert "[Cached Response]" in data2["message"]["content"]
    assert data2["usage"]["total_tokens"] == 0
    assert data2["latency_ms"] == 5

    # 3. Observability Metrics shows cache activity
    obs_res = await client.get("/api/v1/observability/metrics", headers=headers)
    assert obs_res.status_code == 200
    metrics = obs_res.json()
    assert metrics["total_requests"] >= 2
