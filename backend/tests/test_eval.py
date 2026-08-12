import pytest

@pytest.mark.asyncio
async def test_evaluation_suite_and_run(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "evaluser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "evaluser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Evaluation Suite
    create_res = await client.post(
        "/api/v1/evaluations/suites",
        headers=headers,
        json={
            "name": "General Knowledge Suite",
            "description": "Tests model accuracy on basic topics",
            "test_cases": [
                {"prompt": "Hello", "expected_output": "ForgeAI", "assertion_type": "contains"},
                {"prompt": "What is 2+2?", "expected_output": "4", "assertion_type": "contains"}
            ]
        }
    )
    assert create_res.status_code == 201
    suite_data = create_res.json()
    assert suite_data["name"] == "General Knowledge Suite"
    assert len(suite_data["test_cases"]) == 2
    suite_id = suite_data["id"]

    # 2. Run Evaluation Suite
    run_res = await client.post(
        f"/api/v1/evaluations/suites/{suite_id}/run",
        headers=headers,
        json={"model": "mock-v1", "provider": "mock"}
    )
    assert run_res.status_code == 200
    run_data = run_res.json()
    assert run_data["suite_id"] == suite_id
    assert run_data["total_count"] == 2
    assert "score" in run_data
    run_id = run_data["id"]

    # 3. Get Evaluation Run Result
    get_run_res = await client.get(f"/api/v1/evaluations/runs/{run_id}", headers=headers)
    assert get_run_res.status_code == 200
    assert get_run_res.json()["id"] == run_id

@pytest.mark.asyncio
async def test_observability_metrics(client):
    await client.post("/api/v1/auth/register", json={"email": "obsuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "obsuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Generate chat activity to create usage logs
    await client.post(
        "/api/v1/chat/completions",
        headers=headers,
        json={"message": "Obs test prompt", "provider": "mock"}
    )

    # Fetch Observability Metrics
    res = await client.get("/api/v1/observability/metrics", headers=headers)
    assert res.status_code == 200
    metrics = res.json()
    assert metrics["total_requests"] >= 1
    assert metrics["total_tokens"] > 0
    assert "mock" in metrics["provider_breakdown"]
