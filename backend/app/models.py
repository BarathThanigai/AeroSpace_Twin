from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


class ThreatType(str, Enum):
    GPS_SPOOFING = "GPS_Spoofing"
    SENSOR_ANOMALY = "Sensor_Anomaly"
    COMMUNICATION_ANOMALY = "Communication_Anomaly"
    NETWORK_INTRUSION = "Network_Intrusion"
    UNKNOWN = "Unknown"


class Subsystem(BaseModel):
    name: str
    status: HealthStatus
    risk_score: int
    impact_level: int
    current_value: float
    threshold: float
    normal_range: tuple


class Aircraft(BaseModel):
    id: str
    timestamp: datetime
    navigation: Subsystem
    flight_control: Subsystem
    communication: Subsystem
    engine: Subsystem
    sensors: Subsystem
    overall_risk: int
    overall_status: HealthStatus


class AnomalyAlert(BaseModel):
    timestamp: datetime
    is_anomaly: bool
    confidence: float
    features: Dict[str, float]
    anomaly_score: float


class ThreatClassification(BaseModel):
    threat_type: ThreatType
    confidence: float
    affected_subsystems: List[str]
    description: str


class ImpactPrediction(BaseModel):
    timestamp: datetime
    predicted_risk: int
    affected_subsystems: List[str]
    operational_impact: Dict[str, int]
    estimated_consequence: str


class Recommendation(BaseModel):
    id: str
    action: str
    threat_type: ThreatType
    expected_risk_reduction: float
    priority: int


class Incident(BaseModel):
    incident_id: str
    start_time: datetime
    threat_type: ThreatType
    threat_confidence: float
    affected_subsystems: List[str]
    initial_risk: int
    current_risk: int
    predicted_risk: int
    recommendations: List[Recommendation]
    applied_mitigations: List[str]
    final_risk: Optional[int] = None
    resolution_time: Optional[datetime] = None
    timeline_stage: str  # "normal", "attack", "detected", "predicted", "mitigated", "resolved"


class IncidentReport(BaseModel):
    incident_id: str
    timestamp: datetime
    threat_type: str
    confidence_score: float
    affected_systems: List[str]
    current_risk: int
    predicted_impact: Dict[str, Any]
    recommended_actions: List[str]
    applied_mitigations: List[str]
    final_risk_assessment: int
    duration_seconds: float
