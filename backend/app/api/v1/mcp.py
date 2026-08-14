from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import User
from app.db.models_mcp import MCPServerConfig
from app.api.deps import get_current_user
from app.schemas.mcp import MCPServerCreate, MCPServerResponse
from app.services.mcp.client import MCPClient
from app.services.mcp.adapter import MCPToolAdapter
from app.services.tools.registry import global_tool_registry

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.get("/servers", response_model=List[MCPServerResponse])
async def list_mcp_servers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MCPServerConfig)
        .where(MCPServerConfig.user_id == current_user.id)
        .order_by(MCPServerConfig.created_at.desc())
    )
    return result.scalars().all()

@router.post("/servers", response_model=MCPServerResponse, status_code=status.HTTP_201_CREATED)
async def create_mcp_server(
    server_in: MCPServerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    config = MCPServerConfig(
        user_id=current_user.id,
        name=server_in.name,
        server_url=server_in.server_url,
        auth_header=server_in.auth_header,
        is_active=server_in.is_active
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config

@router.post("/sync")
async def sync_mcp_tools(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MCPServerConfig)
        .where(MCPServerConfig.user_id == current_user.id, MCPServerConfig.is_active == True)
    )
    servers = result.scalars().all()
    
    synced_tools = []
    for s in servers:
        client = MCPClient(s.server_url, s.auth_header)
        mcp_tools = await client.list_tools()
        for t in mcp_tools:
            adapter = MCPToolAdapter(t, client)
            global_tool_registry.register(adapter)
            synced_tools.append(t.name)

    return {"status": "success", "synced_server_count": len(servers), "registered_tools": synced_tools}

@router.delete("/servers/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mcp_server(
    server_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MCPServerConfig)
        .where(MCPServerConfig.id == server_id, MCPServerConfig.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="MCP Server config not found")
        
    await db.delete(config)
    await db.commit()
    return None
