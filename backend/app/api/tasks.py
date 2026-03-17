from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..agents.research_agent import agent, Task

router = APIRouter()


class TaskRequest(BaseModel):
    description: str


class ResearchRequest(BaseModel):
    query: str
    goal: str


@router.get("/status")
async def get_agent_status():
    """Get current agent status"""
    return agent.get_status()


@router.post("/tasks", response_model=List[Task])
async def create_tasks(request: ResearchRequest):
    """Create tasks from a research goal"""
    try:
        tasks = await agent.plan(request.goal)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all current tasks"""
    return agent.tasks


@router.post("/tasks/{task_id}/execute")
async def execute_task(task_id: str):
    """Execute a specific task"""
    task = next((t for t in agent.tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    result = await agent.execute_task(task)
    return {"task_id": task_id, "result": result}


@router.post("/research")
async def conduct_research(request: ResearchRequest):
    """Conduct autonomous research"""
    try:
        result = await agent.research(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
