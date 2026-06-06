export const formatRisk = (risk) => {
  return Math.round(risk) + '%'
}

export const formatConfidence = (confidence) => {
  return confidence.toFixed(1) + '%'
}

export const formatTime = (date) => {
  return new Date(date).toLocaleTimeString()
}

export const formatTimestamp = (date) => {
  return new Date(date).toLocaleString()
}

export const getStageEmoji = (stage) => {
  const emojis = {
    'normal': '✅',
    'attack': '⚠️',
    'detected': '🔍',
    'predicted': '📊',
    'mitigated': '🛡️',
    'resolved': '✔️',
  }
  return emojis[stage] || ''
}
