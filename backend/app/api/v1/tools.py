from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.tools import ToolExecuteRequest, ToolChatRequest
from app.services.tools.registry import global_tool_registry, ToolRegistry
from app.services.tools.builtins.math_time import CalculatorTool, DateTimeTool
from app.services.tools.builtins.search_weather import WebSearchTool, WeatherTool
from app.services.tools.builtins.doc_search import DocumentSearchTool
from app.services.llm.factory import get_llm_provider
from app.services.llm.base import LLMMessage

# Register standard built-in tools in global registry
def _bootstrap_tools():
    if not global_tool_registry.get_tool("calculator"):
        global_tool_registry.register(CalculatorTool())
    if not global_tool_registry.get_tool("current_datetime"):
        global_tool_registry.register(DateTimeTool())
    if not global_tool_registry.get_tool("web_search"):
        global_tool_registry.register(WebSearchTool())
    if not global_tool_registry.register(WeatherTool()):
        global_tool_registry.register(WeatherTool())
    if not global_tool_registry.get_tool("document_search"):
        global_tool_registry.register(DocumentSearchTool())

_bootstrap_tools()

router = APIRouter(prefix="/tools", tags=["Tools"])

@router.get("", response_model=List[Dict[str, Any]])
async def list_tools(current_user: User = Depends(get_current_user)):
    return global_tool_registry.list_tools()

@router.post("/execute")
async def execute_tool_direct(
    req: ToolExecuteRequest,
    current_user: User = Depends(get_current_user)
):
    if req.tool_name == "document_search":
        req.arguments["user_id"] = current_user.id

    result = await global_tool_registry.execute_tool(req.tool_name, req.arguments)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"status": "success", "result": result}

@router.post("/chat")
async def chat_with_tools(
    req: ToolChatRequest,
    current_user: User = Depends(get_current_user)
):
    provider = get_llm_provider(req.provider)
    available_tools = global_tool_registry.get_openai_tools_schema()

    if req.enabled_tools:
        available_tools = [
            t for t in available_tools 
            if t.get("function", {}).get("name") in req.enabled_tools
        ]

    messages = [LLMMessage(role="user", content=req.message)]
    
    # 1. Initial LLM Decision Step
    first_response = await provider.generate(
        messages=messages,
        system_prompt=req.system_prompt,
        model=req.model,
        tools=available_tools
    )

    tool_executions = []
    
    # 2. Check if LLM requested tool execution
    if first_response.tool_calls:
        for tool_call in first_response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["arguments"]
            if tool_name == "document_search":
                tool_args["user_id"] = current_user.id
                
            res = await global_tool_registry.execute_tool(tool_name, tool_args)
            tool_executions.append({
                "tool_name": tool_name,
                "arguments": tool_args,
                "result": res
            })

        # 3. Follow-up synthesis step with tool results appended
        synthesis_prompt = (
            f"Original Request: {req.message}\n"
            f"Tool Execution Results: {tool_executions}\n"
            f"Please summarize the tool results and provide the final answer to the user."
        )
        final_llm_resp = await provider.generate(
            messages=[LLMMessage(role="user", content=synthesis_prompt)],
            model=req.model
        )
        return {
            "final_answer": final_llm_resp.content,
            "tool_calls_executed": tool_executions,
            "iterations": 2
        }

    return {
        "final_answer": first_response.content,
        "tool_calls_executed": [],
        "iterations": 1
    }
