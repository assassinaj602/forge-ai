import pytest
from app.services.audio.tts import TTSService

@pytest.mark.asyncio
async def test_tts_service():
    res = await TTSService.generate_speech("Hello world speech synthesis", voice="alloy")
    assert "audio_base64" in res
    assert res["character_count"] == len("Hello world speech synthesis")

@pytest.mark.asyncio
async def test_tts_endpoint(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "ttsuser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "ttsuser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        "/api/v1/audio/speech",
        headers=headers,
        json={"text": "Synthesize this speech", "voice": "echo", "format": "mp3"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "audio_base64" in data
    assert data["voice"] == "echo"

@pytest.mark.asyncio
async def test_oauth_social_login(client):
    res = await client.post(
        "/api/v1/auth/oauth/social",
        json={"provider": "google", "access_token": "ya29.simulated_oauth_token_123"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
