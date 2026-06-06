import asyncio
from typing import Dict, Callable, Optional
from datetime import datetime
from .generator import SyntheticDataGenerator, AircraftFactory
from ..models import Aircraft


class AircraftDataStream:
    """Manages simulated real-time aircraft data stream."""

    def __init__(self, update_interval: float = 1.5):
        self.update_interval = update_interval
        self.generator = SyntheticDataGenerator()
        self.current_aircraft: Optional[Aircraft] = None
        self.is_running = False
        self.is_attacking = False
        self.attack_type: Optional[str] = None
        self.attack_severity = 1.0
        self.stream_listeners: Dict[str, Callable] = {}

    def initialize(self):
        """Initialize with normal aircraft state."""
        normal_data = self.generator.get_normal_data()
        self.current_aircraft = AircraftFactory.create_aircraft(normal_data)
        self.is_attacking = False
        self.attack_type = None

    def start_attack(self, attack_type: str, severity: float = 1.0):
        """Start injecting attack data."""
        self.is_attacking = True
        self.attack_type = attack_type
        self.attack_severity = severity

    def stop_attack(self):
        """Stop attack and return to normal operation."""
        self.is_attacking = False
        self.attack_type = None
        self.attack_severity = 1.0

    def get_next_data(self) -> Aircraft:
        """Generate next sensor reading based on current state."""
        if not self.is_attacking:
            sensor_data = self.generator.get_normal_data()
        else:
            if self.attack_type == "gps_spoofing":
                sensor_data = self.generator.inject_gps_spoofing(self.attack_severity)
            elif self.attack_type == "sensor_anomaly":
                sensor_data = self.generator.inject_sensor_anomaly(self.attack_severity)
            elif self.attack_type == "communication_anomaly":
                sensor_data = self.generator.inject_communication_anomaly(self.attack_severity)
            else:
                sensor_data = self.generator.get_normal_data()

        self.current_aircraft = AircraftFactory.create_aircraft(sensor_data)
        return self.current_aircraft

    async def stream(self):
        """Continuously generate and stream aircraft data."""
        self.is_running = True
        self.initialize()

        try:
            while self.is_running:
                aircraft_data = self.get_next_data()

                # Notify all listeners
                for listener_id, callback in self.stream_listeners.items():
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(aircraft_data)
                        else:
                            callback(aircraft_data)
                    except Exception as e:
                        print(f"Error in stream listener {listener_id}: {e}")

                await asyncio.sleep(self.update_interval)
        except Exception as e:
            print(f"Error in stream: {e}")
        finally:
            self.is_running = False

    def register_listener(self, listener_id: str, callback: Callable):
        """Register a callback to receive stream updates."""
        self.stream_listeners[listener_id] = callback

    def unregister_listener(self, listener_id: str):
        """Unregister a stream listener."""
        if listener_id in self.stream_listeners:
            del self.stream_listeners[listener_id]

    def stop(self):
        """Stop the stream."""
        self.is_running = False


# Global stream instance
aircraft_stream: Optional[AircraftDataStream] = None


def initialize_stream(update_interval: float = 1.5) -> AircraftDataStream:
    """Initialize the global aircraft data stream."""
    global aircraft_stream
    aircraft_stream = AircraftDataStream(update_interval)
    return aircraft_stream


def get_stream() -> AircraftDataStream:
    """Get the global aircraft stream instance."""
    global aircraft_stream
    if aircraft_stream is None:
        aircraft_stream = initialize_stream()
    return aircraft_stream
