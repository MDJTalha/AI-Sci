from fastapi import APIRouter
from pydantic import BaseModel
from ..agents.research_agent import agent

router = APIRouter()


class AgentInfo(BaseModel):
    model: str
    status: str


@router.get("/info")
async def get_agent_info():
    """Get agent information"""
    return {
        "model": "gpt-4",
        "status": "active",
        "capabilities": ["planning", "research", "analysis", "synthesis"]
    }


@router.get("/memory")
async def get_memory_stats():
    """Get agent memory statistics"""
    return {
        "knowledge_items": len(agent.knowledge_base),
        "active_tasks": len(agent.tasks)
    }
