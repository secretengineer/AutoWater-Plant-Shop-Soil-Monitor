# test_data_processing.py
import unittest
from src.data_processing import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def test_process(self):
        processor = DataProcessor()
        raw_data = {"moisture": 30}
        processed_data = processor.process(raw_data)
        self.assertIsNotNone(processed_data)

if __name__ == '__main__':
    unittest.main()
