from fastapi import APIRouter
from typing import Dict, Any
from ..data.stream import get_stream
from ..ml.anomaly_detector import get_detector
from ..ml.threat_classifier import get_classifier
from ..core.digital_twin import get_twin
from ..core.incident_manager import get_manager
from ..core.recommendation_engine import get_engine
from ..utils.report_generator import ReportGenerator
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AeroShield Twin"}


@router.get("/systems")
async def get_aircraft_systems() -> Dict[str, Any]:
    """Get current aircraft system status."""
    try:
        twin = get_twin()
        state = twin.get_full_state()
        logger.info("Aircraft systems retrieved")
        return state
    except Exception as e:
        logger.error(f"Error retrieving aircraft systems: {e}")
        return {"error": str(e)}


@router.get("/digital-twin")
async def get_digital_twin() -> Dict[str, Any]:
    """Get full digital twin state."""
    try:
        twin = get_twin()
        return twin.get_full_state()
    except Exception as e:
        logger.error(f"Error getting digital twin: {e}")
        return {"error": str(e)}


@router.get("/alerts")
async def get_alerts() -> Dict[str, Any]:
    """Get current anomaly alerts."""
    try:
        stream = get_stream()
        aircraft = stream.current_aircraft

        if not aircraft:
            return {"alerts": [], "status": "no_aircraft_data"}

        detector = get_detector()
        if not detector.is_trained:
            return {"alerts": [], "status": "detector_not_trained"}

        is_anomaly, confidence, score, features = detector.detect(aircraft)

        if is_anomaly:
            classifier = get_classifier()
            threat = classifier.classify(aircraft, features, confidence)

            return {
                "anomaly_detected": True,
                "confidence": round(confidence, 2),
                "anomaly_score": round(score, 4),
                "features": {k: round(v, 2) for k, v in features.items()},
                "threat_type": threat.threat_type.value,
                "threat_confidence": round(threat.confidence, 2),
                "affected_subsystems": threat.affected_subsystems,
                "timestamp": aircraft.timestamp.isoformat(),
            }
        else:
            return {
                "anomaly_detected": False,
                "confidence": round(confidence, 2),
                "timestamp": aircraft.timestamp.isoformat(),
            }
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return {"error": str(e)}


@router.post("/simulate/gps-spoof")
async def simulate_gps_spoofing(severity: float = 1.0) -> Dict[str, Any]:
    """Start GPS spoofing attack simulation."""
    try:
        stream = get_stream()
        stream.start_attack("gps_spoofing", severity)

        manager = get_manager()
        manager.create_incident(
            threat_type="GPS_Spoofing",
            threat_confidence=0.0,
            affected_subsystems=["navigation", "flight_control"],
            initial_risk=60,
        )

        logger.info(f"GPS spoofing attack started with severity {severity}")
        return {
            "status": "attack_started",
            "attack_type": "gps_spoofing",
            "severity": severity,
        }
    except Exception as e:
        logger.error(f"Error starting GPS spoofing: {e}")
        return {"error": str(e)}


@router.post("/simulate/sensor-attack")
async def simulate_sensor_anomaly(severity: float = 1.0) -> Dict[str, Any]:
    """Start sensor anomaly attack simulation."""
    try:
        stream = get_stream()
        stream.start_attack("sensor_anomaly", severity)

        manager = get_manager()
        manager.create_incident(
            threat_type="Sensor_Anomaly",
            threat_confidence=0.0,
            affected_subsystems=["sensors", "engine"],
            initial_risk=50,
        )

        logger.info(f"Sensor anomaly attack started with severity {severity}")
        return {
            "status": "attack_started",
            "attack_type": "sensor_anomaly",
            "severity": severity,
        }
    except Exception as e:
        logger.error(f"Error starting sensor attack: {e}")
        return {"error": str(e)}


@router.post("/simulate/network-attack")
async def simulate_network_intrusion(severity: float = 1.0) -> Dict[str, Any]:
    """Start network intrusion attack simulation."""
    try:
        stream = get_stream()
        stream.start_attack("communication_anomaly", severity)

        manager = get_manager()
        manager.create_incident(
            threat_type="Network_Intrusion",
            threat_confidence=0.0,
            affected_subsystems=["communication", "flight_control"],
            initial_risk=70,
        )

        logger.info(f"Network intrusion attack started with severity {severity}")
        return {
            "status": "attack_started",
            "attack_type": "network_intrusion",
            "severity": severity,
        }
    except Exception as e:
        logger.error(f"Error starting network attack: {e}")
        return {"error": str(e)}


@router.post("/stop-attack")
async def stop_attack() -> Dict[str, Any]:
    """Stop current attack simulation."""
    try:
        stream = get_stream()
        stream.stop_attack()
        logger.info("Attack stopped")
        return {"status": "attack_stopped"}
    except Exception as e:
        logger.error(f"Error stopping attack: {e}")
        return {"error": str(e)}


@router.get("/recommendations")
async def get_recommendations() -> Dict[str, Any]:
    """Get mitigation recommendations for current threat."""
    try:
        manager = get_manager()
        incident = manager.get_current_incident()

        if not incident:
            return {"recommendations": [], "message": "No active incident"}

        threat_type = incident["threat_type"]
        engine = get_engine()
        recommendations = engine.get_recommendations(threat_type)

        return {
            "incident_id": incident["incident_id"],
            "threat_type": threat_type,
            "recommendations": [
                {
                    "id": r.id,
                    "action": r.action,
                    "expected_risk_reduction": r.expected_risk_reduction,
                    "priority": r.priority,
                }
                for r in recommendations
            ],
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return {"error": str(e)}


@router.post("/apply-mitigation")
async def apply_mitigation(mitigation_action: str) -> Dict[str, Any]:
    """Apply a mitigation action."""
    try:
        manager = get_manager()
        incident = manager.get_current_incident()

        if not incident:
            return {"error": "No active incident"}

        threat_type = incident["threat_type"]
        current_risk = incident["current_risk"]

        engine = get_engine()
        new_risk = engine.apply_mitigation(threat_type, mitigation_action, current_risk)

        manager.apply_mitigation(mitigation_action, new_risk)

        logger.info(
            f"Mitigation applied: {mitigation_action}. Risk reduced from {current_risk} to {new_risk}"
        )

        return {
            "status": "mitigation_applied",
            "action": mitigation_action,
            "previous_risk": current_risk,
            "new_risk": new_risk,
            "risk_reduction": round((current_risk - new_risk) / current_risk * 100, 1),
        }
    except Exception as e:
        logger.error(f"Error applying mitigation: {e}")
        return {"error": str(e)}


@router.post("/end-incident")
async def end_incident() -> Dict[str, Any]:
    """End current incident and generate report."""
    try:
        manager = get_manager()
        incident = manager.get_current_incident()

        if not incident:
            return {"status": "no_active_incident"}

        manager.end_current_incident()
        logger.info(f"Incident {incident['incident_id']} ended")

        return {"status": "incident_ended", "incident_id": incident["incident_id"]}
    except Exception as e:
        logger.error(f"Error ending incident: {e}")
        return {"error": str(e)}


@router.get("/report")
async def get_incident_report() -> Dict[str, Any]:
    """Get current incident report."""
    try:
        manager = get_manager()
        twin = get_twin()

        incident = manager.get_current_incident()
        if not incident:
            return {"error": "No active incident"}

        aircraft_state = twin.get_full_state()

        report_gen = ReportGenerator()
        report = report_gen.generate_json_report(manager, aircraft_state, 0.0)

        # Save JSON report
        saved_path = report_gen.save_report(report)

        # Try to generate PDF
        pdf_path = report_gen.generate_pdf_report(report)

        return {
            "status": "report_generated",
            "json_path": saved_path,
            "pdf_path": pdf_path,
            "report_data": report,
        }
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {"error": str(e)}


@router.get("/incident-history")
async def get_incident_history(limit: int = 10) -> Dict[str, Any]:
    """Get incident history."""
    try:
        manager = get_manager()
        history = manager.get_incident_history(limit)
        return {"incidents": history}
    except Exception as e:
        logger.error(f"Error getting incident history: {e}")
        return {"error": str(e)}
