import pytest
import base64
from app.services.audio.stt import AudioProcessingService

@pytest.mark.asyncio
async def test_audio_transcription_service():
    sample_bytes = b"fake_audio_wav_data_header_bytes_12345"
    sample_base64 = base64.b64encode(sample_bytes).decode("utf-8")
    
    res = await AudioProcessingService.transcribe_audio_base64(sample_base64, language="en")
    assert res["text"] != ""
    assert res["confidence"] > 0.90
    assert "audio-" in res["id"]

@pytest.mark.asyncio
async def test_audio_transcription_endpoint(client):
    # Register & Login User
    await client.post("/api/v1/auth/register", json={"email": "audiouser@example.com", "password": "password123"})
    token = (await client.post("/api/v1/auth/login", data={"username": "audiouser@example.com", "password": "password123"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    sample_bytes = b"fake_audio_wav_data_header_bytes_12345"
    sample_base64 = base64.b64encode(sample_bytes).decode("utf-8")

    res = await client.post(
        "/api/v1/audio/transcribe",
        headers=headers,
        json={"audio_base64": sample_base64, "language": "en"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "text" in data
    assert "confidence" in data
