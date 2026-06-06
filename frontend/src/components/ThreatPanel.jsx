import React from 'react'
import { formatConfidence, formatTimestamp } from '../utils/formatters'

export const ThreatPanel = ({ alerts, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4">Threat Detection</h2>
        <div className="text-center text-gray-500 py-8">Loading...</div>
      </div>
    )
  }

  if (!alerts || !alerts.anomaly_detected) {
    return (
      <div className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4">Threat Detection</h2>
        <div className="bg-green-50 border border-green-300 rounded p-4">
          <div className="flex items-center gap-3">
            <span className="text-2xl">✓</span>
            <div>
              <p className="font-semibold text-green-800">No Threats Detected</p>
              <p className="text-sm text-green-700">Aircraft systems operating normally</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Threat Detection</h2>
      <div className="bg-red-50 border-2 border-red-400 rounded p-4">
        <div className="flex items-start gap-4">
          <span className="text-3xl">⚠️</span>
          <div className="flex-1">
            <h3 className="text-xl font-bold text-red-700">{alerts.threat_type}</h3>
            <div className="mt-3 space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Confidence:</span>
                <span className="font-semibold">{formatConfidence(alerts.threat_confidence)}</span>
              </div>
              <div className="flex justify-between">
                <span>Anomaly Score:</span>
                <span className="font-semibold">{alerts.anomaly_score.toFixed(4)}</span>
              </div>
              <div className="flex justify-between">
                <span>Detected:</span>
                <span className="font-semibold">{formatTimestamp(alerts.timestamp)}</span>
              </div>
              <div className="mt-2 pt-2 border-t border-red-200">
                <p className="text-gray-700"><span className="font-semibold">Affected Systems:</span></p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {alerts.affected_subsystems.map(subsystem => (
                    <span key={subsystem} className="bg-red-200 text-red-800 px-2 py-1 rounded text-xs font-semibold">
                      {subsystem}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ThreatPanel
