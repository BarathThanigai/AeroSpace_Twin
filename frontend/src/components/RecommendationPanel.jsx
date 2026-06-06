import React, { useState } from 'react'

export const RecommendationPanel = ({ recommendations, onApply, isApplying }) => {
  const [selectedMitigation, setSelectedMitigation] = useState(null)

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4">Recommended Mitigations</h2>
        <div className="text-center text-gray-500 py-8">No recommendations available</div>
      </div>
    )
  }

  const handleApply = async (action) => {
    setSelectedMitigation(action)
    await onApply(action)
    setTimeout(() => setSelectedMitigation(null), 1000)
  }

  return (
    <div className="bg-white rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Recommended Mitigations</h2>
      
      <div className="space-y-3">
        {recommendations.map((rec, idx) => (
          <div key={rec.id || idx} className="border border-blue-200 rounded p-4 bg-blue-50">
            <div className="flex justify-between items-start mb-2">
              <div>
                <h3 className="font-bold text-blue-900">{rec.action}</h3>
                <p className="text-sm text-blue-700">
                  Priority: {rec.priority} | Expected Risk Reduction: {(rec.expected_risk_reduction * 100).toFixed(0)}%
                </p>
              </div>
            </div>
            
            <button
              onClick={() => handleApply(rec.action)}
              disabled={isApplying || selectedMitigation !== null}
              className="mt-3 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded transition-colors"
            >
              {selectedMitigation === rec.action ? '✓ Applied' : 'Apply Mitigation'}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default RecommendationPanel
