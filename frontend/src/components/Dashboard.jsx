import React from 'react'
import DigitalTwin from './DigitalTwin'
import ThreatPanel from './ThreatPanel'
import ImpactPanel from './ImpactPanel'
import RecommendationPanel from './RecommendationPanel'
import ControlPanel from './ControlPanel'
import IncidentTimeline from './IncidentTimeline'
import { useAircraft } from '../hooks/useAircraft'
import { useIncident } from '../hooks/useIncident'

export const Dashboard = () => {
  const { aircraft, loading: aircraftLoading } = useAircraft()
  const {
    incident,
    alerts,
    recommendations,
    loading: incidentLoading,
    startAttack,
    applyMitigation,
    endIncident,
    fetchRecommendations,
  } = useIncident()

  React.useEffect(() => {
    if (alerts && alerts.anomaly_detected) {
      fetchRecommendations()
    }
  }, [alerts, fetchRecommendations])

  const hasAlert = alerts && alerts.anomaly_detected
  const isAttacking = incident && incident.status === 'attack_started'

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-2">AeroShield Twin</h1>
          <p className="text-xl text-gray-600">AI-Powered Cybersecurity Digital Twin for Aircraft Systems</p>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Left Column - Digital Twin */}
          <div className="lg:col-span-3">
            <DigitalTwin aircraft={aircraft} />
          </div>

          {/* Threat Panel */}
          <div>
            <ThreatPanel alerts={alerts} isLoading={aircraftLoading} />
          </div>

          {/* Impact Panel */}
          <div>
            <ImpactPanel alerts={alerts} aircraft={aircraft} />
          </div>

          {/* Control Panel */}
          <div>
            <ControlPanel
              onStartAttack={startAttack}
              onStopAttack={() => {}}
              onEndIncident={endIncident}
              isAttacking={isAttacking}
              isLoading={incidentLoading}
            />
          </div>
        </div>

        {/* Timeline */}
        <div className="mb-6">
          <IncidentTimeline
            currentStage={alerts?.threat_type || 'normal'}
            hasAlert={hasAlert}
            hasMitigation={false}
          />
        </div>

        {/* Recommendations */}
        {hasAlert && (
          <div className="mb-6">
            <RecommendationPanel
              recommendations={recommendations}
              onApply={applyMitigation}
              isApplying={incidentLoading}
            />
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center text-gray-600 text-sm">
          <p>Real-time monitoring and threat response for aircraft cybersecurity</p>
          <p className="mt-1">Version 1.0.0 • Powered by AeroShield Intelligence</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
