"""
Test configuration for AutoWater Plant Shop Soil Monitor.

This module provides test-specific configuration and fixtures.
"""

import unittest
import tempfile
import os
from unittest.mock import Mock, patch
import sys
import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.sensors import SensorManager, SensorData
from src.data_processing import DataProcessor
from src.config import ConfigManager


class BaseTestCase(unittest.TestCase):
    """Base test case with common setup and utilities."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test configuration
        self.test_config = {
            'sensor': {
                'type': 'test',
                'update_interval': 1
            },
            'sensors': {
                'ids': ['test_sensor_1', 'test_sensor_2']
            },
            'dashboard': {
                'host': '127.0.0.1',
                'port': 5001
            }
        }
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_mock_sensor_data(self, sensor_id: str = "test_sensor", 
                               moisture: float = 50.0, temperature: float = 25.0) -> SensorData:
        """Create mock sensor data for testing."""
        return SensorData(
            sensor_id=sensor_id,
            moisture=moisture,
            temperature=temperature,
            timestamp=datetime.datetime.now()
        )


class MockSensorManager:
    """Mock sensor manager for testing."""
    
    def __init__(self, sensor_ids=None):
        self.sensor_ids = sensor_ids or ['mock_sensor_1', 'mock_sensor_2']
        self.last_readings = {}
    
    def collect_data(self):
        """Return mock sensor data."""
        data = {}
        for sensor_id in self.sensor_ids:
            data[sensor_id] = SensorData(
                sensor_id=sensor_id,
                moisture=50.0 + hash(sensor_id) % 30,
                temperature=25.0 + hash(sensor_id) % 10
            )
        return data
    
    def get_sensor_health(self):
        """Return mock health status."""
        return {sensor_id: True for sensor_id in self.sensor_ids}
    
    def get_summary_stats(self):
        """Return mock summary statistics."""
        return {
            'total_sensors': len(self.sensor_ids),
            'active_sensors': len(self.sensor_ids),
            'avg_moisture': 55.0,
            'min_moisture': 40.0,
            'max_moisture': 70.0,
            'last_update': datetime.datetime.now().isoformat()
        }