from typing import Optional, Dict
from ..models import Aircraft, HealthStatus, Subsystem


class DigitalTwin:
    """Manages the virtual aircraft representation and state."""

    def __init__(self):
        self.aircraft: Optional[Aircraft] = None
        self.state_history = []
        self.threat_level = "normal"

    def update_state(self, aircraft: Aircraft):
        """Update digital twin with new aircraft state."""
        self.aircraft = aircraft

        # Store in history
        self.state_history.append(
            {
                "timestamp": aircraft.timestamp,
                "overall_risk": aircraft.overall_risk,
                "overall_status": aircraft.overall_status,
            }
        )

        # Keep only last 100 states
        if len(self.state_history) > 100:
            self.state_history.pop(0)

        # Update threat level based on overall status
        if aircraft.overall_status == HealthStatus.CRITICAL:
            self.threat_level = "critical"
        elif aircraft.overall_status == HealthStatus.WARNING:
            self.threat_level = "warning"
        else:
            self.threat_level = "normal"

    def get_subsystem_status(self, subsystem_name: str) -> Optional[Subsystem]:
        """Get current subsystem status."""
        if not self.aircraft:
            return None
        return getattr(self.aircraft, subsystem_name, None)

    def get_affected_subsystems(self, subsystem_names: list) -> Dict:
        """Get status of specific subsystems."""
        if not self.aircraft:
            return {}

        result = {}
        for name in subsystem_names:
            subsystem = getattr(self.aircraft, name, None)
            if subsystem:
                result[name] = {
                    "status": subsystem.status,
                    "risk_score": subsystem.risk_score,
                    "impact_level": subsystem.impact_level,
                }
        return result

    def get_full_state(self) -> Dict:
        """Get complete aircraft state."""
        if not self.aircraft:
            return {}

        return {
            "id": self.aircraft.id,
            "timestamp": self.aircraft.timestamp.isoformat(),
            "overall_risk": self.aircraft.overall_risk,
            "overall_status": self.aircraft.overall_status,
            "threat_level": self.threat_level,
            "subsystems": {
                "navigation": {
                    "status": self.aircraft.navigation.status,
                    "risk_score": self.aircraft.navigation.risk_score,
                    "current_value": round(self.aircraft.navigation.current_value, 2),
                    "impact_level": self.aircraft.navigation.impact_level,
                },
                "flight_control": {
                    "status": self.aircraft.flight_control.status,
                    "risk_score": self.aircraft.flight_control.risk_score,
                    "current_value": round(self.aircraft.flight_control.current_value, 2),
                    "impact_level": self.aircraft.flight_control.impact_level,
                },
                "communication": {
                    "status": self.aircraft.communication.status,
                    "risk_score": self.aircraft.communication.risk_score,
                    "current_value": round(self.aircraft.communication.current_value, 2),
                    "impact_level": self.aircraft.communication.impact_level,
                },
                "engine": {
                    "status": self.aircraft.engine.status,
                    "risk_score": self.aircraft.engine.risk_score,
                    "current_value": round(self.aircraft.engine.current_value, 2),
                    "impact_level": self.aircraft.engine.impact_level,
                },
                "sensors": {
                    "status": self.aircraft.sensors.status,
                    "risk_score": self.aircraft.sensors.risk_score,
                    "current_value": round(self.aircraft.sensors.current_value, 2),
                    "impact_level": self.aircraft.sensors.impact_level,
                },
            },
        }

    def get_history(self, limit: int = 50) -> list:
        """Get state history."""
        return self.state_history[-limit:]


# Global digital twin instance
_twin: DigitalTwin = None


def initialize_twin() -> DigitalTwin:
    """Initialize global digital twin."""
    global _twin
    _twin = DigitalTwin()
    return _twin


def get_twin() -> DigitalTwin:
    """Get global digital twin instance."""
    global _twin
    if _twin is None:
        _twin = DigitalTwin()
    return _twin
