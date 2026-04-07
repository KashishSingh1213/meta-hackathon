import { useEffect, useState } from 'react'
import { cliniqAPI } from '../api/client.js'

function EpisodeSummary({ task, observation, stepCount, totalReward, onReturnToMenu, onComplete }) {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await cliniqAPI.getEpisodeSummary()
        setSummary(response.data)
        onComplete(response.data)
      } catch (error) {
        console.error('Failed to fetch summary:', error)
        // Create mock summary
        setSummary({
          task_name: task,
          total_reward: totalReward,
          step_count: stepCount,
          grade: totalReward >= 4.5 ? 'A' : totalReward >= 3.5 ? 'B' : totalReward >= 2.5 ? 'C' : 'D',
          reward_breakdown: {
            accuracy: 0.75,
            safety: 0.85,
            efficiency: 0.70,
            penalty: 0.1,
          },
          xp_earned: Math.floor((totalReward / 5.0) * 100),
          achievements_unlocked: ['Fast Thinker'],
          duration_seconds: stepCount * 30,
        })
      } finally {
        setLoading(false)
      }
    }
    fetchSummary()
  }, [])

  if (loading || !summary) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">Loading episode summary...</p>
      </div>
    )
  }

  const getGradeColor = (grade) => {
    const colors = {
      'A': 'text-success',
      'B': 'text-medical',
      'C': 'text-warning',
      'D': 'text-danger',
      'F': 'text-danger',
    }
    return colors[grade] || colors.A
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6 animate-slide-in">
      {/* Main Grade */}
      <div className="card-medical text-center">
        <p className="text-gray-400 mb-2">Episode Complete!</p>
        <div className={`text-8xl font-bold ${getGradeColor(summary.grade)} mb-4`}>
          {summary.grade}
        </div>
        <h2 className="text-3xl font-bold text-white mb-2">
          {summary.grade === 'A' && '🏆 Perfect Diagnosis!'}
          {summary.grade === 'B' && '⭐ Great Work!'}
          {summary.grade === 'C' && '💪 Good Effort!'}
          {summary.grade === 'D' && '📚 Keep Learning!'}
          {summary.grade === 'F' && '💔 Not Quite!'}
        </h2>
      </div>

      {/* Score Breakdown */}
      <div className="card-medical">
        <h3 className="text-lg font-bold text-white mb-4">Performance Breakdown</h3>
        <div className="space-y-4">
          {/* Total Reward */}
          <div className="p-4 glass-dark rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-400">Total Reward</span>
              <span className="text-2xl font-bold text-medical">{summary.total_reward.toFixed(2)} / 5.0</span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-3 overflow-hidden">
              <div
                className="bg-gradient-to-r from-medical to-success h-full transition-all duration-300"
                style={{ width: `${Math.min((summary.total_reward / 5.0) * 100, 100)}%` }}
              />
            </div>
          </div>

          {/* Accuracy */}
          <div className="p-4 glass-dark rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-400">🎯 Accuracy</span>
              <span className="text-lg font-bold text-success">{(summary.reward_breakdown.accuracy * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
              <div className="w-3/4 h-full bg-success" />
            </div>
          </div>

          {/* Safety */}
          <div className="p-4 glass-dark rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-400">🛡️ Safety</span>
              <span className="text-lg font-bold text-medical">{(summary.reward_breakdown.safety * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
              <div className="w-4/5 h-full bg-medical" />
            </div>
          </div>

          {/* Efficiency */}
          <div className="p-4 glass-dark rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-400">⚡ Efficiency</span>
              <span className="text-lg font-bold text-warning">{(summary.reward_breakdown.efficiency * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
              <div className="w-2/3 h-full bg-warning" />
            </div>
          </div>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-3 gap-4">
        <div className="glass-dark p-4 rounded-lg text-center">
          <p className="text-3xl font-bold text-medical mb-1">{summary.step_count}</p>
          <p className="text-xs text-gray-400">Steps</p>
        </div>
        <div className="glass-dark p-4 rounded-lg text-center">
          <p className="text-3xl font-bold text-success mb-1">{summary.xp_earned}</p>
          <p className="text-xs text-gray-400">XP Earned</p>
        </div>
        <div className="glass-dark p-4 rounded-lg text-center">
          <p className="text-3xl font-bold text-warning mb-1">{(summary.duration_seconds / 60).toFixed(1)}m</p>
          <p className="text-xs text-gray-400">Duration</p>
        </div>
      </div>

      {/* Achievements */}
      {summary.achievements_unlocked && summary.achievements_unlocked.length > 0 && (
        <div className="card-medical">
          <h3 className="text-lg font-bold text-white mb-3">🏅 Achievements Unlocked</h3>
          <div className="grid grid-cols-2 gap-2">
            {summary.achievements_unlocked.map(achievement => (
              <div key={achievement} className="p-3 bg-success/20 border border-success/30 rounded-lg text-center">
                <p className="text-sm font-semibold text-success">{achievement}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4">
        <button
          onClick={onReturnToMenu}
          className="btn-secondary flex-1"
        >
          Return to Menu
        </button>
        <button
          onClick={onReturnToMenu}
          className="btn-primary flex-1"
        >
          Play Again
        </button>
      </div>
    </div>
  )
}

export default EpisodeSummary
