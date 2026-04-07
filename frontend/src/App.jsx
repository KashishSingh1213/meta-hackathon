import { useState, useEffect } from 'react'
import TaskSelector from './components/TaskSelector'
import PatientCard from './components/PatientCard'
import ActionPanel from './components/ActionPanel'
import RewardChart from './components/RewardChart'
import EpisodeSummary from './components/EpisodeSummary'
import { useEnvironment } from './hooks/useEnvironment.js'
import { useLocalStorage } from './hooks/useLocalStorage.js'

function App() {
  const [gameState, setGameState] = useState('task-select')
  const [xp, setXp] = useLocalStorage('cliniq_xp', 0)
  const [level, setLevel] = useLocalStorage('cliniq_level', 1)
  const [achievements, setAchievements] = useLocalStorage('cliniq_achievements', [])
  const [selectedTask, setSelectedTask] = useState(null)
  
  const {
    observation,
    loading,
    error,
    stepCount,
    totalReward,
    episodeDone,
    reset,
    step,
  } = useEnvironment()

  const handleTaskSelect = async (task) => {
    setSelectedTask(task)
    await reset(task)
    setGameState('playing')
  }

  const handleReturnToMenu = () => {
    setGameState('task-select')
    setSelectedTask(null)
  }

  const handleEpisodeComplete = (summary) => {
    // Update stats
    setXp(prev => Math.min(prev + summary.xp_earned, 999999))
    setLevel(Math.floor(xp / 500) + 1)
    
    // Add achievements
    if (summary.achievements_unlocked) {
      setAchievements(prev => [
        ...new Set([...prev, ...summary.achievements_unlocked])
      ])
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-dark via-darker to-black">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 glass-dark border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-medical rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">⚕️</span>
            </div>
            <h1 className="text-2xl font-bold text-white">ClinIQ</h1>
          </div>
          <div className="flex items-center gap-6">
            <div className="text-right">
              <p className="text-sm text-gray-400">Level {level}</p>
              <p className="text-lg font-semibold text-medical">{xp} XP</p>
            </div>
            {gameState === 'playing' && (
              <button
                onClick={handleReturnToMenu}
                className="btn-secondary text-sm"
              >
                Main Menu
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-12 min-h-screen">
        <div className="max-w-7xl mx-auto px-4">
          {gameState === 'task-select' && (
            <TaskSelector onSelectTask={handleTaskSelect} />
          )}

          {gameState === 'playing' && observation && !episodeDone && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-slide-in">
              <div className="lg:col-span-2 space-y-6">
                <PatientCard observation={observation} stepCount={stepCount} />
                <ActionPanel
                  observation={observation}
                  onAction={step}
                  loading={loading}
                />
              </div>
              <div>
                <RewardChart
                  stepCount={stepCount}
                  totalReward={totalReward}
                />
              </div>
            </div>
          )}

          {gameState === 'playing' && episodeDone && observation && (
            <EpisodeSummary
              task={selectedTask}
              observation={observation}
              stepCount={stepCount}
              totalReward={totalReward}
              onReturnToMenu={handleReturnToMenu}
              onComplete={handleEpisodeComplete}
            />
          )}

          {error && (
            <div className="glass-dark bg-danger/20 border-danger/50 p-4 rounded-lg">
              <p className="text-danger">{error}</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
