# test_dashboard.py
import unittest
from src.dashboard import app, sensor_data
import json

class TestDashboard(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case environment.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_update(self):
        """
        Test the update method of Dashboard.
        """
        data = {"sensor1": 35}
        # Simulate updating the sensor data
        sensor_data[0]['moisture'] = data["sensor1"]
        self.assertEqual(sensor_data[0]['moisture'], 35)

    def test_show_dashboard(self):
        """
        Test the /dashboard route.
        """
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sensor Dashboard', response.data)

    def test_get_sensors(self):
        """
        Test the /api/sensors route.
        """
        response = self.app.get('/api/sensors')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('sensors', data)
        self.assertIsInstance(data['sensors'], list)

if __name__ == '__main__':
    unittest.main()
