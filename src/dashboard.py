"""
Web dashboard module for AutoWater Plant Shop Soil Monitor.

This module provides a Flask-based web interface for monitoring sensor data,
viewing analytics, and managing the system.
"""

from flask import Flask, render_template, jsonify, request
from typing import Optional
from datetime import datetime
import json

from .logging_config import get_logger
from .config import config

logger = get_logger(__name__)


class DashboardData:
    """Manages data for the dashboard interface."""
    
    def __init__(self, sensor_manager=None, data_processor=None):
        """
        Initialize dashboard data manager.
        
        Args:
            sensor_manager: SensorManager instance
            data_processor: DataProcessor instance
        """
        self.sensor_manager = sensor_manager
        self.data_processor = data_processor
        self.last_processed_data = {}
        
    def get_current_sensor_data(self) -> dict:
        """Get current sensor readings formatted for dashboard."""
        try:
            if not self.sensor_manager:
                # Return mock data if no sensor manager available
                return {
                    "sensors": [
                        {"id": f"sensor_{i+1}", "moisture": 30 + (i * 5), "temperature": 22 + i}
                        for i in range(10)
                    ],
                    "timestamp": datetime.now().isoformat(),
                    "mock_data": True
                }
            
            # Get real sensor data
            sensor_readings = self.sensor_manager.collect_data()
            
            sensors_list = []
            for sensor_id, sensor_data in sensor_readings.items():
                sensors_list.append({
                    "id": sensor_id,
                    "moisture": sensor_data.moisture,
                    "temperature": sensor_data.temperature,
                    "timestamp": sensor_data.timestamp.isoformat()
                })
            
            # Get health status
            health_status = self.sensor_manager.get_sensor_health()
            
            return {
                "sensors": sensors_list,
                "health": health_status,
                "summary": self.sensor_manager.get_summary_stats(),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting sensor data: {e}")
            return {"error": str(e), "sensors": []}
    
    def get_processed_data(self) -> dict:
        """Get processed data and analytics."""
        return self.last_processed_data.copy() if self.last_processed_data else {}
    
    def update_processed_data(self, processed_data: dict) -> None:
        """Update the processed data cache."""
        self.last_processed_data = processed_data.copy()


def create_dashboard_app(sensor_manager=None, data_processor=None) -> Flask:
    """
    Create and configure the Flask dashboard application.
    
    Args:
        sensor_manager: SensorManager instance
        data_processor: DataProcessor instance
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Configure Flask app
    app.config['SECRET_KEY'] = config.get_secret('flask.secret_key', 'dev-key-change-in-production')
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize dashboard data manager
    dashboard_data = DashboardData(sensor_manager, data_processor)
    
    @app.route('/')
    def home():
        """Redirect to dashboard."""
        return render_template('dashboard.html')
    
    @app.route('/dashboard')
    def show_dashboard():
        """Render the main dashboard page."""
        try:
            return render_template('dashboard.html')
        except Exception as e:
            logger.error(f"Error rendering dashboard: {e}")
            return f"Dashboard error: {e}", 500
    
    @app.route('/api/sensors')
    @app.route('/api/sensors/')
    def get_sensors():
        """
        Get current sensor data as JSON.
        
        Returns:
            JSON response with sensor data
        """
        try:
            data = dashboard_data.get_current_sensor_data()
            return jsonify(data)
        except Exception as e:
            logger.error(f"Error in /api/sensors: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/analytics')
    @app.route('/api/analytics/')
    def get_analytics():
        """
        Get processed analytics data.
        
        Returns:
            JSON response with analytics data
        """
        try:
            data = dashboard_data.get_processed_data()
            return jsonify(data)
        except Exception as e:
            logger.error(f"Error in /api/analytics: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/health')
    @app.route('/api/health/')
    def get_health():
        """
        Get system health status.
        
        Returns:
            JSON response with health information
        """
        try:
            health_data = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "sensor_manager": sensor_manager is not None,
                    "data_processor": data_processor is not None,
                }
            }
            
            if sensor_manager:
                sensor_health = sensor_manager.get_sensor_health()
                health_data["sensors"] = sensor_health
                health_data["healthy_sensors"] = sum(1 for status in sensor_health.values() if status)
                health_data["total_sensors"] = len(sensor_health)
            
            return jsonify(health_data)
        except Exception as e:
            logger.error(f"Error in /api/health: {e}")
            return jsonify({"status": "error", "error": str(e)}), 500
    
    @app.route('/api/config')
    @app.route('/api/config/')
    def get_config():
        """
        Get current configuration (non-sensitive parts).
        
        Returns:
            JSON response with configuration
        """
        try:
            # Only return non-sensitive configuration
            safe_config = {
                "sensor": {
                    "type": config.get('sensor.type'),
                    "update_interval": config.get('sensor.update_interval')
                },
                "dashboard": {
                    "host": config.get('dashboard.host'),
                    "port": config.get('dashboard.port')
                }
            }
            return jsonify(safe_config)
        except Exception as e:
            logger.error(f"Error in /api/config: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    # Store dashboard_data in app context for access by other components
    app.dashboard_data = dashboard_data
    
    logger.info("Dashboard application created successfully")
    return app


# For backward compatibility and standalone testing
def create_standalone_app():
    """Create a standalone dashboard app with mock data."""
    return create_dashboard_app()
