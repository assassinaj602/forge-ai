import asyncio
import time
from typing import AsyncGenerator, List, Optional, Any, Dict
from app.services.llm.base import BaseLLMProvider, LLMMessage, LLMResponse

class MockLLMProvider(BaseLLMProvider):
    async def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> LLMResponse:
        start_time = time.time()
        last_message = messages[-1].content if messages else "Hello"
        last_message_lower = last_message.lower()

        tool_calls = None
        # Smart tool call intent detection (check if tool result is not already in history)
        has_tool_result = any("Action: " in m.content for m in messages if m.content)
        
        if tools and not has_tool_result:
            tool_names = [t.get("function", {}).get("name") for t in tools if isinstance(t, dict)]
            if ("calculate" in last_message_lower or "+" in last_message_lower or "*" in last_message_lower) and "calculator" in tool_names:
                tool_calls = [{
                    "id": "call_calc_01",
                    "name": "calculator",
                    "arguments": {"expression": "12 * 45 + 100"}
                }]
            elif ("time" in last_message_lower or "date" in last_message_lower) and "current_datetime" in tool_names:
                tool_calls = [{
                    "id": "call_time_01",
                    "name": "current_datetime",
                    "arguments": {"timezone_name": "UTC"}
                }]
            elif ("weather" in last_message_lower or "temperature" in last_message_lower) and "weather_search" in tool_names:
                tool_calls = [{
                    "id": "call_weather_01",
                    "name": "weather_search",
                    "arguments": {"location": "San Francisco, CA"}
                }]

        if tool_calls:
            response_text = f"Decided to invoke tool: {tool_calls[0]['name']}."
        else:
            response_text = f"ForgeAI Assistant: Received message '{last_message}'."

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
            latency_ms=latency_ms,
            tool_calls=tool_calls
        )

    async def stream_generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        last_message = messages[-1].content if messages else "Hello"
        response_text = f"ForgeAI Streaming: Response for '{last_message}'."
        words = response_text.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.05)
