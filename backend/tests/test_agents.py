import pytest

@pytest.mark.asyncio
async def test_agent_crud_and_execution(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "agentuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "agentuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Agent
    create_res = await client.post(
        "/api/v1/agents",
        headers=headers,
        json={
            "name": "Research Analyst",
            "description": "Analyzes market data and documents",
            "system_instructions": "You are a meticulous researcher.",
            "model": "mock-v1",
            "provider": "mock",
            "max_iterations": 5,
            "tools": ["calculator", "current_datetime"]
        }
    )
    assert create_res.status_code == 201
    agent_data = create_res.json()
    assert agent_data["name"] == "Research Analyst"
    assert agent_data["max_iterations"] == 5
    agent_id = agent_data["id"]

    # 2. List Agents
    list_res = await client.get("/api/v1/agents", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # 3. Execute Agent Task (Tool-enabled ReAct loop)
    exec_res = await client.post(
        f"/api/v1/agents/{agent_id}/execute",
        headers=headers,
        json={"task": "Please calculate 12 * 45 + 100 and report the date."}
    )
    assert exec_res.status_code == 200
    exec_data = exec_res.json()
    assert exec_data["status"] == "completed"
    assert exec_data["iteration_count"] > 0
    assert len(exec_data["steps_log"]) > 0
    execution_id = exec_data["id"]

    # 4. Fetch Execution Trace Observability
    trace_res = await client.get(f"/api/v1/agents/executions/{execution_id}", headers=headers)
    assert trace_res.status_code == 200
    assert trace_res.json()["id"] == execution_id

    # 5. Delete Agent
    del_res = await client.delete(f"/api/v1/agents/{agent_id}", headers=headers)
    assert del_res.status_code == 204
