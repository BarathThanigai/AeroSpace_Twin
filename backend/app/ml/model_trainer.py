import numpy as np
from pathlib import Path
from ..data.generator import SyntheticDataGenerator, AircraftFactory
from .anomaly_detector import AnomalyDetector


def generate_training_data(num_samples: int = 1000) -> np.ndarray:
    """Generate training data from normal aircraft operations."""
    generator = SyntheticDataGenerator()

    training_features = []

    for _ in range(num_samples):
        normal_data = generator.get_normal_data()
        aircraft = AircraftFactory.create_aircraft(normal_data)

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
        training_features.append(features)

    return np.array(training_features)


def train_isolation_forest(
    num_samples: int = 1000,
    contamination: float = 0.1,
    model_path: str = None,
    scaler_path: str = None,
) -> AnomalyDetector:
    """Train and save Isolation Forest model."""

    print(f"Generating {num_samples} training samples...")
    training_data = generate_training_data(num_samples)

    print("Training Isolation Forest...")
    detector = AnomalyDetector()
    detector.train(training_data, contamination=contamination)

    if model_path and scaler_path:
        print(f"Saving model to {model_path} and {scaler_path}...")
        detector.save_model(model_path, scaler_path)

    print("✓ Training complete!")
    return detector


if __name__ == "__main__":
    model_path = "app/ml/models/isolation_forest.pkl"
    scaler_path = "app/ml/models/scaler.pkl"

    # Create models directory if it doesn't exist
    Path("app/ml/models").mkdir(parents=True, exist_ok=True)

    train_isolation_forest(num_samples=1500, model_path=model_path, scaler_path=scaler_path)
