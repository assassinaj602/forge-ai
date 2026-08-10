import pytest

@pytest.mark.asyncio
async def test_list_tools(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "tooluser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "tooluser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.get("/api/v1/tools", headers=headers)
    assert res.status_code == 200
    tools = res.json()
    assert len(tools) >= 4
    tool_names = [t["name"] for t in tools]
    assert "calculator" in tool_names
    assert "current_datetime" in tool_names
    assert "web_search" in tool_names

@pytest.mark.asyncio
async def test_execute_calculator_tool(client):
    await client.post("/api/v1/auth/register", json={"email": "tooluser2@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "tooluser2@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        "/api/v1/tools/execute",
        headers=headers,
        json={"tool_name": "calculator", "arguments": {"expression": "25 * 4 + 50"}}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["result"]["result"] == 150

@pytest.mark.asyncio
async def test_execute_datetime_tool(client):
    await client.post("/api/v1/auth/register", json={"email": "tooluser3@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "tooluser3@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        "/api/v1/tools/execute",
        headers=headers,
        json={"tool_name": "current_datetime", "arguments": {"timezone_name": "UTC"}}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "iso_timestamp" in data["result"]

@pytest.mark.asyncio
async def test_chat_tool_calling_loop(client):
    await client.post("/api/v1/auth/register", json={"email": "tooluser4@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "tooluser4@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Query triggering calculator tool
    res = await client.post(
        "/api/v1/tools/chat",
        headers=headers,
        json={"message": "Please calculate 12 * 45 + 100", "provider": "mock"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "final_answer" in data
    assert len(data["tool_calls_executed"]) > 0
    assert data["tool_calls_executed"][0]["tool_name"] == "calculator"
    assert data["iterations"] == 2
