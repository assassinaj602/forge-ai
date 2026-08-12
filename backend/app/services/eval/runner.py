import re
from typing import List, Dict, Any
from app.db.models_eval import EvalSuite, EvalTestCase, EvalRun
from app.services.llm.factory import get_llm_provider
from app.services.llm.base import LLMMessage

class EvalRunner:
    @staticmethod
    def evaluate_assertion(assertion_type: str, actual: str, expected: str) -> bool:
        actual_clean = (actual or "").strip().lower()
        expected_clean = (expected or "").strip().lower()

        if assertion_type == "contains":
            return expected_clean in actual_clean
        elif assertion_type == "exact_match":
            return actual_clean == expected_clean
        elif assertion_type == "regex":
            try:
                return bool(re.search(expected, actual, re.IGNORECASE))
            except Exception:
                return False
        elif assertion_type == "length":
            try:
                min_len = int(expected)
                return len(actual) >= min_len
            except Exception:
                return len(actual) > 0
        return True

    @staticmethod
    async def run_suite(
        suite: EvalSuite,
        test_cases: List[EvalTestCase],
        model: str,
        provider_name: str,
        user_id: str
    ) -> EvalRun:
        llm = get_llm_provider(provider_name)
        results = []
        passed_count = 0

        for tc in test_cases:
            messages = [LLMMessage(role="user", content=tc.prompt)]
            llm_resp = await llm.generate(messages=messages, model=model)
            
            passed = EvalRunner.evaluate_assertion(tc.assertion_type, llm_resp.content, tc.expected_output or "")
            if passed:
                passed_count += 1

            results.append({
                "test_case_id": tc.id,
                "prompt": tc.prompt,
                "expected_output": tc.expected_output,
                "assertion_type": tc.assertion_type,
                "actual_output": llm_resp.content,
                "passed": passed,
                "latency_ms": llm_resp.latency_ms,
                "total_tokens": llm_resp.total_tokens
            })

        total_count = len(test_cases)
        score = round((passed_count / total_count * 100.0), 2) if total_count > 0 else 100.0

        eval_run = EvalRun(
            suite_id=suite.id,
            user_id=user_id,
            model=model,
            provider=provider_name,
            score=score,
            passed_count=passed_count,
            failed_count=total_count - passed_count,
            total_count=total_count,
            results=results
        )
        return eval_run
