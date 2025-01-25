# test_sensors.py
import unittest
from src.sensors import SensorManager

class TestSensorManager(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case environment.
        """
        self.sensor_manager = SensorManager()

    def test_collect_data(self):
        """
        Test the collect_data method of SensorManager.
        """
        data = self.sensor_manager.collect_data()
        self.assertIsNotNone(data, "Data should not be None")
        self.assertIsInstance(data, dict, "Data should be a dictionary")
        # Add more specific assertions based on the expected structure of data
        # Example: self.assertIn('moisture', data)
        # Example: self.assertGreaterEqual(data['moisture'], 0)

if __name__ == '__main__':
    unittest.main()
