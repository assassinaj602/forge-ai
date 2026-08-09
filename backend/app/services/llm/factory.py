from app.services.llm.base import BaseLLMProvider
from app.services.llm.mock import MockLLMProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.gemini_provider import GeminiProvider

def get_llm_provider(provider_name: str = "mock") -> BaseLLMProvider:
    provider_name = (provider_name or "mock").lower().strip()
    if provider_name == "openai":
        return OpenAIProvider()
    elif provider_name in ["gemini", "google"]:
        return GeminiProvider()
    else:
        return MockLLMProvider()
