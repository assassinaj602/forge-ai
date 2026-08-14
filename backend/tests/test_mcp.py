import pytest

@pytest.mark.asyncio
async def test_mcp_server_crud_and_tool_sync(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "mcpuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "mcpuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create MCP Server Config
    create_res = await client.post(
        "/api/v1/mcp/servers",
        headers=headers,
        json={
            "name": "GitHub & DB Tools MCP Server",
            "server_url": "https://mcp.example.com",
            "auth_header": "Bearer mcp-secret-token-123"
        }
    )
    assert create_res.status_code == 201
    server_data = create_res.json()
    assert server_data["name"] == "GitHub & DB Tools MCP Server"
    server_id = server_data["id"]

    # 2. List MCP Servers
    list_res = await client.get("/api/v1/mcp/servers", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # 3. Sync MCP Tools into ToolRegistry
    sync_res = await client.post("/api/v1/mcp/sync", headers=headers)
    assert sync_res.status_code == 200
    sync_data = sync_res.json()
    assert sync_data["status"] == "success"
    assert "mcp_github_issues" in sync_data["registered_tools"]

    # 4. Verify synced MCP tools appear in global tool registry API
    tools_res = await client.get("/api/v1/tools", headers=headers)
    assert tools_res.status_code == 200
    registered_names = [t["name"] for t in tools_res.json()]
    assert "mcp_github_issues" in registered_names

    # 5. Delete MCP Server Config
    del_res = await client.delete(f"/api/v1/mcp/servers/{server_id}", headers=headers)
    assert del_res.status_code == 204
