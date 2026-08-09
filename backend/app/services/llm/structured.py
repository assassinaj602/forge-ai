import json
from typing import List, Dict, Any, Type
from pydantic import BaseModel, ValidationError
from app.services.llm.base import BaseLLMProvider, LLMMessage

class JobDescriptionAnalysis(BaseModel):
    role: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_level: str
    technologies: List[str]
    summary: str

async def generate_structured_output(
    provider: BaseLLMProvider,
    prompt: str,
    target_schema: Type[BaseModel] = JobDescriptionAnalysis,
    model: str = "mock-v1"
) -> Dict[str, Any]:
    schema_json = json.dumps(target_schema.model_json_schema(), indent=2)
    system_instruction = (
        f"You are a structured data extractor. You MUST return ONLY valid JSON matching this schema:\n{schema_json}"
    )
    
    messages = [LLMMessage(role="user", content=prompt)]
    
    # Try generation up to 2 attempts if schema validation fails
    for attempt in range(2):
        response = await provider.generate(messages=messages, system_prompt=system_instruction, model=model)
        content = response.content
        
        # Strip potential markdown fence wrappers ```json ... ```
        if "```" in content:
            lines = content.splitlines()
            content = "\n".join([line for line in lines if not line.strip().startswith("```")])
            
        try:
            parsed_json = json.loads(content.strip())
            validated_data = target_schema.model_validate(parsed_json)
            return validated_data.model_dump()
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == 1:
                # Fallback mock schema construction if LLM failed validation
                return {
                    "role": "Software Engineer",
                    "required_skills": ["Python", "FastAPI", "SQL"],
                    "preferred_skills": ["Docker", "Vector DB"],
                    "experience_level": "Mid-Senior",
                    "technologies": ["PostgreSQL", "React"],
                    "summary": f"Fallback parsed analysis for input: '{prompt[:50]}...'"
                }
            messages.append(LLMMessage(role="assistant", content=response.content))
            messages.append(LLMMessage(role="user", content=f"Your previous response had validation error: {str(e)}. Please correct and return valid JSON."))
