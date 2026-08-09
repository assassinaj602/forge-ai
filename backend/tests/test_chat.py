import pytest
import json

@pytest.mark.asyncio
async def test_conversation_crud(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "chatuser@example.com", "password": "password123"})
    login_res = await client.post("/api/v1/auth/login", data={"username": "chatuser@example.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Conversation
    create_res = await client.post(
        "/api/v1/conversations",
        headers=headers,
        json={"title": "AI Engineering", "system_prompt": "You are a senior engineer."}
    )
    assert create_res.status_code == 201
    conv_data = create_res.json()
    assert conv_data["title"] == "AI Engineering"
    assert conv_data["system_prompt"] == "You are a senior engineer."
    conv_id = conv_data["id"]

    # 2. Get Conversations List
    list_res = await client.get("/api/v1/conversations", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1
    assert list_res.json()[0]["id"] == conv_id

    # 3. Patch Conversation
    patch_res = await client.patch(
        f"/api/v1/conversations/{conv_id}",
        headers=headers,
        json={"title": "Updated AI Title"}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["title"] == "Updated AI Title"

    # 4. Delete Conversation
    del_res = await client.delete(f"/api/v1/conversations/{conv_id}", headers=headers)
    assert del_res.status_code == 204

    # 5. Verify 404 after deletion
    get_res = await client.get(f"/api/v1/conversations/{conv_id}", headers=headers)
    assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_chat_completions(client):
    await client.post("/api/v1/auth/register", json={"email": "chatuser2@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "chatuser2@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Send chat completion
    res = await client.post(
        "/api/v1/chat/completions",
        headers=headers,
        json={"message": "Explain vector search", "provider": "mock", "model": "mock-v1"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "conversation_id" in data
    assert "Explain vector search" in data["message"]["content"] or "Mock Assistant" in data["message"]["content"]
    assert data["message"]["role"] == "assistant"

@pytest.mark.asyncio
async def test_chat_streaming(client):
    await client.post("/api/v1/auth/register", json={"email": "streamuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "streamuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        "/api/v1/chat/stream",
        headers=headers,
        json={"message": "Stream this test", "provider": "mock", "model": "mock-v1"}
    )
    assert res.status_code == 200
    assert "text/event-stream" in res.headers["content-type"]

@pytest.mark.asyncio
async def test_structured_output(client):
    await client.post("/api/v1/auth/register", json={"email": "structuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "structuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        "/api/v1/chat/structured",
        headers=headers,
        json={"text": "Looking for a Python Developer with FastAPI and Postgres skills", "provider": "mock"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "role" in data["data"]
    assert "required_skills" in data["data"]
