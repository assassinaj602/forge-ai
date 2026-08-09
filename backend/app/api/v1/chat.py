import json
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db.models import User, Conversation, Message
from app.db.models_usage import UsageLog
from app.api.deps import get_current_user
from app.schemas.chat import ChatMessageRequest, StructuredAnalysisRequest
from app.services.llm.factory import get_llm_provider
from app.services.llm.base import LLMMessage
from app.services.llm.structured import generate_structured_output

router = APIRouter(prefix="/chat", tags=["Chat"])

async def get_or_create_conversation(
    db: AsyncSession,
    user_id: str,
    conversation_id: str = None,
    provider: str = "mock",
    model: str = "mock-v1",
    system_prompt: str = None
) -> Conversation:
    if conversation_id:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id, Conversation.user_id == user_id)
            .options(selectinload(Conversation.messages))
        )
        conv = result.scalar_one_or_none()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conv

    conv = Conversation(
        user_id=user_id,
        title="New Chat",
        provider=provider,
        model=model,
        system_prompt=system_prompt
    )
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    
    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conv.id)
        .options(selectinload(Conversation.messages))
    )
    return result.scalar_one()

@router.post("/completions")
async def chat_completions(
    req: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    conv = await get_or_create_conversation(
        db, current_user.id, req.conversation_id, req.provider, req.model, req.system_prompt
    )

    # Save user message
    user_msg = Message(conversation_id=conv.id, role="user", content=req.message)
    db.add(user_msg)
    await db.commit()

    # Build message context
    history = [LLMMessage(role=m.role, content=m.content) for m in conv.messages]
    history.append(LLMMessage(role="user", content=req.message))

    provider = get_llm_provider(req.provider)
    llm_resp = await provider.generate(
        messages=history,
        system_prompt=req.system_prompt or conv.system_prompt,
        model=req.model or conv.model
    )

    # Save assistant message
    asst_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=llm_resp.content,
        tokens_used=llm_resp.total_tokens,
        latency_ms=llm_resp.latency_ms
    )
    db.add(asst_msg)

    # Record usage log
    usage = UsageLog(
        user_id=current_user.id,
        provider=llm_resp.provider,
        model=llm_resp.model,
        prompt_tokens=llm_resp.prompt_tokens,
        completion_tokens=llm_resp.completion_tokens,
        total_tokens=llm_resp.total_tokens,
        estimated_cost=llm_resp.total_tokens * 0.000002,
        latency_ms=llm_resp.latency_ms
    )
    db.add(usage)
    await db.commit()

    return {
        "conversation_id": conv.id,
        "message": {
            "id": asst_msg.id,
            "role": "assistant",
            "content": llm_resp.content,
            "tokens_used": llm_resp.total_tokens,
            "latency_ms": llm_resp.latency_ms
        }
    }

@router.post("/stream")
async def chat_stream(
    req: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    conv = await get_or_create_conversation(
        db, current_user.id, req.conversation_id, req.provider, req.model, req.system_prompt
    )

    user_msg = Message(conversation_id=conv.id, role="user", content=req.message)
    db.add(user_msg)
    await db.commit()

    history = [LLMMessage(role=m.role, content=m.content) for m in conv.messages]
    history.append(LLMMessage(role="user", content=req.message))

    provider = get_llm_provider(req.provider)

    async def event_generator() -> AsyncGenerator[dict, None]:
        full_content = ""
        async for chunk in provider.stream_generate(
            messages=history,
            system_prompt=req.system_prompt or conv.system_prompt,
            model=req.model or conv.model
        ):
            full_content += chunk
            yield {"data": json.dumps({"content": chunk, "conversation_id": conv.id})}
            
        # Save complete message after stream ends
        asst_msg = Message(
            conversation_id=conv.id,
            role="assistant",
            content=full_content,
            tokens_used=len(full_content.split()),
            latency_ms=500
        )
        db.add(asst_msg)
        await db.commit()
        yield {"data": json.dumps({"content": "", "conversation_id": conv.id, "done": True})}

    return EventSourceResponse(event_generator())

@router.post("/structured")
async def analyze_structured(
    req: StructuredAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    provider = get_llm_provider(req.provider)
    result = await generate_structured_output(
        provider=provider,
        prompt=req.text,
        model=req.model or "mock-v1"
    )
    return {"status": "success", "data": result}
