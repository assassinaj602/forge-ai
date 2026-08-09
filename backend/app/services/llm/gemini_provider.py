import time
import os
import httpx
from typing import AsyncGenerator, List, Optional, Any
from app.services.llm.base import BaseLLMProvider, LLMMessage, LLMResponse

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")

    async def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        if not self.api_key:
            from app.services.llm.mock import MockLLMProvider
            return await MockLLMProvider().generate(messages, system_prompt, model or "gemini-1.5-flash", **kwargs)

        model_name = model or "gemini-1.5-flash"
        start_time = time.time()
        
        contents = []
        for m in messages:
            role = "user" if m.role in ["user", "system"] else "model"
            contents.append({"role": role, "parts": [{"text": m.content}]})

        async with httpx.AsyncClient() as client:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            res = await client.post(url, json={"contents": contents}, timeout=60.0)
            res.raise_for_status()
            data = res.json()

        latency_ms = int((time.time() - start_time) * 1000)
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        
        return LLMResponse(
            content=content,
            model=model_name,
            provider="gemini",
            prompt_tokens=len(str(messages)),
            completion_tokens=len(content),
            total_tokens=len(str(messages)) + len(content),
            latency_ms=latency_ms
        )

    async def stream_generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        if not self.api_key:
            from app.services.llm.mock import MockLLMProvider
            async for chunk in MockLLMProvider().stream_generate(messages, system_prompt, model, **kwargs):
                yield chunk
            return

        model_name = model or "gemini-1.5-flash"
        contents = []
        for m in messages:
            role = "user" if m.role in ["user", "system"] else "model"
            contents.append({"role": role, "parts": [{"text": m.content}]})

        async with httpx.AsyncClient() as client:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:streamGenerateContent?key={self.api_key}&alt=sse"
            async with client.stream("POST", url, json={"contents": contents}, timeout=60.0) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        import json
                        try:
                            payload = json.loads(line[6:])
                            text = payload["candidates"][0]["content"]["parts"][0]["text"]
                            if text:
                                yield text
                        except Exception:
                            continue
