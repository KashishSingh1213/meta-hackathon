import { useState, useCallback } from 'react'
import { cliniqAPI } from '../api/client.js'

export const useEnvironment = () => {
  const [observation, setObservation] = useState(null)
  const [state, setState] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [stepCount, setStepCount] = useState(0)
  const [totalReward, setTotalReward] = useState(0)
  const [episodeDone, setEpisodeDone] = useState(false)

  const reset = useCallback(async (task) => {
    setLoading(true)
    setError(null)
    try {
      const response = await cliniqAPI.resetEnvironment(task)
      setObservation(response.data)
      setStepCount(0)
      setTotalReward(0)
      setEpisodeDone(false)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reset environment')
    } finally {
      setLoading(false)
    }
  }, [])

  const step = useCallback(async (action) => {
    setLoading(true)
    setError(null)
    try {
      const response = await cliniqAPI.takeAction(action)
      const result = response.data
      setObservation(result.observation)
      setStepCount(prev => prev + 1)
      setTotalReward(prev => prev + result.reward)
      setEpisodeDone(result.done)
      return result
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to take action')
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  const getState = useCallback(async () => {
    try {
      const response = await cliniqAPI.getState()
      setState(response.data)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get state')
    }
  }, [])

  return {
    observation,
    state,
    loading,
    error,
    stepCount,
    totalReward,
    episodeDone,
    reset,
    step,
    getState,
  }
}
