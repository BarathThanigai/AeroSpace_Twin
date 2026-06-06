#!/usr/bin/env python
"""Train the Isolation Forest anomaly detection model."""

import sys
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.ml.model_trainer import train_isolation_forest
from app.config import MODEL_PATH, SCALER_PATH

if __name__ == "__main__":
    print("Training AeroShield Twin Anomaly Detection Model...")
    print(f"Model will be saved to: {MODEL_PATH}")
    print(f"Scaler will be saved to: {SCALER_PATH}")

    # Create models directory
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Train the model
    detector = train_isolation_forest(
        num_samples=2000,
        contamination=0.1,
        model_path=str(MODEL_PATH),
        scaler_path=str(SCALER_PATH),
    )

    print(f"\n✓ Model training complete!")
    print(f"✓ Model saved: {MODEL_PATH}")
    print(f"✓ Scaler saved: {SCALER_PATH}")
