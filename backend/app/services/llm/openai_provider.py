import time
import os
import httpx
from typing import AsyncGenerator, List, Optional, Any
from app.services.llm.base import BaseLLMProvider, LLMMessage, LLMResponse

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1"

    async def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> LLMResponse:
        if not self.api_key:
            # Fallback to mock behavior if no API key provided
            from app.services.llm.mock import MockLLMProvider
            return await MockLLMProvider().generate(messages, system_prompt, model or "gpt-4o-mini", **kwargs)

        model_name = model or "gpt-4o-mini"
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            if m.image_url or m.image_base64:
                content_parts = [{"type": "text", "text": m.content}]
                img_src = m.image_url if m.image_url else f"data:image/jpeg;base64,{m.image_base64}"
                content_parts.append({"type": "image_url", "image_url": {"url": img_src}})
                formatted_messages.append({"role": m.role, "content": content_parts})
            else:
                formatted_messages.append({"role": m.role, "content": m.content})

        start_time = time.time()
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": model_name, "messages": formatted_messages, **kwargs},
                timeout=60.0
            )
            res.raise_for_status()
            data = res.json()

        latency_ms = int((time.time() - start_time) * 1000)
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        return LLMResponse(
            content=content,
            model=model_name,
            provider="openai",
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
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

        model_name = model or "gpt-4o-mini"
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            formatted_messages.append({"role": m.role, "content": m.content})

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": model_name, "messages": formatted_messages, "stream": True, **kwargs},
                timeout=60.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and not line.endswith("[DONE]"):
                        import json
                        try:
                            payload = json.loads(line[6:])
                            delta = payload["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield delta
                        except Exception:
                            continue
