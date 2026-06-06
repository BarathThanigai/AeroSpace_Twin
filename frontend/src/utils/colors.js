export const COLORS = {
  healthy: '#4CAF50',
  warning: '#FFA500',
  critical: '#FF6B6B',
  normal: '#2196F3',
  border: '#E0E0E0',
  text: '#333333',
  lightText: '#666666',
}

export const getStatusColor = (status) => {
  switch (status) {
    case 'healthy':
      return COLORS.healthy
    case 'warning':
      return COLORS.warning
    case 'critical':
      return COLORS.critical
    default:
      return COLORS.normal
  }
}

export const getHealthColor = (riskScore) => {
  if (riskScore <= 20) return COLORS.healthy
  if (riskScore <= 60) return COLORS.warning
  return COLORS.critical
}
