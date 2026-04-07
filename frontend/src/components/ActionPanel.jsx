import { useState } from 'react'
import { useAgent } from '../hooks/useAgent.js'

const ACTION_TEMPLATES = {
  request_history: {
    label: 'Request History',
    icon: '📋',
    details: {},
  },
  order_labs: {
    label: 'Order Labs',
    icon: '🧪',
    details: {
      labs: ['Blood culture', 'CBC', 'CMP', 'Lactate'],
    },
  },
  diagnose: {
    label: 'Make Diagnosis',
    icon: '🎯',
    details: {
      diagnosis: '',
    },
  },
  recommend_treatment: {
    label: 'Recommend Treatment',
    icon: '💊',
    details: {
      treatment: '',
    },
  },
}

function ActionPanel({ observation, onAction, loading }) {
  const [selectedActionType, setSelectedActionType] = useState(null)
  const [actionDetails, setActionDetails] = useState({})
  const [agentMode, setAgentMode] = useState(false)
  const { isDeciding, agentAction, decide } = useAgent()

  const handleActionSubmit = async (actionType) => {
    const action = {
      action_type: actionType,
      details: actionDetails[actionType] || {},
      reasoning: null,
    }

    await onAction(action)
    setSelectedActionType(null)
    setActionDetails({})
  }

  const handleUseAgent = async () => {
    setAgentMode(true)
    const decision = await decide(observation)
    if (decision && decision.action) {
      await onAction(decision.action)
    }
    setAgentMode(false)
  }

  const handleDetailChange = (actionType, field, value) => {
    setActionDetails(prev => ({
      ...prev,
      [actionType]: {
        ...prev[actionType],
        [field]: value,
      },
    }))
  }

  return (
    <div className="card-medical">
      <h3 className="text-xl font-bold text-white mb-4">Next Action</h3>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {Object.entries(ACTION_TEMPLATES).map(([type, config]) => (
          <button
            key={type}
            onClick={() => setSelectedActionType(type)}
            disabled={loading || isDeciding}
            className={`p-3 rounded-lg transition-all text-center ${
              selectedActionType === type
                ? 'glass-dark bg-medical/30 border-medical/50'
                : 'glass-dark hover:bg-white/5'
            }`}
          >
            <div className="text-2xl mb-1">{config.icon}</div>
            <p className="text-xs font-semibold text-white">{config.label}</p>
          </button>
        ))}
      </div>

      {/* Action Details Form */}
      {selectedActionType && (
        <div className="p-4 glass-dark rounded-lg mb-4 space-y-4">
          {selectedActionType === 'order_labs' && (
            <div>
              <label className="text-sm font-semibold text-gray-300 mb-2 block">Select Labs to Order:</label>
              <div className="space-y-2">
                {['Blood culture', 'CBC', 'CMP', 'Lactate', 'Troponin', 'D-dimer', 'Procalcitonin'].map(lab => (
                  <label key={lab} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      defaultChecked={actionDetails[selectedActionType]?.labs?.includes(lab)}
                      onChange={(e) => {
                        const labs = actionDetails[selectedActionType]?.labs || []
                        const newLabs = e.target.checked
                          ? [...labs, lab]
                          : labs.filter(l => l !== lab)
                        handleDetailChange(selectedActionType, 'labs', newLabs)
                      }}
                      className="rounded"
                    />
                    <span className="text-sm text-gray-300">{lab}</span>
                  </label>
                ))}
              </div>
            </div>
          )}

          {selectedActionType === 'diagnose' && (
            <div>
              <label className="text-sm font-semibold text-gray-300 mb-2 block">Your Diagnosis:</label>
              <textarea
                value={actionDetails[selectedActionType]?.diagnosis || ''}
                onChange={(e) => handleDetailChange(selectedActionType, 'diagnosis', e.target.value)}
                placeholder="Enter your diagnosis..."
                className="w-full p-3 bg-black/30 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-medical"
                rows="3"
              />
            </div>
          )}

          {selectedActionType === 'recommend_treatment' && (
            <div>
              <label className="text-sm font-semibold text-gray-300 mb-2 block">Treatment Plan:</label>
              <textarea
                value={actionDetails[selectedActionType]?.treatment || ''}
                onChange={(e) => handleDetailChange(selectedActionType, 'treatment', e.target.value)}
                placeholder="Enter your treatment recommendations..."
                className="w-full p-3 bg-black/30 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-medical"
                rows="4"
              />
            </div>
          )}

          {/* Submit Button */}
          <button
            onClick={() => handleActionSubmit(selectedActionType)}
            disabled={loading}
            className="btn-primary w-full"
          >
            {loading ? 'Processing...' : 'Submit Action'}
          </button>
        </div>
      )}

      {/* AI Agent Button */}
      <div className="border-t border-white/10 pt-4">
        <button
          onClick={handleUseAgent}
          disabled={loading || isDeciding}
          className="btn-secondary w-full flex items-center justify-center gap-2"
        >
          <span>🤖</span>
          <span>{isDeciding ? 'AI Thinking...' : 'Let AI Decide'}</span>
        </button>
        {agentAction && (
          <div className="mt-3 p-3 bg-medical/10 border border-medical/20 rounded-lg text-sm">
            <p className="text-gray-300"><strong>AI Reasoning:</strong></p>
            <p className="text-white mt-1">{agentAction.reasoning}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default ActionPanel
