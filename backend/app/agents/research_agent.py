from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import List, Dict, Optional
from pydantic import BaseModel
import uuid
import os


class Task(BaseModel):
    id: str
    description: str
    status: str = "pending"
    result: Optional[str] = None


class ResearchAgent:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = ChatOpenAI(model=model, temperature=0.7, api_key=api_key)
        else:
            self.llm = None
        self.tasks: List[Task] = []
        self.knowledge_base = []
        
    async def plan(self, goal: str) -> List[Task]:
        """Break down a research goal into executable tasks"""
        if not self.llm:
            # Mock response if no API key
            return [
                Task(id=str(uuid.uuid4()), description=f"Research: {goal}"),
                Task(id=str(uuid.uuid4()), description="Analyze findings"),
                Task(id=str(uuid.uuid4()), description="Synthesize results")
            ]
        
        prompt = f"""Break down this research goal into specific, actionable tasks (return as JSON array):
        
Goal: {goal}

Example format: [{"description": "task 1"}, {"description": "task 2"}]"""
        
        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            task_descriptions = self._parse_tasks(response.content)
        except Exception as e:
            task_descriptions = [f"Research {goal}", "Analyze findings", "Write summary"]
        
        self.tasks = [
            Task(id=str(uuid.uuid4()), description=desc)
            for desc in task_descriptions
        ]
        return self.tasks
    
    async def execute_task(self, task: Task) -> str:
        """Execute a single research task"""
        if not self.llm:
            return f"Mock result for: {task.description}. Add OPENAI_API_KEY for real results."
        
        prompt = f"""Execute this research task:
        
Task: {task.description}

Provide findings, analysis, or results."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        task.status = "completed"
        task.result = response.content
        return response.content
    
    async def research(self, query: str) -> Dict:
        """Conduct autonomous research on a topic"""
        tasks = await self.plan(query)
        
        results = []
        for task in self.tasks:
            result = await self.execute_task(task)
            results.append({"task": task.description, "result": result})
        
        summary = "Research completed. See findings above."
        if self.llm:
            try:
                synthesis = await self.llm.ainvoke([HumanMessage(content=f"Summarize: {results}")])
                summary = synthesis.content
            except:
                pass
        
        return {
            "query": query,
            "tasks_completed": len([t for t in self.tasks if t.status == "completed"]),
            "findings": results,
            "summary": summary
        }
    
    def _parse_tasks(self, response: str) -> List[str]:
        """Parse LLM response into task list"""
        import json
        try:
            tasks = json.loads(response)
            if isinstance(tasks, list):
                return [t.get("description", str(t)) if isinstance(t, dict) else str(t) for t in tasks]
        except:
            pass
        return [line.strip() for line in response.split('\n') if line.strip() and line.strip()[0] not in '[]{}']
    
    def get_status(self) -> Dict:
        return {
            "total_tasks": len(self.tasks),
            "completed": sum(1 for t in self.tasks if t.status == "completed"),
            "pending": sum(1 for t in self.tasks if t.status == "pending"),
            "has_api_key": self.llm is not None
        }


agent = ResearchAgent()
