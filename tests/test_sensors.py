# test_sensors.py
import unittest
from src.sensors import SensorManager

class TestSensorManager(unittest.TestCase):
    def test_collect_data(self):
        sensor_manager = SensorManager()
        data = sensor_manager.collect_data()
        self.assertIsNotNone(data)

if __name__ == '__main__':
    unittest.main()
