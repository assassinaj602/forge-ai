from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db.models import User
from app.db.models_agent import Agent, AgentExecution
from app.api.deps import get_current_user
from app.schemas.agent import (
    AgentCreate, AgentUpdate, AgentResponse, AgentExecuteRequest, AgentExecutionResponse
)
from app.services.agents.runner import AgentRunner

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("", response_model=List[AgentResponse])
async def list_agents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Agent)
        .where(Agent.user_id == current_user.id)
        .order_by(Agent.created_at.desc())
    )
    return result.scalars().all()

@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_in: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    agent = Agent(
        user_id=current_user.id,
        name=agent_in.name,
        description=agent_in.description,
        system_instructions=agent_in.system_instructions,
        model=agent_in.model,
        provider=agent_in.provider,
        max_iterations=agent_in.max_iterations,
        temperature=agent_in.temperature,
        tools=agent_in.tools
    )
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Agent)
        .where(Agent.id == agent_id, Agent.user_id == current_user.id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_in: AgentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Agent)
        .where(Agent.id == agent_id, Agent.user_id == current_user.id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if agent_in.name is not None:
        agent.name = agent_in.name
    if agent_in.description is not None:
        agent.description = agent_in.description
    if agent_in.system_instructions is not None:
        agent.system_instructions = agent_in.system_instructions
    if agent_in.model is not None:
        agent.model = agent_in.model
    if agent_in.provider is not None:
        agent.provider = agent_in.provider
    if agent_in.max_iterations is not None:
        agent.max_iterations = agent_in.max_iterations
    if agent_in.temperature is not None:
        agent.temperature = agent_in.temperature
    if agent_in.tools is not None:
        agent.tools = agent_in.tools

    await db.commit()
    await db.refresh(agent)
    return agent

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Agent)
        .where(Agent.id == agent_id, Agent.user_id == current_user.id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    await db.delete(agent)
    await db.commit()
    return None

@router.post("/{agent_id}/execute", response_model=AgentExecutionResponse)
async def execute_agent_task(
    agent_id: str,
    req: AgentExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Agent)
        .where(Agent.id == agent_id, Agent.user_id == current_user.id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    execution = AgentExecution(
        agent_id=agent.id,
        user_id=current_user.id,
        task=req.task,
        status="running"
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)

    # Run Autonomous ReAct Execution Loop
    completed_execution = await AgentRunner.run(agent, req.task, execution, db)
    return completed_execution

@router.get("/executions/{execution_id}", response_model=AgentExecutionResponse)
async def get_agent_execution_trace(
    execution_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AgentExecution)
        .where(AgentExecution.id == execution_id, AgentExecution.user_id == current_user.id)
    )
    execution = result.scalar_one_or_none()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution trace not found")
    return execution
