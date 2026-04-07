import { useState, useCallback } from 'react'
import { cliniqAPI } from '../api/client.js'

export const useAgent = () => {
  const [isDeciding, setIsDeciding] = useState(false)
  const [agentAction, setAgentAction] = useState(null)
  const [error, setError] = useState(null)

  const decide = useCallback(async (observation, context = null) => {
    setIsDeciding(true)
    setError(null)
    try {
      const response = await cliniqAPI.getAgentDecision(observation, context)
      const decision = response.data
      setAgentAction(decision)
      return decision
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to get agent decision'
      setError(message)
      return null
    } finally {
      setIsDeciding(false)
    }
  }, [])

  return {
    isDeciding,
    agentAction,
    error,
    decide,
  }
}
