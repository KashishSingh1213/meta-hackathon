import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

function RewardChart({ stepCount, totalReward }) {
  // Generate mock data for visualization
  const data = Array.from({ length: Math.max(stepCount, 1) }, (_, i) => ({
    step: i + 1,
    reward: Math.random() * (totalReward / Math.max(stepCount, 1)) * 1.5,
    cumulative: (totalReward / Math.max(stepCount, 1)) * (i + 1) * 0.9,
  }))

  return (
    <div className="card-medical">
      <div className="space-y-6">
        {/* Reward Score */}
        <div>
          <h3 className="text-sm font-semibold text-gray-300 mb-3">CURRENT SCORE</h3>
          <div className="glass-dark p-4 rounded-lg text-center">
            <p className="text-5xl font-bold text-medical">{totalReward.toFixed(2)}</p>
            <p className="text-sm text-gray-400 mt-1">out of 5.0</p>
            <div className="w-full bg-white/10 rounded-full h-2 mt-3 overflow-hidden">
              <div
                className="bg-gradient-to-r from-medical to-success h-full transition-all duration-300"
                style={{ width: `${Math.min((totalReward / 5.0) * 100, 100)}%` }}
              />
            </div>
          </div>
        </div>

        {/* Step Counter */}
        <div className="glass-dark p-4 rounded-lg">
          <p className="text-sm text-gray-400">Steps Taken</p>
          <p className="text-3xl font-bold text-white mt-1">{stepCount}</p>
        </div>

        {/* Performance Indicators */}
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-gray-300">PERFORMANCE</h3>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-400">Accuracy</span>
              <div className="flex-1 mx-2 h-2 bg-white/10 rounded-full overflow-hidden">
                <div className="w-2/3 h-full bg-success"></div>
              </div>
              <span className="text-xs font-semibold text-white">67%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-400">Safety</span>
              <div className="flex-1 mx-2 h-2 bg-white/10 rounded-full overflow-hidden">
                <div className="w-4/5 h-full bg-medical"></div>
              </div>
              <span className="text-xs font-semibold text-white">80%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-400">Efficiency</span>
              <div className="flex-1 mx-2 h-2 bg-white/10 rounded-full overflow-hidden">
                <div className="w-1/2 h-full bg-warning"></div>
              </div>
              <span className="text-xs font-semibold text-white">50%</span>
            </div>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="grid grid-cols-2 gap-2">
          <div className="glass-dark p-2 rounded text-center">
            <p className="text-xs text-gray-400">Alive</p>
            <p className="text-lg font-bold text-success">✓</p>
          </div>
          <div className="glass-dark p-2 rounded text-center">
            <p className="text-xs text-gray-400">On Track</p>
            <p className="text-lg font-bold text-medical">✓</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RewardChart
