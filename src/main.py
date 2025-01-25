# main.py
from sensors import SensorManager
from zigbee_communication import ZigbeeManager
from data_processing import DataProcessor
from dashboard import Dashboard
import time

def main() -> None:
    """
    Main function to initialize components and start the data collection process.
    """
    # Initialize sensor manager
    sensor_manager = SensorManager()
    
    # Initialize Zigbee communication
    zigbee_manager = ZigbeeManager()
    
    # Initialize data processor
    data_processor = DataProcessor()
    
    # Initialize dashboard
    dashboard = Dashboard()
    
    # Start collecting data
    try:
        while True:
            sensor_data = sensor_manager.collect_data()
            processed_data = data_processor.process(sensor_data)
            dashboard.update(processed_data)
            time.sleep(1)  # Add a delay to prevent tight loop
    except KeyboardInterrupt:
        print("Data collection stopped by user.")

if __name__ == "__main__":
    main()
