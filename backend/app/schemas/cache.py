from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CacheEntryBase(BaseModel):
    prompt: str
    response_content: str
    provider: str
    model: str

class CacheEntryCreate(CacheEntryBase):
    pass

class CacheEntryResponse(CacheEntryBase):
    id: str
    user_id: str
    hit_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
