import asyncio
import time
from typing import AsyncGenerator, List, Optional, Any
from app.services.llm.base import BaseLLMProvider, LLMMessage, LLMResponse

class MockLLMProvider(BaseLLMProvider):
    async def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        start_time = time.time()
        last_message = messages[-1].content if messages else "Hello"
        
        # Simple intelligent mock response generator
        response_text = f"ForgeAI Mock Assistant: Received your message '{last_message}'. Model: {model or 'mock-v1'}."
        latency_ms = int((time.time() - start_time) * 1000)
        
        prompt_tokens = sum(len(m.content.split()) for m in messages)
        completion_tokens = len(response_text.split())
        
        return LLMResponse(
            content=response_text,
            model=model or "mock-v1",
            provider="mock",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            latency_ms=latency_ms
        )

    async def stream_generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        last_message = messages[-1].content if messages else "Hello"
        response_text = f"ForgeAI Mock Assistant: Streaming response for '{last_message}'."
        words = response_text.split()
        
        for word in words:
            yield word + " "
            await asyncio.sleep(0.05)
