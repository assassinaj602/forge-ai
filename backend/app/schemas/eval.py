from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class TestCaseBase(BaseModel):
    prompt: str
    expected_output: Optional[str] = None
    assertion_type: str = "contains"

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseResponse(TestCaseBase):
    id: str
    suite_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SuiteBase(BaseModel):
    name: str
    description: Optional[str] = None

class SuiteCreate(SuiteBase):
    test_cases: List[TestCaseCreate] = []

class SuiteResponse(SuiteBase):
    id: str
    user_id: str
    created_at: datetime
    test_cases: List[TestCaseResponse] = []

    model_config = ConfigDict(from_attributes=True)

class EvalRunRequest(BaseModel):
    model: Optional[str] = "mock-v1"
    provider: Optional[str] = "mock"

class EvalRunResponse(BaseModel):
    id: str
    suite_id: str
    user_id: str
    model: str
    provider: str
    score: float
    passed_count: int
    failed_count: int
    total_count: int
    results: List[Dict[str, Any]] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ObservabilityMetricsResponse(BaseModel):
    total_requests: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_tokens: int
    total_estimated_cost_usd: float
    avg_latency_ms: float
    provider_breakdown: Dict[str, Dict[str, Any]]
