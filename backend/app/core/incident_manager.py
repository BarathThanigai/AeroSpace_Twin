import json
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4
from ..models import Incident, ThreatType


class IncidentManager:
    """Manage incident lifecycle and tracking."""

    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.current_incident: Optional[Incident] = None

    def create_incident(
        self,
        threat_type: ThreatType,
        threat_confidence: float,
        affected_subsystems: List[str],
        initial_risk: int,
    ) -> Incident:
        """Create new incident."""
        incident = Incident(
            incident_id=str(uuid4())[:8],
            start_time=datetime.now(),
            threat_type=threat_type,
            threat_confidence=threat_confidence,
            affected_subsystems=affected_subsystems,
            initial_risk=initial_risk,
            current_risk=initial_risk,
            predicted_risk=initial_risk,
            recommendations=[],
            applied_mitigations=[],
            timeline_stage="attack",
        )

        self.incidents[incident.incident_id] = incident
        self.current_incident = incident
        return incident

    def update_incident_detection(self, predicted_risk: int):
        """Update incident when threat is detected."""
        if not self.current_incident:
            return

        self.current_incident.predicted_risk = predicted_risk
        self.current_incident.timeline_stage = "detected"

    def add_recommendations(self, recommendations):
        """Add recommendations to current incident."""
        if not self.current_incident:
            return

        self.current_incident.recommendations = recommendations
        self.current_incident.timeline_stage = "predicted"

    def apply_mitigation(self, mitigation_action: str, current_risk: int):
        """Apply mitigation and update risk."""
        if not self.current_incident:
            return

        self.current_incident.applied_mitigations.append(mitigation_action)
        self.current_incident.current_risk = current_risk
        self.current_incident.timeline_stage = "mitigated"

    def resolve_incident(self, final_risk: int):
        """Mark incident as resolved."""
        if not self.current_incident:
            return

        self.current_incident.final_risk = final_risk
        self.current_incident.resolution_time = datetime.now()
        self.current_incident.timeline_stage = "resolved"

    def get_current_incident(self) -> Optional[Dict]:
        """Get current incident as dictionary."""
        if not self.current_incident:
            return None

        return {
            "incident_id": self.current_incident.incident_id,
            "start_time": self.current_incident.start_time.isoformat(),
            "threat_type": self.current_incident.threat_type.value,
            "threat_confidence": self.current_incident.threat_confidence,
            "affected_subsystems": self.current_incident.affected_subsystems,
            "initial_risk": self.current_incident.initial_risk,
            "current_risk": self.current_incident.current_risk,
            "predicted_risk": self.current_incident.predicted_risk,
            "recommendations": [r.dict() for r in self.current_incident.recommendations]
            if self.current_incident.recommendations
            else [],
            "applied_mitigations": self.current_incident.applied_mitigations,
            "final_risk": self.current_incident.final_risk,
            "resolution_time": self.current_incident.resolution_time.isoformat()
            if self.current_incident.resolution_time
            else None,
            "timeline_stage": self.current_incident.timeline_stage,
        }

    def end_current_incident(self):
        """End the current incident and reset."""
        if self.current_incident:
            self.current_incident.timeline_stage = "resolved"
        self.current_incident = None

    def get_incident_history(self, limit: int = 10) -> List[Dict]:
        """Get recent incidents."""
        recent = list(self.incidents.values())[-limit:]
        return [
            {
                "incident_id": inc.incident_id,
                "threat_type": inc.threat_type.value,
                "start_time": inc.start_time.isoformat(),
                "initial_risk": inc.initial_risk,
                "final_risk": inc.final_risk,
            }
            for inc in recent
        ]


# Global incident manager instance
_manager: IncidentManager = None


def initialize_manager() -> IncidentManager:
    """Initialize global incident manager."""
    global _manager
    _manager = IncidentManager()
    return _manager


def get_manager() -> IncidentManager:
    """Get global incident manager instance."""
    global _manager
    if _manager is None:
        _manager = IncidentManager()
    return _manager
