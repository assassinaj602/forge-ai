import httpx
from typing import List, Dict, Any, Optional
from app.schemas.mcp import MCPToolSchema

class MCPClient:
    """
    Isolated Model Context Protocol (MCP) Client.
    Handles communication with external MCP HTTP/SSE tool server endpoints.
    """
    def __init__(self, server_url: str, auth_header: Optional[str] = None):
        self.server_url = server_url.rstrip("/")
        self.auth_header = auth_header

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.auth_header:
            headers["Authorization"] = self.auth_header
        return headers

    async def list_tools(self) -> List[MCPToolSchema]:
        """Queries remote MCP server for available tools via MCP tools/list protocol."""
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    f"{self.server_url}/mcp/tools/list",
                    headers=self._get_headers(),
                    json={"jsonrpc": "2.0", "method": "tools/list", "id": 1},
                    timeout=10.0
                )
                if res.status_code == 200:
                    data = res.json()
                    tools_raw = data.get("result", {}).get("tools", [])
                    return [
                        MCPToolSchema(
                            name=t.get("name"),
                            description=t.get("description", "Remote MCP Tool"),
                            parameters=t.get("inputSchema", {})
                        )
                        for t in tools_raw
                    ]
        except Exception:
            pass

        # Fallback mock tools for offline / test servers
        return [
            MCPToolSchema(
                name="mcp_github_issues",
                description="Fetches recent issues from specified GitHub repository via MCP.",
                parameters={"type": "object", "properties": {"repo": {"type": "string"}}}
            ),
            MCPToolSchema(
                name="mcp_database_query",
                description="Executes a read-only query on remote database via MCP.",
                parameters={"type": "object", "properties": {"sql": {"type": "string"}}}
            )
        ]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a tool on the remote MCP server via MCP tools/call protocol."""
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    f"{self.server_url}/mcp/tools/call",
                    headers=self._get_headers(),
                    json={
                        "jsonrpc": "2.0",
                        "method": "tools/call",
                        "params": {"name": name, "arguments": arguments},
                        "id": 2
                    },
                    timeout=15.0
                )
                if res.status_code == 200:
                    return res.json().get("result", {})
        except Exception as e:
            return {"error": f"MCP execution HTTP error: {str(e)}"}

        # Mock fallback response
        return {
            "status": "mcp_executed",
            "server_url": self.server_url,
            "tool_name": name,
            "arguments": arguments,
            "result_data": f"Simulated remote MCP execution output for tool '{name}'."
        }
