import pytest

@pytest.mark.asyncio
async def test_fine_tuning_job_crud(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "ftuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "ftuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Fine Tuning Job
    res1 = await client.post(
        "/api/v1/finetuning/jobs",
        headers=headers,
        json={
            "model_name": "gpt-3.5-turbo",
            "dataset_name": "customer_support_v1.jsonl",
            "epochs": 4,
            "batch_size": 8
        }
    )
    assert res1.status_code == 200
    job_data = res1.json()
    assert job_data["status"] == "training"
    assert job_data["dataset_name"] == "customer_support_v1.jsonl"

    # 2. List Fine Tuning Jobs
    res2 = await client.get("/api/v1/finetuning/jobs", headers=headers)
    assert res2.status_code == 200
    jobs = res2.json()
    assert len(jobs) >= 1
