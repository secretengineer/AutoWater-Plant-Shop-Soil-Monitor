# data_processing.py
class DataProcessor:
    def process(self, sensor_data: dict) -> dict:
        """
        Process raw sensor data.

        Args:
            sensor_data (dict): The raw data from sensors.

        Returns:
            dict: The processed data.
        """
        try:
            # Process raw sensor data
            processed_data = self._process_data(sensor_data)
            return processed_data
        except Exception as e:
            print(f"An error occurred while processing data: {e}")
            return {}

    def _process_data(self, sensor_data: dict) -> dict:
        """
        Internal method to process raw sensor data.

        Args:
            sensor_data (dict): The raw data from sensors.

        Returns:
            dict: The processed data.
        """
        # Replace with actual processing logic
        processed_data = {
            "average_moisture": sum(sensor_data.values()) / len(sensor_data) if sensor_data else 0
        }
        return processed_data
