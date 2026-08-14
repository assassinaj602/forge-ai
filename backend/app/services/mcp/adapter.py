from typing import Dict, Any, Type
from pydantic import create_model, BaseModel, Field
from app.services.tools.base import BaseTool
from app.services.mcp.client import MCPClient
from app.schemas.mcp import MCPToolSchema

class MCPToolAdapter(BaseTool):
    """
    Adapter wrapping remote MCP tools as native BaseTool instances 
    for dynamic registration into ToolRegistry.
    """
    def __init__(self, mcp_schema: MCPToolSchema, client: MCPClient):
        self.name = mcp_schema.name
        self.description = mcp_schema.description
        self.client = client
        self.args_schema = self._build_dynamic_args_schema(mcp_schema.name, mcp_schema.parameters)

    def _build_dynamic_args_schema(self, tool_name: str, parameters: Dict[str, Any]) -> Type[BaseModel]:
        props = parameters.get("properties", {})
        fields = {}
        for prop_name, prop_info in props.items():
            field_type = str
            fields[prop_name] = (field_type, Field(..., description=prop_info.get("description", prop_name)))
        
        if not fields:
            fields["input_data"] = (Optional[str], Field(None, description="Optional payload"))
            
        return create_model(f"MCP_{tool_name}_Args", **fields)

    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        return await self.client.call_tool(self.name, kwargs)
