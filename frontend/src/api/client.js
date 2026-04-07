import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

export const cliniqAPI = {
  health: () => api.get('/api/health'),
  getTasks: () => api.get('/api/tasks'),
  resetEnvironment: (task, seed = null) =>
    api.post('/api/reset', { task, seed }),
  getState: () => api.get('/api/state'),
  takeAction: (action) =>
    api.post('/api/step', { action }),
  getAgentDecision: (observation, context = null) =>
    api.post('/api/agent/decide', { observation, context }),
  getEpisodeSummary: () => api.get('/api/episode/summary'),
}

export default api
