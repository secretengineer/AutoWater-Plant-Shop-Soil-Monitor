"""
Data processing module for AutoWater Plant Shop Soil Monitor.

This module handles processing, analysis, and aggregation of sensor data.
"""

import statistics
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from .logging_config import get_logger
from .sensors import SensorData

logger = get_logger(__name__)


class DataProcessor:
    """Processes and analyzes sensor data for insights and alerts."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.historical_data: Dict[str, List[SensorData]] = {}
        self.alert_thresholds = {
            'low_moisture': 20.0,    # Alert if moisture below 20%
            'high_moisture': 80.0,   # Alert if moisture above 80%
            'temperature_min': 5.0,  # Alert if temperature below 5°C
            'temperature_max': 40.0  # Alert if temperature above 40°C
        }
        logger.info("DataProcessor initialized")

    def process(self, sensor_data: Dict[str, SensorData]) -> Dict:
        """
        Process raw sensor data and generate insights.

        Args:
            sensor_data: Dictionary mapping sensor IDs to SensorData objects

        Returns:
            Dictionary containing processed data and insights
        """
        try:
            logger.debug(f"Processing data from {len(sensor_data)} sensors")
            
            # Store historical data
            self._store_historical_data(sensor_data)
            
            # Process the data
            processed_data = {
                'timestamp': datetime.now().isoformat(),
                'sensor_readings': self._format_sensor_readings(sensor_data),
                'statistics': self._calculate_statistics(sensor_data),
                'alerts': self._generate_alerts(sensor_data),
                'trends': self._analyze_trends(sensor_data),
                'recommendations': self._generate_recommendations(sensor_data)
            }
            
            logger.info(f"Successfully processed data. Generated {len(processed_data['alerts'])} alerts")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing sensor data: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'sensor_readings': {},
                'statistics': {},
                'alerts': [],
                'trends': {},
                'recommendations': []
            }

    def _store_historical_data(self, sensor_data: Dict[str, SensorData]) -> None:
        """Store sensor data for historical analysis."""
        for sensor_id, data in sensor_data.items():
            if sensor_id not in self.historical_data:
                self.historical_data[sensor_id] = []
            
            self.historical_data[sensor_id].append(data)
            
            # Keep only last 1000 readings per sensor to prevent memory issues
            if len(self.historical_data[sensor_id]) > 1000:
                self.historical_data[sensor_id] = self.historical_data[sensor_id][-1000:]

    def _format_sensor_readings(self, sensor_data: Dict[str, SensorData]) -> Dict:
        """Format sensor readings for output."""
        return {
            sensor_id: data.to_dict() 
            for sensor_id, data in sensor_data.items()
        }

    def _calculate_statistics(self, sensor_data: Dict[str, SensorData]) -> Dict:
        """Calculate statistical summaries of the sensor data."""
        if not sensor_data:
            return {}
        
        moisture_values = [data.moisture for data in sensor_data.values()]
        temp_values = [data.temperature for data in sensor_data.values() 
                      if data.temperature is not None]
        
        stats = {
            'moisture': {
                'average': round(statistics.mean(moisture_values), 2),
                'median': round(statistics.median(moisture_values), 2),
                'min': min(moisture_values),
                'max': max(moisture_values),
                'std_dev': round(statistics.stdev(moisture_values) if len(moisture_values) > 1 else 0, 2)
            }
        }
        
        if temp_values:
            stats['temperature'] = {
                'average': round(statistics.mean(temp_values), 2),
                'median': round(statistics.median(temp_values), 2),
                'min': min(temp_values),
                'max': max(temp_values),
                'std_dev': round(statistics.stdev(temp_values) if len(temp_values) > 1 else 0, 2)
            }
        
        return stats

    def _generate_alerts(self, sensor_data: Dict[str, SensorData]) -> List[Dict]:
        """Generate alerts based on sensor readings and thresholds."""
        alerts = []
        
        for sensor_id, data in sensor_data.items():
            # Moisture alerts
            if data.moisture < self.alert_thresholds['low_moisture']:
                alerts.append({
                    'type': 'low_moisture',
                    'severity': 'warning',
                    'sensor_id': sensor_id,
                    'message': f"Low soil moisture detected: {data.moisture}%",
                    'value': data.moisture,
                    'threshold': self.alert_thresholds['low_moisture'],
                    'timestamp': data.timestamp.isoformat()
                })
            
            elif data.moisture > self.alert_thresholds['high_moisture']:
                alerts.append({
                    'type': 'high_moisture',
                    'severity': 'info',
                    'sensor_id': sensor_id,
                    'message': f"High soil moisture detected: {data.moisture}%",
                    'value': data.moisture,
                    'threshold': self.alert_thresholds['high_moisture'],
                    'timestamp': data.timestamp.isoformat()
                })
            
            # Temperature alerts
            if data.temperature is not None:
                if data.temperature < self.alert_thresholds['temperature_min']:
                    alerts.append({
                        'type': 'low_temperature',
                        'severity': 'warning',
                        'sensor_id': sensor_id,
                        'message': f"Low temperature detected: {data.temperature}°C",
                        'value': data.temperature,
                        'threshold': self.alert_thresholds['temperature_min'],
                        'timestamp': data.timestamp.isoformat()
                    })
                
                elif data.temperature > self.alert_thresholds['temperature_max']:
                    alerts.append({
                        'type': 'high_temperature',
                        'severity': 'critical',
                        'sensor_id': sensor_id,
                        'message': f"High temperature detected: {data.temperature}°C",
                        'value': data.temperature,
                        'threshold': self.alert_thresholds['temperature_max'],
                        'timestamp': data.timestamp.isoformat()
                    })
        
        return alerts

    def _analyze_trends(self, sensor_data: Dict[str, SensorData]) -> Dict:
        """Analyze trends in sensor data over time."""
        trends = {}
        
        for sensor_id, current_data in sensor_data.items():
            if sensor_id in self.historical_data and len(self.historical_data[sensor_id]) >= 2:
                historical = self.historical_data[sensor_id]
                recent_readings = historical[-10:]  # Last 10 readings
                
                if len(recent_readings) >= 2:
                    # Calculate moisture trend
                    moisture_values = [reading.moisture for reading in recent_readings]
                    moisture_trend = self._calculate_trend(moisture_values)
                    
                    trends[sensor_id] = {
                        'moisture_trend': moisture_trend,
                        'readings_count': len(recent_readings),
                        'time_span_hours': (recent_readings[-1].timestamp - recent_readings[0].timestamp).total_seconds() / 3600
                    }
        
        return trends

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate if values are trending up, down, or stable."""
        if len(values) < 2:
            return 'insufficient_data'
        
        # Simple linear trend calculation
        n = len(values)
        x = list(range(n))
        y = values
        
        # Calculate slope using least squares
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 'stable'
        
        slope = numerator / denominator
        
        # Classify trend based on slope
        if slope > 1:
            return 'increasing'
        elif slope < -1:
            return 'decreasing'
        else:
            return 'stable'

    def _generate_recommendations(self, sensor_data: Dict[str, SensorData]) -> List[str]:
        """Generate actionable recommendations based on sensor data."""
        recommendations = []
        
        if not sensor_data:
            return ["No sensor data available. Check sensor connections."]
        
        moisture_values = [data.moisture for data in sensor_data.values()]
        avg_moisture = statistics.mean(moisture_values)
        
        # Moisture-based recommendations
        if avg_moisture < 30:
            recommendations.append("Consider watering plants - average soil moisture is low")
        elif avg_moisture > 70:
            recommendations.append("Soil moisture is high - check drainage and reduce watering")
        
        # Individual sensor recommendations
        low_moisture_sensors = [
            sensor_id for sensor_id, data in sensor_data.items() 
            if data.moisture < 25
        ]
        
        if low_moisture_sensors:
            recommendations.append(f"Immediate attention needed for sensors: {', '.join(low_moisture_sensors)}")
        
        # Temperature-based recommendations
        temp_values = [data.temperature for data in sensor_data.values() 
                      if data.temperature is not None]
        
        if temp_values:
            avg_temp = statistics.mean(temp_values)
            if avg_temp > 35:
                recommendations.append("High soil temperature detected - consider shade or increased watering")
            elif avg_temp < 10:
                recommendations.append("Low soil temperature - plants may need protection")
        
        return recommendations if recommendations else ["All sensors reading within normal ranges"]
