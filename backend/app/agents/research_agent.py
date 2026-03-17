from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from typing import List, Dict, Optional
from pydantic import BaseModel
import uuid


class Task(BaseModel):
    id: str
    description: str
    status: str = "pending"
    result: Optional[str] = None


class ResearchAgent:
    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model, temperature=0.7)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tasks: List[Task] = []
        self.knowledge_base = []
        
    async def plan(self, goal: str) -> List[Task]:
        """Break down a research goal into executable tasks"""
        prompt = f"""Break down this research goal into specific, actionable tasks:
        
Goal: {goal}

Return a JSON list of tasks with descriptions."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        # Parse response into tasks
        task_descriptions = self._parse_tasks(response.content)
        
        self.tasks = [
            Task(id=str(uuid.uuid4()), description=desc)
            for desc in task_descriptions
        ]
        return self.tasks
    
    async def execute_task(self, task: Task) -> str:
        """Execute a single research task"""
        prompt = f"""Execute this research task:
        
Task: {task.description}

Provide findings, analysis, or results."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        task.status = "completed"
        task.result = response.content
        return response.content
    
    async def research(self, query: str) -> Dict:
        """Conduct autonomous research on a topic"""
        # Plan
        tasks = await self.plan(query)
        
        # Execute
        results = []
        for task in tasks:
            result = await self.execute_task(task)
            results.append({"task": task.description, "result": result})
        
        # Synthesize
        synthesis_prompt = f"""Synthesize these research findings into a coherent summary:
        
{results}"""
        
        synthesis = await self.llm.ainvoke([HumanMessage(content=synthesis_prompt)])
        
        return {
            "query": query,
            "tasks_completed": len(tasks),
            "findings": results,
            "summary": synthesis.content
        }
    
    def _parse_tasks(self, response: str) -> List[str]:
        """Parse LLM response into task list"""
        import json
        try:
            tasks = json.loads(response)
            if isinstance(tasks, list):
                return [t.get("description", str(t)) for t in tasks]
        except:
            pass
        # Fallback: split by newlines
        return [line.strip() for line in response.split('\n') if line.strip()]
    
    def get_status(self) -> Dict:
        return {
            "total_tasks": len(self.tasks),
            "completed": sum(1 for t in self.tasks if t.status == "completed"),
            "pending": sum(1 for t in self.tasks if t.status == "pending")
        }


# Global agent instance
agent = ResearchAgent()
