from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ToolExecuteRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class ToolChatRequest(BaseModel):
    message: str
    provider: Optional[str] = "mock"
    model: Optional[str] = "mock-v1"
    system_prompt: Optional[str] = None
    enabled_tools: Optional[List[str]] = None
