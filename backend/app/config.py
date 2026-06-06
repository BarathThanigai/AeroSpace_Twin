import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"

# Model Settings
MODEL_PATH = BASE_DIR / "ml" / "models" / "isolation_forest.pkl"
SCALER_PATH = BASE_DIR / "ml" / "models" / "scaler.pkl"

# Real-time Settings
UPDATE_INTERVAL = 1.5  # seconds
ANOMALY_THRESHOLD = 0.5
CONFIDENCE_THRESHOLD = 0.6

# Aircraft Subsystems
SUBSYSTEMS = ["navigation", "flight_control", "communication", "engine", "sensors"]
INITIAL_HEALTH = "healthy"
INITIAL_RISK_SCORE = 5

# Threat Types
THREAT_TYPES = ["GPS_Spoofing", "Sensor_Anomaly", "Communication_Anomaly", "Network_Intrusion", "Unknown"]

# Impact Levels
IMPACT_LEVELS = {"normal": 0, "low": 25, "medium": 50, "high": 75, "critical": 100}
HEALTH_STATES = ["healthy", "warning", "critical"]
