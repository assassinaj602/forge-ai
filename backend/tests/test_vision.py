import pytest
from app.services.llm.vision_utils import validate_and_decode_base64_image

@pytest.mark.asyncio
async def test_multimodal_vision_chat_completion(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "visionuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "visionuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    sample_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

    # 1. Test Vision Utils validation helper
    valid, mime = validate_and_decode_base64_image(sample_base64)
    assert valid is True
    assert "image" in mime

    # 2. Test Multimodal Chat Completion with base64 image payload
    res = await client.post(
        "/api/v1/chat/completions",
        headers=headers,
        json={
            "message": "Analyze this architecture diagram",
            "image_base64": sample_base64,
            "provider": "mock",
            "model": "mock-v1"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert "[Multimodal Vision Analysis]" in data["message"]["content"]
    assert "Base64 Image Data" in data["message"]["content"]
