import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List
from ..models import Subsystem, Aircraft, HealthStatus


class SyntheticDataGenerator:
    """Generate synthetic aircraft sensor data with optional anomalies."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        np.random.seed(seed)
        self.normal_patterns = self._create_normal_patterns()
        self.current_values = self._initialize_values()

    def _create_normal_patterns(self) -> Dict[str, Dict]:
        """Define normal operating ranges for each subsystem."""
        return {
            "navigation": {
                "gps_signal": {"mean": 90, "std": 5, "min": 70, "max": 100},
                "position_accuracy": {"mean": 2, "std": 0.3, "min": 0.5, "max": 5},
                "heading_error": {"mean": 1, "std": 0.2, "min": 0, "max": 3},
            },
            "flight_control": {
                "pitch_stability": {"mean": 50, "std": 5, "min": 30, "max": 70},
                "roll_rate": {"mean": 0, "std": 2, "min": -10, "max": 10},
                "control_response": {"mean": 95, "std": 2, "min": 85, "max": 100},
            },
            "communication": {
                "signal_strength": {"mean": 85, "std": 5, "min": 60, "max": 100},
                "packet_loss": {"mean": 1, "std": 0.5, "min": 0, "max": 5},
                "latency_ms": {"mean": 50, "std": 10, "min": 20, "max": 100},
            },
            "engine": {
                "temp_celsius": {"mean": 650, "std": 20, "min": 500, "max": 850},
                "pressure_psi": {"mean": 45, "std": 3, "min": 30, "max": 60},
                "vibration": {"mean": 0.2, "std": 0.05, "min": 0, "max": 0.5},
            },
            "sensors": {
                "temperature_variation": {"mean": 0, "std": 0.1, "min": -0.5, "max": 0.5},
                "pressure_variation": {"mean": 0, "std": 0.2, "min": -1, "max": 1},
                "acceleration_g": {"mean": 1, "std": 0.1, "min": 0.5, "max": 1.5},
            },
        }

    def _initialize_values(self) -> Dict[str, float]:
        """Initialize current sensor values in normal ranges."""
        values = {}
        for subsystem, params in self.normal_patterns.items():
            for key, distribution in params.items():
                val = np.random.normal(distribution["mean"], distribution["std"])
                val = np.clip(val, distribution["min"], distribution["max"])
                values[f"{subsystem}_{key}"] = val
        return values

    def get_normal_data(self) -> Dict[str, float]:
        """Generate next normal sensor reading with small random variations."""
        for key, distribution_set in self.normal_patterns.items():
            for param, distribution in distribution_set.items():
                key_name = f"{key}_{param}"
                if key_name in self.current_values:
                    # Small drift from current value
                    drift = np.random.normal(0, distribution["std"] * 0.3)
                    new_val = self.current_values[key_name] + drift
                    new_val = np.clip(new_val, distribution["min"], distribution["max"])
                    self.current_values[key_name] = new_val

        return self.current_values.copy()

    def inject_gps_spoofing(self, severity: float = 1.0) -> Dict[str, float]:
        """Inject GPS spoofing anomalies."""
        data = self.get_normal_data()

        # GPS signal drops significantly
        data["navigation_gps_signal"] = np.random.uniform(10, 30) * severity
        # Position jumps erratically
        data["navigation_position_accuracy"] = np.random.uniform(50, 200) * severity
        # Heading becomes erratic
        data["navigation_heading_error"] = np.random.uniform(20, 89) * severity

        return data

    def inject_sensor_anomaly(self, severity: float = 1.0) -> Dict[str, float]:
        """Inject sensor anomalies (temperature/pressure spikes)."""
        data = self.get_normal_data()

        # Temperature spike
        data["engine_temp_celsius"] = np.random.uniform(850, 1200) * severity
        # Pressure deviation
        data["engine_pressure_psi"] = np.random.uniform(60, 100) * severity
        # Vibration spike
        data["engine_vibration"] = np.random.uniform(0.7, 1.5) * severity

        return data

    def inject_communication_anomaly(self, severity: float = 1.0) -> Dict[str, float]:
        """Inject communication anomalies."""
        data = self.get_normal_data()

        # Signal strength drops
        data["communication_signal_strength"] = np.random.uniform(20, 50) * severity
        # Packet loss spikes
        data["communication_packet_loss"] = np.random.uniform(15, 50) * severity
        # Latency increases
        data["communication_latency_ms"] = np.random.uniform(200, 500) * severity

        return data


class SubsystemFactory:
    """Create subsystem objects with current health status."""

    @staticmethod
    def create_subsystem(
        name: str,
        current_value: float,
        threshold: float = 50,
        normal_range: tuple = (0, 100),
    ) -> Subsystem:
        """Factory method to create a subsystem with computed health status."""
        risk_score = int(round(max(0, min(100, abs(100 - current_value)))))

        if risk_score <= 20:
            status = HealthStatus.HEALTHY
        elif risk_score <= 60:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        impact_level = risk_score

        return Subsystem(
            name=name,
            status=status,
            risk_score=risk_score,
            impact_level=impact_level,
            current_value=current_value,
            threshold=threshold,
            normal_range=normal_range,
        )


class AircraftFactory:
    """Create Aircraft digital twin objects."""

    @staticmethod
    def create_aircraft(sensor_data: Dict[str, float], aircraft_id: str = "AIRCRAFT-001") -> Aircraft:
        """Create an Aircraft object from sensor data."""

        subsystems = {
            "navigation": SubsystemFactory.create_subsystem(
                "navigation", sensor_data.get("navigation_gps_signal", 90)
            ),
            "flight_control": SubsystemFactory.create_subsystem(
                "flight_control", sensor_data.get("flight_control_control_response", 95)
            ),
            "communication": SubsystemFactory.create_subsystem(
                "communication",
                sensor_data.get("communication_signal_strength", 85),
            ),
            "engine": SubsystemFactory.create_subsystem(
                "engine",
                100 - (sensor_data.get("engine_temp_celsius", 650) - 500) / 7,
            ),
            "sensors": SubsystemFactory.create_subsystem(
                "sensors", 90 + sensor_data.get("sensors_temperature_variation", 0)
            ),
        }

        overall_risk = int(np.mean([s.risk_score for s in subsystems.values()]))

        if overall_risk <= 20:
            overall_status = HealthStatus.HEALTHY
        elif overall_risk <= 60:
            overall_status = HealthStatus.WARNING
        else:
            overall_status = HealthStatus.CRITICAL

        return Aircraft(
            id=aircraft_id,
            timestamp=datetime.now(),
            navigation=subsystems["navigation"],
            flight_control=subsystems["flight_control"],
            communication=subsystems["communication"],
            engine=subsystems["engine"],
            sensors=subsystems["sensors"],
            overall_risk=overall_risk,
            overall_status=overall_status,
        )
