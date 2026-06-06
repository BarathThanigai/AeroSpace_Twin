import numpy as np
import pickle
from pathlib import Path
from typing import Dict, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from ..models import Aircraft, AnomalyAlert
from datetime import datetime


class AnomalyDetector:
    """Isolation Forest based anomaly detection for aircraft systems."""

    def __init__(self, model_path: str = None, scaler_path: str = None):
        self.model = None
        self.scaler = None
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.is_trained = False

        if model_path and Path(model_path).exists():
            self.load_model(model_path, scaler_path)

    def _extract_features(self, aircraft: Aircraft) -> np.ndarray:
        """Extract feature vector from aircraft data."""
        features = [
            aircraft.navigation.current_value,
            aircraft.flight_control.current_value,
            aircraft.communication.current_value,
            aircraft.engine.current_value,
            aircraft.sensors.current_value,
            aircraft.navigation.risk_score,
            aircraft.flight_control.risk_score,
            aircraft.communication.risk_score,
            aircraft.engine.risk_score,
            aircraft.sensors.risk_score,
        ]
        return np.array(features).reshape(1, -1)

    def train(self, training_data: np.ndarray, contamination: float = 0.1):
        """Train Isolation Forest on normal data."""
        self.scaler = StandardScaler()
        scaled_data = self.scaler.fit_transform(training_data)

        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100,
        )
        self.model.fit(scaled_data)
        self.is_trained = True

    def detect(self, aircraft: Aircraft) -> Tuple[bool, float, float, Dict]:
        """Detect anomalies in aircraft data."""
        if not self.is_trained or self.model is None:
            raise ValueError("Model not trained. Call train() first.")

        features = self._extract_features(aircraft)
        scaled_features = self.scaler.transform(features)

        # Prediction: -1 = anomaly, 1 = normal
        prediction = self.model.predict(scaled_features)[0]
        anomaly_score = self.model.score_samples(scaled_features)[0]

        # Convert to confidence (0-100)
        confidence = min(100, max(0, abs(anomaly_score) * 100))

        is_anomaly = prediction == -1

        feature_dict = {
            "navigation": aircraft.navigation.current_value,
            "flight_control": aircraft.flight_control.current_value,
            "communication": aircraft.communication.current_value,
            "engine": aircraft.engine.current_value,
            "sensors": aircraft.sensors.current_value,
        }

        return is_anomaly, confidence, anomaly_score, feature_dict

    def save_model(self, model_path: str, scaler_path: str):
        """Save trained model and scaler."""
        if self.model is not None:
            with open(model_path, "wb") as f:
                pickle.dump(self.model, f)
        if self.scaler is not None:
            with open(scaler_path, "wb") as f:
                pickle.dump(self.scaler, f)

    def load_model(self, model_path: str, scaler_path: str):
        """Load pre-trained model and scaler."""
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
        with open(scaler_path, "rb") as f:
            self.scaler = pickle.load(f)
        self.is_trained = True


# Global anomaly detector instance
_detector: AnomalyDetector = None


def initialize_detector(model_path: str = None, scaler_path: str = None) -> AnomalyDetector:
    """Initialize global anomaly detector."""
    global _detector
    _detector = AnomalyDetector(model_path, scaler_path)
    return _detector


def get_detector() -> AnomalyDetector:
    """Get global anomaly detector instance."""
    global _detector
    if _detector is None:
        _detector = AnomalyDetector()
    return _detector
