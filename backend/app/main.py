from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import tasks, agents, research
from .core import config

app = FastAPI(
    title="NeuroScholar API",
    description="Autonomous AI Research Agent",
    version="0.1.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(research.router, prefix="/api/research", tags=["research"])

@app.get("/")
async def root():
    return {"message": "NeuroScholar API", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
