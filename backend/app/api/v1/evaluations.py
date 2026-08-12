from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db.models import User
from app.db.models_eval import EvalSuite, EvalTestCase, EvalRun
from app.api.deps import get_current_user
from app.schemas.eval import (
    SuiteCreate, SuiteResponse, TestCaseCreate, TestCaseResponse, EvalRunRequest, EvalRunResponse
)
from app.services.eval.runner import EvalRunner

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])

@router.get("/suites", response_model=List[SuiteResponse])
async def list_suites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(EvalSuite)
        .where(EvalSuite.user_id == current_user.id)
        .options(selectinload(EvalSuite.test_cases))
        .order_by(EvalSuite.created_at.desc())
    )
    return result.scalars().all()

@router.post("/suites", response_model=SuiteResponse, status_code=status.HTTP_201_CREATED)
async def create_suite(
    suite_in: SuiteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    suite = EvalSuite(
        user_id=current_user.id,
        name=suite_in.name,
        description=suite_in.description
    )
    db.add(suite)
    await db.commit()
    await db.refresh(suite)

    for tc_in in suite_in.test_cases:
        tc = EvalTestCase(
            suite_id=suite.id,
            prompt=tc_in.prompt,
            expected_output=tc_in.expected_output,
            assertion_type=tc_in.assertion_type
        )
        db.add(tc)
    
    await db.commit()

    result = await db.execute(
        select(EvalSuite)
        .where(EvalSuite.id == suite.id)
        .options(selectinload(EvalSuite.test_cases))
    )
    return result.scalar_one()

@router.post("/suites/{suite_id}/run", response_model=EvalRunResponse)
async def run_suite_evaluation(
    suite_id: str,
    req: EvalRunRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(EvalSuite)
        .where(EvalSuite.id == suite_id, EvalSuite.user_id == current_user.id)
        .options(selectinload(EvalSuite.test_cases))
    )
    suite = result.scalar_one_or_none()
    if not suite:
        raise HTTPException(status_code=404, detail="Evaluation Suite not found")

    eval_run = await EvalRunner.run_suite(
        suite=suite,
        test_cases=suite.test_cases,
        model=req.model or "mock-v1",
        provider_name=req.provider or "mock",
        user_id=current_user.id
    )
    db.add(eval_run)
    await db.commit()
    await db.refresh(eval_run)
    return eval_run

@router.get("/runs/{run_id}", response_model=EvalRunResponse)
async def get_eval_run_result(
    run_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(EvalRun)
        .where(EvalRun.id == run_id, EvalRun.user_id == current_user.id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation Run not found")
    return run
