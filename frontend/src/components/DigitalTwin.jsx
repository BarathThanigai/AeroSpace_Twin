import React from 'react'
import SubsystemCard from './SubsystemCard'

export const DigitalTwin = ({ aircraft }) => {
  if (!aircraft || !aircraft.subsystems) {
    return (
      <div className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-6">Aircraft Digital Twin</h2>
        <div className="text-center text-gray-500 py-8">Loading aircraft data...</div>
      </div>
    )
  }

  const { subsystems, overall_risk, overall_status } = aircraft

  return (
    <div className="bg-white rounded-lg p-6 shadow-md">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Aircraft Digital Twin</h2>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="text-lg font-semibold">
              Overall Status: <span className="capitalize">{overall_status}</span>
            </div>
            <div className="text-lg font-semibold">
              Overall Risk: <span className="text-red-600">{Math.round(overall_risk)}%</span>
            </div>
          </div>
          <div className="w-12 h-12 rounded-full flex items-center justify-center text-2xl"
            style={{
              backgroundColor: overall_status === 'healthy' ? '#4CAF50' : 
                              overall_status === 'warning' ? '#FFA500' : '#FF6B6B'
            }}>
            {overall_status === 'healthy' ? '✓' : 
             overall_status === 'warning' ? '⚠' : '✗'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {Object.entries(subsystems).map(([name, subsystem]) => (
          <SubsystemCard
            key={name}
            name={name}
            status={subsystem.status}
            riskScore={subsystem.risk_score}
            impactLevel={subsystem.impact_level}
          />
        ))}
      </div>
    </div>
  )
}

export default DigitalTwin
