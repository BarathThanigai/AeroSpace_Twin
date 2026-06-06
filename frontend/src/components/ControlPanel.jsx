import React, { useState } from 'react'

export const ControlPanel = ({ onStartAttack, onStopAttack, onEndIncident, isAttacking, isLoading }) => {
  const [selectedAttack, setSelectedAttack] = useState(null)

  const attacks = [
    { id: 'gps', label: '🛰️ GPS Spoofing', description: 'Simulate GPS signal manipulation' },
    { id: 'sensor', label: '📊 Sensor Anomaly', description: 'Simulate sensor malfunction' },
    { id: 'network', label: '🔗 Network Intrusion', description: 'Simulate network attack' },
  ]

  const handleStartAttack = (attackType) => {
    setSelectedAttack(attackType)
    onStartAttack(attackType)
  }

  const handleStopAttack = () => {
    onStopAttack()
    setSelectedAttack(null)
  }

  return (
    <div className="bg-white rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Attack Simulation</h2>
      
      <div className="space-y-3 mb-6">
        {attacks.map(attack => (
          <button
            key={attack.id}
            onClick={() => handleStartAttack(attack.id)}
            disabled={isAttacking || isLoading}
            className="w-full text-left p-4 border-2 border-gray-300 rounded hover:border-red-500 hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <div className="flex justify-between items-center">
              <div>
                <h3 className="font-bold">{attack.label}</h3>
                <p className="text-sm text-gray-600">{attack.description}</p>
              </div>
              {selectedAttack === attack.id && isAttacking && (
                <span className="text-red-600 font-bold">ACTIVE ⚠️</span>
              )}
            </div>
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {isAttacking && (
          <>
            <button
              onClick={handleStopAttack}
              className="w-full bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-3 px-4 rounded transition-colors"
            >
              ⏹️ Stop Attack
            </button>
            <button
              onClick={onEndIncident}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded transition-colors"
            >
              ✓ End Incident & Generate Report
            </button>
          </>
        )}
        {!isAttacking && (
          <button
            disabled
            className="w-full bg-gray-300 text-gray-600 font-bold py-3 px-4 rounded cursor-not-allowed"
          >
            No Active Attack
          </button>
        )}
      </div>
    </div>
  )
}

export default ControlPanel
