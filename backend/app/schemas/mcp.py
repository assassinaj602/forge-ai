from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class MCPServerBase(BaseModel):
    name: str
    server_url: str
    auth_header: Optional[str] = None
    is_active: bool = True

class MCPServerCreate(MCPServerBase):
    pass

class MCPServerResponse(MCPServerBase):
    id: str
    user_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MCPToolSchema(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = {}
