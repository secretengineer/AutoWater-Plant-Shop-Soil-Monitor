# test_dashboard.py
import unittest
from src.dashboard import Dashboard

class TestDashboard(unittest.TestCase):
    def test_update(self):
        dashboard = Dashboard()
        data = {"moisture": 30}
        dashboard.update(data)  # Assuming update method does not return anything

if __name__ == '__main__':
    unittest.main()
