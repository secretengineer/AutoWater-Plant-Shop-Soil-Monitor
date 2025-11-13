"""
Test suite for sensor management functionality.
"""

import unittest
from unittest.mock import patch, Mock
import datetime
from test_base import BaseTestCase

from src.sensors import SensorManager, SensorData


class TestSensorData(BaseTestCase):
    """Test cases for SensorData class."""
    
    def test_sensor_data_creation(self):
        """Test creating a SensorData instance."""
        timestamp = datetime.datetime.now()
        sensor_data = SensorData(
            sensor_id="test_sensor",
            moisture=45.5,
            temperature=23.2,
            timestamp=timestamp
        )
        
        self.assertEqual(sensor_data.sensor_id, "test_sensor")
        self.assertEqual(sensor_data.moisture, 45.5)
        self.assertEqual(sensor_data.temperature, 23.2)
        self.assertEqual(sensor_data.timestamp, timestamp)
    
    def test_sensor_data_to_dict(self):
        """Test converting SensorData to dictionary."""
        timestamp = datetime.datetime.now()
        sensor_data = SensorData(
            sensor_id="test_sensor",
            moisture=45.5,
            temperature=23.2,
            timestamp=timestamp
        )
        
        data_dict = sensor_data.to_dict()
        
        self.assertIsInstance(data_dict, dict)
        self.assertEqual(data_dict['sensor_id'], "test_sensor")
        self.assertEqual(data_dict['moisture'], 45.5)
        self.assertEqual(data_dict['temperature'], 23.2)
        self.assertEqual(data_dict['timestamp'], timestamp.isoformat())


class TestSensorManager(BaseTestCase):
    """Test cases for SensorManager class."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.sensor_ids = ["test_sensor_1", "test_sensor_2", "test_sensor_3"]
        self.sensor_manager = SensorManager(self.sensor_ids)

    def test_initialization(self):
        """Test SensorManager initialization."""
        self.assertEqual(self.sensor_manager.sensor_ids, self.sensor_ids)
        self.assertIsInstance(self.sensor_manager.last_readings, dict)
        self.assertEqual(len(self.sensor_manager.last_readings), 0)

    def test_collect_data_success(self):
        """Test successful data collection from all sensors."""
        data = self.sensor_manager.collect_data()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), len(self.sensor_ids))
        
        for sensor_id in self.sensor_ids:
            self.assertIn(sensor_id, data)
            self.assertIsInstance(data[sensor_id], SensorData)
            self.assertEqual(data[sensor_id].sensor_id, sensor_id)
            self.assertIsInstance(data[sensor_id].moisture, float)
            self.assertGreaterEqual(data[sensor_id].moisture, 0)
            self.assertLessEqual(data[sensor_id].moisture, 100)

    def test_collect_data_updates_last_readings(self):
        """Test that collect_data updates last_readings."""
        self.assertEqual(len(self.sensor_manager.last_readings), 0)
        
        data = self.sensor_manager.collect_data()
        
        self.assertEqual(len(self.sensor_manager.last_readings), len(self.sensor_ids))
        for sensor_id in self.sensor_ids:
            self.assertIn(sensor_id, self.sensor_manager.last_readings)

    @patch('src.sensors.SensorManager._read_single_sensor')
    def test_collect_data_with_sensor_failure(self, mock_read_sensor):
        """Test data collection when some sensors fail."""
        # Mock one sensor to fail, others to succeed
        def side_effect(sensor_id):
            if sensor_id == "test_sensor_2":
                raise Exception("Sensor communication failure")
            return self.create_mock_sensor_data(sensor_id)
        
        mock_read_sensor.side_effect = side_effect
        
        # First, populate last_readings with some data
        self.sensor_manager.last_readings["test_sensor_2"] = self.create_mock_sensor_data("test_sensor_2")
        
        data = self.sensor_manager.collect_data()
        
        # Should still return data for working sensors
        self.assertIn("test_sensor_1", data)
        self.assertIn("test_sensor_3", data)
        # Should use last known reading for failed sensor
        self.assertIn("test_sensor_2", data)

    def test_get_sensor_health(self):
        """Test sensor health status checking."""
        # Collect some data first
        self.sensor_manager.collect_data()
        
        health_status = self.sensor_manager.get_sensor_health()
        
        self.assertIsInstance(health_status, dict)
        self.assertEqual(len(health_status), len(self.sensor_ids))
        
        for sensor_id in self.sensor_ids:
            self.assertIn(sensor_id, health_status)
            self.assertIsInstance(health_status[sensor_id], bool)

    def test_get_summary_stats(self):
        """Test getting summary statistics."""
        # Collect some data first
        self.sensor_manager.collect_data()
        
        stats = self.sensor_manager.get_summary_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_sensors', stats)
        self.assertIn('active_sensors', stats)
        self.assertIn('avg_moisture', stats)
        self.assertIn('min_moisture', stats)
        self.assertIn('max_moisture', stats)
        self.assertIn('last_update', stats)
        
        self.assertEqual(stats['total_sensors'], len(self.sensor_ids))
        self.assertGreaterEqual(stats['active_sensors'], 0)
        self.assertLessEqual(stats['active_sensors'], len(self.sensor_ids))

    def test_get_summary_stats_no_data(self):
        """Test getting summary statistics with no data."""
        stats = self.sensor_manager.get_summary_stats()
        
        self.assertEqual(stats, {})


if __name__ == '__main__':
    unittest.main()
