from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List, Optional
from pydantic import BaseModel

class LLMMessage(BaseModel):
    role: str  # user, assistant, system, tool
    content: str

class LLMResponse(BaseModel):
    content: str
    model: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: int = 0

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        pass

    @abstractmethod
    async def stream_generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        pass
