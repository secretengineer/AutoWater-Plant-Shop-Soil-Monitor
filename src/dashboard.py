# dashboard.py

from flask import render_template, jsonify, Flask, request

app = Flask(__name__)

# Mock sensor data for demonstration purposes
sensor_data = [
    {"id": "sensor1", "moisture": 30},
    {"id": "sensor2", "moisture": 45},
    # Add more mock sensors as needed
]

# Define a function to handle sensor data retrieval
def get_sensor_data():
    return sensor_data

@app.route('/dashboard')
def show_dashboard():
    return render_template('dashboard.html')

@app.route('/api/sensors')
def get_sensors():
    # Return the mock sensor data
    return jsonify({"sensors": get_sensor_data()})

# Define a function to handle sensor data updates
def update_sensor_data(new_data):
    global sensor_data
    sensor_data = new_data

# Define a route to update sensor data
@app.route('/api/sensors', methods=['PUT'])
def update_sensors():
    new_data = request.get_json()
    update_sensor_data(new_data)
    return jsonify({"message": "Sensor data updated successfully"})

if __name__ == "__main__":
    app.run(debug=True)
