import React from 'react'

export const ImpactPanel = ({ alerts, aircraft }) => {
  if (!alerts || !alerts.anomaly_detected) {
    return (
      <div className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4">Impact Analysis</h2>
        <div className="text-center text-gray-500 py-8">No active threat</div>
      </div>
    )
  }

  const affectedSubsystems = alerts.affected_subsystems || []
  const impactLevel = affectedSubsystems.length > 2 ? 'Critical' : 
                      affectedSubsystems.length > 1 ? 'High' : 'Medium'

  return (
    <div className="bg-white rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Impact Analysis</h2>
      
      <div className="space-y-4">
        <div className="bg-red-50 border border-red-200 rounded p-4">
          <p className="text-sm text-gray-600">Predicted Impact Level</p>
          <p className="text-3xl font-bold text-red-700">{impactLevel}</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-yellow-50 border border-yellow-200 rounded p-4">
            <p className="text-sm text-gray-600">Systems at Risk</p>
            <p className="text-2xl font-bold text-yellow-700">{affectedSubsystems.length}</p>
          </div>

          <div className="bg-orange-50 border border-orange-200 rounded p-4">
            <p className="text-sm text-gray-600">Operational Risk</p>
            <p className="text-2xl font-bold text-orange-700">
              {aircraft && aircraft.overall_risk ? Math.round(aircraft.overall_risk) : '?'}%
            </p>
          </div>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded p-4">
          <p className="text-sm font-semibold text-gray-700 mb-2">Affected Subsystems:</p>
          <div className="flex flex-wrap gap-2">
            {affectedSubsystems.map(sys => (
              <span key={sys} className="bg-red-200 text-red-800 px-3 py-1 rounded text-sm font-semibold">
                {sys}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ImpactPanel
