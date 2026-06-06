import React from 'react'
import { getStageEmoji } from '../utils/formatters'

export const IncidentTimeline = ({ currentStage, hasAlert, hasMitigation }) => {
  const stages = [
    { id: 'normal', label: 'Normal Operation', active: !hasAlert && !hasMitigation },
    { id: 'attack', label: 'Attack Detected', active: hasAlert && !hasMitigation },
    { id: 'detected', label: 'Threat Classified', active: hasAlert && !hasMitigation },
    { id: 'predicted', label: 'Impact Predicted', active: hasAlert && !hasMitigation },
    { id: 'mitigated', label: 'Mitigation Applied', active: hasMitigation },
    { id: 'resolved', label: 'Resolved', active: false },
  ]

  return (
    <div className="bg-white rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-6">Incident Timeline</h2>
      
      <div className="relative">
        <div className="flex justify-between mb-8">
          {stages.map((stage, idx) => (
            <div key={stage.id} className="flex flex-col items-center flex-1">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold border-2 transition-all ${
                stage.active
                  ? 'bg-green-100 border-green-500 text-green-600'
                  : hasAlert && stages.slice(0, idx).some(s => s.active)
                  ? 'bg-blue-100 border-blue-500 text-blue-600'
                  : 'bg-gray-100 border-gray-300 text-gray-500'
              }`}>
                {stage.active ? '●' : '○'}
              </div>
              <p className="text-xs text-center mt-2 font-semibold">{stage.label}</p>
              {idx < stages.length - 1 && (
                <div className={`absolute top-6 left-1/2 w-full h-1 transition-all ${
                  stage.active ? 'bg-green-500' : hasAlert && idx < 2 ? 'bg-blue-500' : 'bg-gray-300'
                }`}
                  style={{
                    left: `${(idx + 1) * (100 / stages.length)}%`,
                    width: `${100 / stages.length}%`
                  }}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6 p-4 bg-gray-50 border border-gray-200 rounded">
        <p className="text-sm text-gray-700">
          {hasAlert
            ? hasMitigation
              ? 'Mitigation has been applied. System status improving...'
              : 'Threat detected! Review recommendations and apply mitigations.'
            : 'Aircraft systems operating normally.'}
        </p>
      </div>
    </div>
  )
}

export default IncidentTimeline
