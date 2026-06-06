import json
from pathlib import Path
from typing import Dict, List, Tuple
from ..models import ThreatClassification, ThreatType, Aircraft


class ThreatClassifier:
    """Rule-based threat classification."""

    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)
        self.threat_types = list(self.rules.keys())

    def _load_rules(self, rules_path: str) -> Dict:
        """Load threat classification rules from JSON."""
        with open(rules_path, "r") as f:
            return json.load(f)

    def classify(
        self, aircraft: Aircraft, features: Dict[str, float], anomaly_confidence: float
    ) -> ThreatClassification:
        """Classify detected anomalies into threat types."""

        threat_scores = {}

        # Analyze patterns to classify threat
        nav_risk = aircraft.navigation.risk_score
        comm_risk = aircraft.communication.risk_score
        eng_risk = aircraft.engine.risk_score
        sens_risk = aircraft.sensors.risk_score
        fc_risk = aircraft.flight_control.risk_score

        # GPS Spoofing: High navigation risk + heading errors
        gps_score = 0
        if nav_risk > 70:
            gps_score += 40
        if features.get("navigation", 0) < 40:
            gps_score += 30
        threat_scores["GPS_Spoofing"] = gps_score * (anomaly_confidence / 100)

        # Sensor Anomaly: High engine + sensor risk
        sensor_score = 0
        if eng_risk > 60 and sens_risk > 60:
            sensor_score += 50
        if eng_risk > 75:
            sensor_score += 30
        threat_scores["Sensor_Anomaly"] = sensor_score * (anomaly_confidence / 100)

        # Communication Anomaly: High communication risk only
        comm_score = 0
        if comm_risk > 70:
            comm_score += 60
        threat_scores["Communication_Anomaly"] = comm_score * (anomaly_confidence / 100)

        # Network Intrusion: Multiple subsystems affected
        net_score = 0
        high_risk_subsystems = sum(
            1 for risk in [nav_risk, comm_risk, eng_risk, sens_risk, fc_risk] if risk > 60
        )
        if high_risk_subsystems >= 2:
            net_score += 40 + (high_risk_subsystems * 10)
        threat_scores["Network_Intrusion"] = net_score * (anomaly_confidence / 100)

        # Unknown: Catch-all
        threat_scores["Unknown"] = 20

        # Find the highest scoring threat
        classified_threat = max(threat_scores, key=threat_scores.get)
        confidence = min(95, threat_scores[classified_threat])

        # Get affected subsystems from rules
        threat_info = self.rules.get(classified_threat, {})
        affected_subsystems = threat_info.get("affected_subsystems", ["sensors"])

        return ThreatClassification(
            threat_type=ThreatType[classified_threat],
            confidence=confidence,
            affected_subsystems=affected_subsystems,
            description=f"Detected {classified_threat} with {confidence:.1f}% confidence",
        )

    def get_threat_info(self, threat_type: str) -> Dict:
        """Get threat information from rules."""
        return self.rules.get(threat_type, {})


# Global classifier instance
_classifier: ThreatClassifier = None


def initialize_classifier(rules_path: str) -> ThreatClassifier:
    """Initialize global threat classifier."""
    global _classifier
    _classifier = ThreatClassifier(rules_path)
    return _classifier


def get_classifier() -> ThreatClassifier:
    """Get global threat classifier instance."""
    global _classifier
    if _classifier is None:
        raise ValueError("Classifier not initialized. Call initialize_classifier() first.")
    return _classifier
