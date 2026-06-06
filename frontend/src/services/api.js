export const API_BASE_URL = 'http://localhost:8000'

export const api = {
  async getHealth() {
    return fetch(`${API_BASE_URL}/health`).then(r => r.json())
  },

  async getSystems() {
    return fetch(`${API_BASE_URL}/systems`).then(r => r.json())
  },

  async getDigitalTwin() {
    return fetch(`${API_BASE_URL}/digital-twin`).then(r => r.json())
  },

  async getAlerts() {
    return fetch(`${API_BASE_URL}/alerts`).then(r => r.json())
  },

  async simulateGPSSpoofing(severity = 1.0) {
    return fetch(`${API_BASE_URL}/simulate/gps-spoof`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ severity })
    }).then(r => r.json())
  },

  async simulateSensorAttack(severity = 1.0) {
    return fetch(`${API_BASE_URL}/simulate/sensor-attack`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ severity })
    }).then(r => r.json())
  },

  async simulateNetworkAttack(severity = 1.0) {
    return fetch(`${API_BASE_URL}/simulate/network-attack`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ severity })
    }).then(r => r.json())
  },

  async stopAttack() {
    return fetch(`${API_BASE_URL}/stop-attack`, {
      method: 'POST'
    }).then(r => r.json())
  },

  async getRecommendations() {
    return fetch(`${API_BASE_URL}/recommendations`).then(r => r.json())
  },

  async applyMitigation(action) {
    return fetch(`${API_BASE_URL}/apply-mitigation?mitigation_action=${encodeURIComponent(action)}`, {
      method: 'POST'
    }).then(r => r.json())
  },

  async endIncident() {
    return fetch(`${API_BASE_URL}/end-incident`, {
      method: 'POST'
    }).then(r => r.json())
  },

  async getReport() {
    return fetch(`${API_BASE_URL}/report`).then(r => r.json())
  },

  async getIncidentHistory(limit = 10) {
    return fetch(`${API_BASE_URL}/incident-history?limit=${limit}`).then(r => r.json())
  }
}
