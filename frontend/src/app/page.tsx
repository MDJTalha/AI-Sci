'use client'

import { useState } from 'react'
import { Brain, FlaskConical, Search, Play, CheckCircle, Clock } from 'lucide-react'

interface Task {
  id: string
  description: string
  status: string
  result?: string
}

interface ResearchResult {
  query: string
  tasks_completed: number
  findings: Array<{task: string, result: string}>
  summary: string
}

export default function Home() {
  const [goal, setGoal] = useState('')
  const [isResearching, setIsResearching] = useState(false)
  const [tasks, setTasks] = useState<Task[]>([])
  const [result, setResult] = useState<ResearchResult | null>(null)

  const startResearch = async () => {
    if (!goal.trim()) return
    
    setIsResearching(true)
    setResult(null)
    
    try {
      const response = await fetch('http://localhost:8000/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: goal, goal: goal })
      })
      
      if (response.ok) {
        const data = await response.json()
        setResult(data)
      }
    } catch (error) {
      console.error('Research failed:', error)
    } finally {
      setIsResearching(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Brain className="w-12 h-12 text-blue-400" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              NeuroScholar
            </h1>
          </div>
          <p className="text-gray-400 text-lg">
            Autonomous AI Research Agent for Science & Technology
          </p>
        </header>

        {/* Research Input */}
        <section className="mb-12">
          <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <FlaskConical className="w-5 h-5" />
              Research Goal
            </h2>
            <div className="flex gap-4">
              <input
                type="text"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                placeholder="Enter your research goal (e.g., 'Analyze recent advances in quantum computing')"
                className="flex-1 bg-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isResearching}
              />
              <button
                onClick={startResearch}
                disabled={isResearching || !goal.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
              >
                {isResearching ? (
                  <>
                    <Clock className="w-5 h-5 animate-spin" />
                    Researching...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Start Research
                  </>
                )}
              </button>
            </div>
          </div>
        </section>

        {/* Tasks */}
        {tasks.length > 0 && (
          <section className="mb-12">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5" />
              Research Tasks
            </h2>
            <div className="grid gap-4">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className="bg-gray-800 rounded-lg p-4 flex items-center gap-4"
                >
                  <div className={`w-3 h-3 rounded-full ${
                    task.status === 'completed' ? 'bg-green-500' : 'bg-yellow-500'
                  }`} />
                  <span className="flex-1">{task.description}</span>
                  <span className={`text-sm px-3 py-1 rounded-full ${
                    task.status === 'completed' 
                      ? 'bg-green-900 text-green-300' 
                      : 'bg-yellow-900 text-yellow-300'
                  }`}>
                    {task.status}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Results */}
        {result && (
          <section className="mb-12">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Search className="w-5 h-5" />
              Research Results
            </h2>
            <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-blue-400 mb-2">Summary</h3>
                <p className="text-gray-300 leading-relaxed">{result.summary}</p>
              </div>
              
              <div className="border-t border-gray-700 pt-6">
                <h3 className="text-lg font-semibold text-purple-400 mb-4">
                  Findings ({result.tasks_completed} tasks completed)
                </h3>
                <div className="space-y-4">
                  {result.findings.map((finding, idx) => (
                    <div key={idx} className="bg-gray-700 rounded-lg p-4">
                      <p className="text-sm text-gray-400 mb-2">{finding.task}</p>
                      <p className="text-gray-200">{finding.result}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Features */}
        <section className="grid md:grid-cols-3 gap-6 mt-12">
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <Brain className="w-12 h-12 text-blue-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Autonomous Planning</h3>
            <p className="text-gray-400 text-sm">
              Breaks down complex research goals into actionable tasks
            </p>
          </div>
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <FlaskConical className="w-12 h-12 text-purple-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Self-Learning</h3>
            <p className="text-gray-400 text-sm">
              Builds knowledge base from every research session
            </p>
          </div>
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <Search className="w-12 h-12 text-green-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Multi-Source Research</h3>
            <p className="text-gray-400 text-sm">
              Searches academic papers, web, and databases
            </p>
          </div>
        </section>
      </div>
    </main>
  )
}
