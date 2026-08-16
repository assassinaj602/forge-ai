from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ConversationBase(BaseModel):
    title: str = "New Conversation"
    system_prompt: Optional[str] = None
    model: str = "gpt-4o-mini"
    provider: str = "openai"

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    system_prompt: Optional[str] = None

class MessageSchema(BaseModel):
    id: str
    role: str
    content: str
    tokens_used: int
    latency_ms: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ConversationResponse(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageSchema] = []

    model_config = ConfigDict(from_attributes=True)

class ChatMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    provider: Optional[str] = "mock"
    model: Optional[str] = "mock-v1"
    system_prompt: Optional[str] = None

class StructuredAnalysisRequest(BaseModel):
    text: str
    provider: Optional[str] = "mock"
    model: Optional[str] = "mock-v1"
