import pytest
from datetime import timedelta

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "project": "ForgeAI Workspace"}

@pytest.mark.asyncio
async def test_register_user_success(client):
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
async def test_register_user_duplicate(client):
    # First registration
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "password123"}
    )
    # Duplicate registration
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_invalid_input(client):
    # Invalid email
    res1 = await client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": "password123"}
    )
    assert res1.status_code == 422

    # Password too short (< 8 chars)
    res2 = await client.post(
        "/api/v1/auth/register",
        json={"email": "shortpass@example.com", "password": "short"}
    )
    assert res2.status_code == 422

@pytest.mark.asyncio
async def test_login_success(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "bob@example.com", "password": "securepassword"}
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "bob@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_incorrect_password(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "bob2@example.com", "password": "securepassword"}
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "bob2@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "nobody@example.com", "password": "somepassword"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_missing_authorization_header(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_invalid_jwt_token(client):
    response = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid.jwt.token"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_expired_jwt_token(client):
    from app.core.security import create_access_token
    expired_token = create_access_token(subject="some-user-id", expires_delta=timedelta(seconds=-10))
    response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_inactive_user(client, db_session):
    from app.db.models import User
    from app.core.security import create_access_token, get_password_hash
    
    # Create inactive user directly
    user = User(
        email="inactive@example.com",
        hashed_password=get_password_hash("password123"),
        is_active=False
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = create_access_token(subject=user.id)
    response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert "inactive" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_cross_user_tenant_isolation(client, db_session):
    from app.db.models import Conversation, Message
    
    # Register User 1
    u1 = await client.post(
        "/api/v1/auth/register",
        json={"email": "user1@example.com", "password": "password123"}
    )
    token1 = (await client.post(
        "/api/v1/auth/login",
        data={"username": "user1@example.com", "password": "password123"}
    )).json()["access_token"]
    user1_id = u1.json()["id"]

    # Register User 2
    u2 = await client.post(
        "/api/v1/auth/register",
        json={"email": "user2@example.com", "password": "password123"}
    )
    token2 = (await client.post(
        "/api/v1/auth/login",
        data={"username": "user2@example.com", "password": "password123"}
    )).json()["access_token"]
    user2_id = u2.json()["id"]

    # Seed conversation for User 1
    conv1 = Conversation(user_id=user1_id, title="User 1 Secret Chat")
    db_session.add(conv1)
    await db_session.commit()
    await db_session.refresh(conv1)

    # Verify profile isolation
    me1 = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token1}"})
    me2 = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token2}"})
    assert me1.json()["id"] == user1_id
    assert me2.json()["id"] == user2_id
    assert me1.json()["id"] != me2.json()["id"]
