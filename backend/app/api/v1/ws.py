"""
WebSocket Endpoints for Real-time Streaming Chat
"""
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.services.ws.manager import ws_manager
from app.services.llm.factory import get_llm_provider
from app.services.llm.base import LLMMessage

router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/chat")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    # For testing/demo token validation
    user_id = "ws_user"
    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            prompt = data.get("message", "")
            provider_name = data.get("provider", "mock")
            model_name = data.get("model", "mock-v1")

            provider = get_llm_provider(provider_name)
            messages = [LLMMessage(role="user", content=prompt)]

            await ws_manager.send_json(websocket, {"type": "start", "status": "generating"})
            
            async for chunk in provider.generate_stream(messages=messages, model=model_name):
                await ws_manager.send_json(websocket, {"type": "chunk", "delta": chunk})

            await ws_manager.send_json(websocket, {"type": "done", "status": "completed"})

    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, websocket)
    except Exception as e:
        await ws_manager.send_json(websocket, {"type": "error", "detail": str(e)})
        ws_manager.disconnect(user_id, websocket)
