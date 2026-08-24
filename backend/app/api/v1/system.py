"""
Prompt Compression & System Export Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.services.llm.compression import PromptCompressionService
from app.services.system.export import ExportBackupService

router = APIRouter(prefix="/system", tags=["System"])

class CompressPromptRequest(BaseModel):
    prompt: str
    target_ratio: float = 0.5

@router.post("/compress")
async def compress_prompt(req: CompressPromptRequest):
    return PromptCompressionService.compress_prompt(req.prompt, req.target_ratio)

@router.get("/export")
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ExportBackupService.export_user_data(db, current_user.id)
