from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    system_instructions: str
    model: str = "gpt-4o-mini"
    provider: str = "mock"
    max_iterations: int = Field(5, ge=1, le=20)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    tools: List[str] = []

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    system_instructions: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    max_iterations: Optional[int] = Field(None, ge=1, le=20)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    tools: Optional[List[str]] = None

class AgentResponse(AgentBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AgentExecuteRequest(BaseModel):
    task: str

class AgentStepTrace(BaseModel):
    step: int
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[Any] = None

class AgentExecutionResponse(BaseModel):
    id: str
    agent_id: str
    user_id: str
    task: str
    status: str
    final_answer: Optional[str] = None
    iteration_count: int
    steps_log: List[Dict[str, Any]] = []
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
