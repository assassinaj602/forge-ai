"""
Audio Speech-to-Text Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.db.models import User
from app.services.audio.stt import AudioProcessingService

router = APIRouter(prefix="/audio", tags=["Audio"])

class AudioTranscribeRequest(BaseModel):
    audio_base64: str
    language: str = "en"

@router.post("/transcribe")
async def transcribe_audio(
    req: AudioTranscribeRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        res = await AudioProcessingService.transcribe_audio_base64(req.audio_base64, req.language)
        return res
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
