# dashboard.py

from flask import render_template, jsonify, Flask, request

app = Flask(__name__)

# Mock sensor data for demonstration purposes
sensor_data = [
    {"id": "sensor 1", "moisture": 30},
    {"id": "sensor 2", "moisture": 45},
    {"id": "sensor 3", "moisture": 15},
    {"id": "sensor 4", "moisture": 5},
    {"id": "sensor 5", "moisture": 65},
    {"id": "sensor 6", "moisture": 85},
    {"id": "sensor 7", "moisture": 33},
    {"id": "sensor 8", "moisture": 53},
    # Add more mock sensors as needed
]

# Define a function to handle sensor data retrieval
def get_sensor_data():
    return sensor_data

@app.route('/dashboard')
def show_dashboard():
    """
    Render the dashboard HTML page.
    """
    return render_template('dashboard.html')

@app.route('/api/sensors')
def get_sensors():  
    """
    Fetch and return sensor data as JSON.

    Returns:
        Response: JSON response containing sensor data.
    """
    return jsonify({"sensors": get_sensor_data()})

@app.route('/api/sensors', methods=['PUT'])
def update_sensors():
    """
    Update sensor data via a PUT request.

    Returns:
        Response: JSON response indicating success or failure.
    """
    new_data = request.get_json()
    update_sensor_data(new_data)
    return jsonify({"message": "Sensor data updated successfully"})

def update_sensor_data(new_data):
    """
    Update the sensor data with new values.

    Args:
        new_data (dict): The new data to update the sensors with.
    """
    global sensor_data
    for sensor in sensor_data:
        if sensor['id'] in new_data:
            sensor['moisture'] = new_data[sensor['id']]

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
