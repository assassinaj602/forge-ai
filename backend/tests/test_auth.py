import pytest

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "project": "ForgeAI Workspace"}

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "password123", "full_name": "Alice Developer"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["full_name"] == "Alice Developer"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_user(client):
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={"email": "bob@example.com", "password": "securepassword", "full_name": "Bob Builder"}
    )
    
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "bob@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_user_tenant_isolation(client):
    # Register User 1
    await client.post(
        "/api/v1/auth/register",
        json={"email": "user1@example.com", "password": "passuser1", "full_name": "User One"}
    )
    res1 = await client.post(
        "/api/v1/auth/login",
        data={"username": "user1@example.com", "password": "passuser1"}
    )
    token1 = res1.json()["access_token"]

    # Register User 2
    await client.post(
        "/api/v1/auth/register",
        json={"email": "user2@example.com", "password": "passuser2", "full_name": "User Two"}
    )
    res2 = await client.post(
        "/api/v1/auth/login",
        data={"username": "user2@example.com", "password": "passuser2"}
    )
    token2 = res2.json()["access_token"]

    # Access /me with User 1 token
    me1 = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token1}"})
    assert me1.status_code == 200
    assert me1.json()["email"] == "user1@example.com"

    # Access /me with User 2 token
    me2 = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token2}"})
    assert me2.status_code == 200
    assert me2.json()["email"] == "user2@example.com"
    assert me1.json()["id"] != me2.json()["id"]
