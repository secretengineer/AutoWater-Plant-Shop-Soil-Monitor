"""
Main application module for AutoWater Plant Shop Soil Monitor.

This module orchestrates the entire soil monitoring system including:
- Sensor data collection
- Data processing and analysis
- Web dashboard serving
- System monitoring and health checks
"""

import time
import signal
import sys
from typing import Optional
from threading import Thread, Event

from .sensors import SensorManager
from .zigbee_communication import ZigbeeManager
from .data_processing import DataProcessor
from .dashboard import create_dashboard_app
from .logging_config import setup_logging, get_logger
from .config import config

logger = get_logger(__name__)


class AutoWaterMonitor:
    """Main application class that coordinates all system components."""
    
    def __init__(self):
        """Initialize the monitoring system."""
        self.sensor_manager: Optional[SensorManager] = None
        self.zigbee_manager: Optional[ZigbeeManager] = None
        self.data_processor: Optional[DataProcessor] = None
        self.dashboard_thread: Optional[Thread] = None
        self.monitoring_active = Event()
        self.shutdown_requested = Event()
        
        # Configure signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("AutoWaterMonitor initialized")

    def initialize_components(self) -> bool:
        """
        Initialize all system components.
        
        Returns:
            True if all components initialized successfully, False otherwise
        """
        try:
            logger.info("Initializing system components...")
            
            # Initialize sensor manager
            sensor_ids = config.get('sensors.ids', [f"sensor_{i+1}" for i in range(10)])
            self.sensor_manager = SensorManager(sensor_ids)
            
            # Initialize Zigbee communication
            if config.get('zigbee.enabled', True):
                self.zigbee_manager = ZigbeeManager()
            
            # Initialize data processor
            self.data_processor = DataProcessor()
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            return False

    def start_dashboard(self) -> None:
        """Start the web dashboard in a separate thread."""
        try:
            logger.info("Starting web dashboard...")
            
            app = create_dashboard_app(self.sensor_manager, self.data_processor)
            
            # Dashboard configuration
            host = config.get('dashboard.host', '127.0.0.1')
            port = config.get('dashboard.port', 5000)
            debug = config.get('dashboard.debug', False)
            
            def run_dashboard():
                app.run(host=host, port=port, debug=debug, use_reloader=False)
            
            self.dashboard_thread = Thread(target=run_dashboard, daemon=True)
            self.dashboard_thread.start()
            
            logger.info(f"Dashboard started at http://{host}:{port}")
            
        except Exception as e:
            logger.error(f"Failed to start dashboard: {e}")

    def start_monitoring(self) -> None:
        """Start the main monitoring loop."""
        if not self.sensor_manager or not self.data_processor:
            raise RuntimeError("Components not initialized. Call initialize_components() first.")
        
        logger.info("Starting monitoring loop...")
        self.monitoring_active.set()
        
        update_interval = config.get('sensor.update_interval', 60)
        
        try:
            while self.monitoring_active.is_set() and not self.shutdown_requested.is_set():
                loop_start_time = time.time()
                
                try:
                    # Collect sensor data
                    logger.debug("Collecting sensor data...")
                    sensor_data = self.sensor_manager.collect_data()
                    
                    if sensor_data:
                        # Process the data
                        processed_data = self.data_processor.process(sensor_data)
                        
                        # Send via Zigbee if enabled
                        if self.zigbee_manager:
                            try:
                                self.zigbee_manager.send_data(processed_data)
                            except Exception as e:
                                logger.warning(f"Zigbee transmission failed: {e}")
                        
                        # Log summary
                        stats = processed_data.get('statistics', {})
                        alerts_count = len(processed_data.get('alerts', []))
                        
                        logger.info(
                            f"Monitoring cycle complete. "
                            f"Sensors: {len(sensor_data)}, "
                            f"Avg moisture: {stats.get('moisture', {}).get('average', 'N/A')}%, "
                            f"Alerts: {alerts_count}"
                        )
                    else:
                        logger.warning("No sensor data collected")
                
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                
                # Sleep for the remaining time in the update interval
                elapsed_time = time.time() - loop_start_time
                sleep_time = max(0, update_interval - elapsed_time)
                
                if sleep_time > 0:
                    logger.debug(f"Sleeping for {sleep_time:.1f} seconds")
                    if self.shutdown_requested.wait(timeout=sleep_time):
                        break
                        
        except Exception as e:
            logger.error(f"Critical error in monitoring loop: {e}")
        finally:
            logger.info("Monitoring loop stopped")

    def stop_monitoring(self) -> None:
        """Stop the monitoring loop."""
        logger.info("Stopping monitoring...")
        self.monitoring_active.clear()
        self.shutdown_requested.set()

    def run(self) -> None:
        """Run the complete monitoring system."""
        try:
            logger.info("Starting AutoWater Plant Shop Soil Monitor")
            
            # Initialize all components
            if not self.initialize_components():
                logger.error("Failed to initialize components. Exiting.")
                return
            
            # Start web dashboard
            self.start_dashboard()
            
            # Give dashboard time to start
            time.sleep(2)
            
            # Start monitoring loop
            self.start_monitoring()
            
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources and shut down gracefully."""
        logger.info("Cleaning up and shutting down...")
        
        self.stop_monitoring()
        
        # Wait for dashboard thread to finish (with timeout)
        if self.dashboard_thread and self.dashboard_thread.is_alive():
            logger.info("Waiting for dashboard to shutdown...")
            self.dashboard_thread.join(timeout=5)
        
        logger.info("Shutdown complete")

    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown."""
        logger.info(f"Received signal {signum}. Initiating shutdown...")
        self.shutdown_requested.set()


def main() -> None:
    """
    Main entry point for the application.
    """
    # Set up logging
    log_level = config.get('logging.level', 'INFO')
    setup_logging(log_level)
    
    logger.info("=" * 60)
    logger.info("AutoWater Plant Shop Soil Monitor Starting")
    logger.info("=" * 60)
    
    # Create and run the monitor
    monitor = AutoWaterMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
