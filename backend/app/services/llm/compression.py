"""
Prompt Compression Engine for Context Optimization
"""
import re
from typing import Dict, Any

class PromptCompressionService:
    """Intelligent prompt compression service to optimize token usage (LLMLingua pattern)."""

    @staticmethod
    def compress_prompt(prompt: str, target_ratio: float = 0.5) -> Dict[str, Any]:
        if not prompt:
            return {"compressed_prompt": "", "original_tokens": 0, "compressed_tokens": 0, "compression_ratio": 1.0}

        words = prompt.split()
        original_token_estimate = len(words)
        
        # Stopwords & filler words reduction strategy
        fillers = {"the", "a", "an", "is", "are", "was", "were", "and", "or", "in", "on", "at", "to", "for", "of", "with", "that", "this", "it"}
        compressed_words = [w for w in words if w.lower() not in fillers or len(w) > 5]

        # Ensure we don't over-compress
        target_len = max(5, int(len(words) * target_ratio))
        if len(compressed_words) > target_len:
            compressed_words = compressed_words[:target_len]

        compressed_prompt = " ".join(compressed_words)
        compressed_token_estimate = len(compressed_words)
        saved_ratio = round(1.0 - (compressed_token_estimate / max(1, original_token_estimate)), 2)

        return {
            "compressed_prompt": compressed_prompt,
            "original_tokens": original_token_estimate,
            "compressed_tokens": compressed_token_estimate,
            "compression_ratio": saved_ratio,
            "tokens_saved": original_token_estimate - compressed_token_estimate
        }
