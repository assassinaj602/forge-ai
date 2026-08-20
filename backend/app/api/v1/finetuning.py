"""
Fine-tuning Management Endpoints
"""
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import User
from app.db.models_finetuning import FineTuningJob
from app.api.deps import get_current_user

router = APIRouter(prefix="/finetuning", tags=["FineTuning"])

class FineTuningCreateRequest(BaseModel):
    model_name: str = "gpt-3.5-turbo"
    dataset_name: str
    epochs: int = 3
    batch_size: int = 4
    learning_rate: str = "2e-5"

@router.post("/jobs")
async def create_fine_tuning_job(
    req: FineTuningCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    job = FineTuningJob(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        model_name=req.model_name,
        dataset_name=req.dataset_name,
        epochs=req.epochs,
        batch_size=req.batch_size,
        learning_rate=req.learning_rate,
        status="training",
        metrics={"initial_loss": 2.45, "current_step": 1, "total_steps": 100}
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job

@router.get("/jobs")
async def list_fine_tuning_jobs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(FineTuningJob).where(FineTuningJob.user_id == current_user.id))
    return res.scalars().all()
