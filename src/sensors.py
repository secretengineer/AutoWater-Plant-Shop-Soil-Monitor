"""
Sensor management module for AutoWater Plant Shop Soil Monitor.

This module handles sensor initialization, data collection, and sensor health monitoring.
"""

import random
import time
from typing import Dict, List, Optional
from datetime import datetime
from .logging_config import get_logger
from .config import config

logger = get_logger(__name__)


class SensorData:
    """Represents data from a single sensor reading."""
    
    def __init__(self, sensor_id: str, moisture: float, temperature: float = None, 
                 timestamp: datetime = None):
        """
        Initialize sensor data.
        
        Args:
            sensor_id: Unique identifier for the sensor
            moisture: Moisture level (0-100%)
            temperature: Optional temperature reading
            timestamp: When the reading was taken
        """
        self.sensor_id = sensor_id
        self.moisture = moisture
        self.temperature = temperature
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'sensor_id': self.sensor_id,
            'moisture': self.moisture,
            'temperature': self.temperature,
            'timestamp': self.timestamp.isoformat()
        }


class SensorManager:
    """Manages multiple soil moisture sensors and data collection."""
    
    def __init__(self, sensor_ids: List[str] = None):
        """
        Initialize the SensorManager and its sensors.
        
        Args:
            sensor_ids: List of sensor IDs to manage
        """
        self.sensor_ids = sensor_ids or [f"sensor_{i+1}" for i in range(10)]
        self.last_readings: Dict[str, SensorData] = {}
        self.sensor_config = config.get('sensor', {})
        self.update_interval = self.sensor_config.get('update_interval', 60)
        
        logger.info(f"Initialized SensorManager with {len(self.sensor_ids)} sensors")
        logger.debug(f"Sensor IDs: {self.sensor_ids}")

    def collect_data(self) -> Dict[str, SensorData]:
        """
        Collect data from all sensors.

        Returns:
            Dictionary mapping sensor IDs to SensorData objects
        """
        try:
            logger.debug("Starting sensor data collection")
            collected_data = {}
            
            for sensor_id in self.sensor_ids:
                try:
                    sensor_data = self._read_single_sensor(sensor_id)
                    collected_data[sensor_id] = sensor_data
                    self.last_readings[sensor_id] = sensor_data
                    
                except Exception as e:
                    logger.error(f"Failed to read sensor {sensor_id}: {e}")
                    # Use last known reading if available
                    if sensor_id in self.last_readings:
                        collected_data[sensor_id] = self.last_readings[sensor_id]
                        logger.warning(f"Using last known reading for sensor {sensor_id}")
            
            logger.info(f"Successfully collected data from {len(collected_data)} sensors")
            return collected_data
            
        except Exception as e:
            logger.error(f"Critical error during sensor data collection: {e}")
            return {}
    
    def _read_single_sensor(self, sensor_id: str) -> SensorData:
        """
        Read data from a single sensor.
        
        Args:
            sensor_id: ID of the sensor to read
            
        Returns:
            SensorData object with the reading
        """
        # Simulate sensor reading with realistic values
        # In real implementation, this would interface with actual hardware
        
        # Simulate some variability and occasional sensor issues
        if random.random() < 0.05:  # 5% chance of sensor read failure
            raise Exception(f"Sensor {sensor_id} communication timeout")
        
        # Generate realistic moisture data (0-100%)
        base_moisture = 30 + (hash(sensor_id) % 50)  # Consistent base per sensor
        moisture = max(0, min(100, base_moisture + random.uniform(-10, 10)))
        
        # Optional temperature reading
        temperature = 20 + random.uniform(-5, 15)  # 15-35°C range
        
        logger.debug(f"Read sensor {sensor_id}: moisture={moisture:.1f}%, temp={temperature:.1f}°C")
        
        return SensorData(
            sensor_id=sensor_id,
            moisture=round(moisture, 1),
            temperature=round(temperature, 1)
        )
    
    def get_sensor_health(self) -> Dict[str, bool]:
        """
        Check the health status of all sensors.
        
        Returns:
            Dictionary mapping sensor IDs to health status (True = healthy)
        """
        health_status = {}
        current_time = datetime.now()
        
        for sensor_id in self.sensor_ids:
            if sensor_id in self.last_readings:
                last_reading = self.last_readings[sensor_id]
                time_diff = (current_time - last_reading.timestamp).total_seconds()
                # Consider sensor healthy if last reading was within 2x update interval
                health_status[sensor_id] = time_diff < (self.update_interval * 2)
            else:
                health_status[sensor_id] = False
        
        return health_status
    
    def get_summary_stats(self) -> Dict:
        """
        Get summary statistics for all sensors.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.last_readings:
            return {}
        
        moisture_values = [reading.moisture for reading in self.last_readings.values()]
        
        return {
            'total_sensors': len(self.sensor_ids),
            'active_sensors': len(self.last_readings),
            'avg_moisture': sum(moisture_values) / len(moisture_values) if moisture_values else 0,
            'min_moisture': min(moisture_values) if moisture_values else 0,
            'max_moisture': max(moisture_values) if moisture_values else 0,
            'last_update': max(reading.timestamp for reading in self.last_readings.values()).isoformat()
        }
