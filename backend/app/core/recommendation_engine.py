import json
from pathlib import Path
from typing import List, Dict
from ..models import Recommendation, ThreatType


class RecommendationEngine:
    """Generate and manage mitigation recommendations."""

    def __init__(self, mitigations_path: str, impact_rules_path: str):
        self.mitigations = self._load_json(mitigations_path)
        self.impact_rules = self._load_json(impact_rules_path)

    def _load_json(self, path: str) -> Dict:
        """Load JSON file."""
        with open(path, "r") as f:
            return json.load(f)

    def get_recommendations(self, threat_type: str) -> List[Recommendation]:
        """Get recommendations for a threat type."""
        threat_mitigations = self.mitigations.get(threat_type, {})

        recommendations = []
        priority = 1

        for action_name, action_details in threat_mitigations.items():
            recommendation = Recommendation(
                id=f"{threat_type}_{action_name}",
                action=action_details.get("description", action_name),
                threat_type=ThreatType[threat_type],
                expected_risk_reduction=action_details.get("risk_reduction", 0.3),
                priority=priority,
            )
            recommendations.append(recommendation)
            priority += 1

        return recommendations

    def calculate_impact_reduction(
        self, threat_type: str, mitigation_action: str
    ) -> float:
        """Calculate risk reduction for a mitigation."""
        threat_mitigations = self.mitigations.get(threat_type, {})
        action_config = threat_mitigations.get(mitigation_action, {})
        return action_config.get("risk_reduction", 0.3)

    def predict_impact(self, threat_type: str, current_risk: int) -> Dict:
        """Predict operational impact of a threat."""
        impact_info = self.impact_rules.get(threat_type, {})

        affected_subsystems = impact_info.get("affected_subsystems", [])
        impact_on_subsystems = impact_info.get("impact_on_subsystems", {})
        operational_consequences = impact_info.get("operational_consequences", {})

        return {
            "affected_subsystems": affected_subsystems,
            "impact_on_subsystems": impact_on_subsystems,
            "operational_consequences": operational_consequences,
            "current_risk": current_risk,
        }

    def apply_mitigation(self, threat_type: str, mitigation_action: str, current_risk: int) -> int:
        """Apply mitigation and calculate new risk."""
        risk_reduction = self.calculate_impact_reduction(threat_type, mitigation_action)
        new_risk = max(0, int(current_risk * (1 - risk_reduction)))
        return new_risk


# Global recommendation engine instance
_engine: RecommendationEngine = None


def initialize_engine(mitigations_path: str, impact_rules_path: str) -> RecommendationEngine:
    """Initialize global recommendation engine."""
    global _engine
    _engine = RecommendationEngine(mitigations_path, impact_rules_path)
    return _engine


def get_engine() -> RecommendationEngine:
    """Get global recommendation engine instance."""
    global _engine
    if _engine is None:
        raise ValueError("Engine not initialized. Call initialize_engine() first.")
    return _engine
