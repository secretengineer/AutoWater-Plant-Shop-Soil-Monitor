# API Documentation for Soil Monitoring System

## Overview
This document provides an overview of the API endpoints available in the Soil Monitoring System.

## Endpoints

### 1. Get Sensor Data
- **URL**: `/api/sensors`
- **Method**: `GET`
- **Description**: Retrieves the latest sensor data.
- **Response**:
  ```json
  {
    "sensors": [
      {
        "id": "sensor1",
        "moisture": 30,
        "temperature": 22
      },
      ...
    ]
  }
  ```

### 2. Update Sensor Data
- **URL**: `/api/sensors`
- **Method**: `POST`
- **Description**: Updates the sensor data.
- **Request Body**:
  ```json
  {
    "id": "sensor1",
    "moisture": 35,
    "temperature": 23
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "message": "Sensor data updated."
  }
  ```

### 3. Get Dashboard Data
- **URL**: `/api/dashboard`
- **Method**: `GET`
- **Description**: Retrieves data for the dashboard.
- **Response**:
  ```json
  {
    "dashboard": {
      "total_sensors": 10,
      "active_sensors": 8,
      "alerts": [
        {
          "sensor_id": "sensor1",
          "message": "Low moisture level."
        }
      ]
    }
  }
  ```

## Authentication
- All endpoints require an API key for authentication. Include the API key in the request headers:
  ```
  Authorization: Bearer YOUR_API_KEY
  ```

## Conclusion
This API allows for seamless integration with the Soil Monitoring System, enabling real-time data access and updates.
