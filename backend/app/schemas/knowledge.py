from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class CollectionCreate(CollectionBase):
    pass

class CollectionResponse(CollectionBase):
    id: str
    user_id: str
    created_at: datetime
    document_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class DocumentResponse(BaseModel):
    id: str
    collection_id: str
    user_id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    chunk_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RAGQueryRequest(BaseModel):
    query: str
    collection_id: Optional[str] = None
    provider: Optional[str] = "mock"
    model: Optional[str] = "mock-v1"
    top_k: Optional[int] = 4
