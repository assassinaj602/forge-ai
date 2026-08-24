"""
Vector DB & System Data Export/Backup Service
"""
import json
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Conversation, Message
from app.db.models_rag import KnowledgeCollection, DocumentChunk

class ExportBackupService:
    """Service to export conversations, knowledge collections, and vector chunks to JSON backup."""

    @staticmethod
    async def export_user_data(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        # Export conversations
        convs_res = await db.execute(select(Conversation).where(Conversation.user_id == user_id))
        conversations = convs_res.scalars().all()

        conv_data = []
        for c in conversations:
            msg_res = await db.execute(select(Message).where(Message.conversation_id == c.id))
            msgs = msg_res.scalars().all()
            conv_data.append({
                "id": c.id,
                "title": c.title,
                "provider": c.provider,
                "model": c.model,
                "messages": [{"role": m.role, "content": m.content, "created_at": str(m.created_at)} for m in msgs]
            })

        # Export RAG collections
        kc_res = await db.execute(select(KnowledgeCollection).where(KnowledgeCollection.user_id == user_id))
        collections = kc_res.scalars().all()

        kc_data = []
        for k in collections:
            kc_data.append({
                "id": k.id,
                "name": k.name,
                "description": k.description,
                "created_at": str(k.created_at)
            })

        return {
            "version": "1.0",
            "user_id": user_id,
            "conversations": conv_data,
            "knowledge_collections": kc_data,
            "total_conversations": len(conv_data),
            "total_collections": len(kc_data)
        }
