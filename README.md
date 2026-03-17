# NeuroScholar 🧠🔬

An autonomous AI research agent designed to assist in scientific research, technology projects, and scholarly work.

## Features

- **Autonomous Research Agent**: LLM-powered reasoning for scientific tasks
- **Self-Learning Memory**: Vector database for knowledge retention
- **Research Tools**: Paper search, code execution, data analysis
- **Task Planning**: Autonomous goal decomposition and execution
- **Web Dashboard**: Real-time monitoring and interaction interface

## Architecture

```
neuroscholar/
├── backend/          # FastAPI + LangChain
│   └── app/
│       ├── agents/   # AI agent logic
│       ├── api/      # REST endpoints
│       ├── core/     # Core utilities
│       ├── memory/   # Vector storage
│       └── tools/    # Research tools
└── frontend/         # Next.js dashboard
    └── src/
        ├── app/      # Pages
        ├── components/
        └── lib/      # Utilities
```

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create `.env` files:

**backend/.env:**
```
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
DATABASE_URL=your_vector_db_url
```

**frontend/.env.local:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deployment

### Vercel (Frontend) ✅

**Live Demo**: https://frontend-two-taupe-56.vercel.app

```bash
cd frontend
vercel deploy --prod --yes
```

### Backend (Any platform)

Deploy to Railway, Render, or Fly.io:
```bash
# Example for Railway
railway up
```

## License

MIT License
