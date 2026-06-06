import { useState, useEffect, useCallback } from 'react'
import { api } from '../services/api'

export const useIncident = () => {
  const [incident, setIncident] = useState(null)
  const [alerts, setAlerts] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchAlerts = useCallback(async () => {
    try {
      const data = await api.getAlerts()
      setAlerts(data)
    } catch (err) {
      setError(err.message)
    }
  }, [])

  const fetchRecommendations = useCallback(async () => {
    try {
      const data = await api.getRecommendations()
      if (data.recommendations) {
        setRecommendations(data.recommendations)
      }
    } catch (err) {
      setError(err.message)
    }
  }, [])

  const startAttack = useCallback(async (type) => {
    setLoading(true)
    try {
      let result
      if (type === 'gps') result = await api.simulateGPSSpoofing(1.0)
      else if (type === 'sensor') result = await api.simulateSensorAttack(1.0)
      else if (type === 'network') result = await api.simulateNetworkAttack(1.0)
      
      setIncident({ status: 'attack_started', type })
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  const applyMitigation = useCallback(async (action) => {
    try {
      const result = await api.applyMitigation(action)
      return result
    } catch (err) {
      setError(err.message)
      return null
    }
  }, [])

  const endIncident = useCallback(async () => {
    try {
      const result = await api.endIncident()
      setIncident(null)
      setRecommendations([])
      return result
    } catch (err) {
      setError(err.message)
      return null
    }
  }, [])

  useEffect(() => {
    const interval = setInterval(fetchAlerts, 1500)
    return () => clearInterval(interval)
  }, [fetchAlerts])

  return {
    incident,
    alerts,
    recommendations,
    loading,
    error,
    startAttack,
    applyMitigation,
    endIncident,
    fetchRecommendations,
  }
}
