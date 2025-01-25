# test_dashboard.py
import unittest
from src.dashboard import Dashboard

class TestDashboard(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case environment.
        """
        self.dashboard = Dashboard()

    def test_update(self):
        """
        Test the update method of Dashboard.
        """
        data = {"moisture": 30}
        self.dashboard.update(data)  # Assuming update method does not return anything
        # Add assertions if there are any side effects or state changes to verify

if __name__ == '__main__':
    unittest.main()
