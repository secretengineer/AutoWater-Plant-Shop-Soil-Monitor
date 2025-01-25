# main.py
from sensors import SensorManager
from zigbee_communication import ZigbeeManager
from data_processing import DataProcessor
from dashboard import Dashboard

def main():
    # Initialize sensor manager
    sensor_manager = SensorManager()
    
    # Initialize Zigbee communication
    zigbee_manager = ZigbeeManager()
    
    # Initialize data processor
    data_processor = DataProcessor()
    
    # Initialize dashboard
    dashboard = Dashboard()
    
    # Start collecting data
    while True:
        sensor_data = sensor_manager.collect_data()
        processed_data = data_processor.process(sensor_data)
        dashboard.update(processed_data)

if __name__ == "__main__":
    main()
