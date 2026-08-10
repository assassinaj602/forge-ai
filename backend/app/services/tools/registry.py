from typing import Dict, List, Optional, Any
from app.services.tools.base import BaseTool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "schema": t.get_json_schema()
            }
            for t in self._tools.values()
        ]

    def get_openai_tools_schema(self) -> List[Dict[str, Any]]:
        return [t.get_json_schema() for t in self._tools.values()]

    async def execute_tool(self, name: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        tool = self.get_tool(name)
        if not tool:
            return {"error": f"Tool '{name}' not found in registry"}
        try:
            validated_args = tool.args_schema.model_validate(kwargs)
            return await tool.execute(**validated_args.model_dump())
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

# Global tool registry singleton
global_tool_registry = ToolRegistry()
