import React from 'react'
import { getHealthColor } from '../utils/colors'
import { formatRisk } from '../utils/formatters'

export const SubsystemCard = ({ name, status, riskScore, impactLevel }) => {
  const bgColor = getHealthColor(riskScore)
  
  const statusText = {
    'healthy': '✓ Healthy',
    'warning': '⚠ Warning',
    'critical': '✗ Critical'
  }

  return (
    <div className="bg-white border-2 rounded-lg p-4 shadow-md hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <h3 className="font-bold text-lg capitalize">{name}</h3>
        <div
          className="w-6 h-6 rounded-full"
          style={{ backgroundColor: bgColor }}
          title={status}
        />
      </div>
      
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600">Status:</span>
          <span className="font-semibold">{statusText[status]}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Risk Score:</span>
          <span className="font-semibold">{formatRisk(riskScore)}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
          <div
            className="h-2 rounded-full transition-all duration-300"
            style={{
              width: `${riskScore}%`,
              backgroundColor: bgColor
            }}
          />
        </div>
      </div>
    </div>
  )
}

export default SubsystemCard
