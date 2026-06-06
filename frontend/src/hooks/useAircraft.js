import { useState, useEffect, useCallback } from 'react'
import { api } from '../services/api'

export const useAircraft = () => {
  const [aircraft, setAircraft] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchAircraft = useCallback(async () => {
    try {
      const data = await api.getDigitalTwin()
      setAircraft(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchAircraft()
    const interval = setInterval(fetchAircraft, 1500)
    return () => clearInterval(interval)
  }, [fetchAircraft])

  return { aircraft, loading, error, refetch: fetchAircraft }
}
