import { useState } from 'react'
import { cliniqAPI } from '../api/client.js'

const TASK_DATA = {
  viral_uri: {
    title: 'Viral Upper Respiratory Infection',
    description: 'A patient presents with sore throat, runny nose, and cough.',
    difficulty: 'easy',
    icon: '🤧',
    color: 'from-blue-400 to-blue-600',
  },
  type2_diabetes: {
    title: 'Type 2 Diabetes Management',
    description: 'Managing blood glucose and diabetes complications in follow-up.',
    difficulty: 'medium',
    icon: '🩺',
    color: 'from-purple-400 to-purple-600',
  },
  sepsis_triage: {
    title: 'Sepsis Triage & Treatment',
    description: 'Quickly identify and treat a patient showing signs of sepsis.',
    difficulty: 'hard',
    icon: '⚠️',
    color: 'from-red-400 to-red-600',
  },
  drug_interaction: {
    title: 'Drug Interaction Management',
    description: 'Identify and resolve harmful drug interactions.',
    difficulty: 'hard',
    icon: '💊',
    color: 'from-orange-400 to-orange-600',
  },
  rare_disease_hunt: {
    title: 'Rare Disease Diagnosis',
    description: 'Diagnose a rare but important disease from vague symptoms.',
    difficulty: 'expert',
    icon: '🔍',
    color: 'from-pink-400 to-pink-600',
  },
}

function TaskSelector({ onSelectTask }) {
  const [loading, setLoading] = useState(false)
  const [tasks, setTasks] = useState(Object.keys(TASK_DATA))

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: 'bg-green-500/20 text-green-400 border-green-500/30',
      medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
      hard: 'bg-red-500/20 text-red-400 border-red-500/30',
      expert: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
    }
    return colors[difficulty] || colors.easy
  }

  const handleSelectTask = async (taskId) => {
    setLoading(true)
    try {
      await onSelectTask(taskId)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="text-center space-y-2">
        <h2 className="text-4xl font-bold text-white">Clinical Cases</h2>
        <p className="text-gray-400">Select a case to begin your clinical decision-making challenge</p>
      </div>

      {/* Tasks Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tasks.map((taskId) => {
          const task = TASK_DATA[taskId]
          return (
            <button
              key={taskId}
              onClick={() => handleSelectTask(taskId)}
              disabled={loading}
              className="group relative overflow-hidden rounded-xl transition-all transform hover:scale-105 active:scale-95"
            >
              {/* Background gradient */}
              <div className={`absolute inset-0 bg-gradient-to-br ${task.color} opacity-20 group-hover:opacity-30 transition-opacity`} />
              
              {/* Glass effect */}
              <div className="relative glass-dark p-8 flex flex-col gap-4 h-full">
                {/* Icon */}
                <div className="text-5xl">{task.icon}</div>

                {/* Title */}
                <h3 className="text-xl font-bold text-white text-left">{task.title}</h3>

                {/* Description */}
                <p className="text-sm text-gray-400 text-left flex-grow">{task.description}</p>

                {/* Difficulty Badge */}
                <div className="flex justify-between items-center">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getDifficultyColor(task.difficulty)}`}>
                    {task.difficulty.toUpperCase()}
                  </span>
                  <span className="text-2xl group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </div>
            </button>
          )
        })}
      </div>

      {/* Info Box */}
      <div className="glass-dark p-6 rounded-xl">
        <h3 className="text-lg font-semibold text-white mb-3">How to Play:</h3>
        <ul className="space-y-2 text-gray-400 text-sm">
          <li>✓ Request patient history to understand their background</li>
          <li>✓ Order labs and tests to gather diagnostic information</li>
          <li>✓ Make a diagnosis based on the evidence</li>
          <li>✓ Recommend appropriate treatment</li>
          <li>✓ Get scored on accuracy, safety, and efficiency</li>
        </ul>
      </div>
    </div>
  )
}

export default TaskSelector
