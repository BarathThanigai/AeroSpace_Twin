import { useEffect, useRef } from 'react'

export const useWebSocket = (onMessage) => {
  const ws = useRef(null)

  useEffect(() => {
    // For now, we'll use polling instead of WebSocket
    // WebSocket can be added later for real-time updates
    const pollInterval = setInterval(onMessage, 1500)
    return () => clearInterval(pollInterval)
  }, [onMessage])

  return ws
}
