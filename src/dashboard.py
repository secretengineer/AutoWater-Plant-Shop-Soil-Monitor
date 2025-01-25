# dashboard.py

from flask import render_template, jsonify, Flask

app = Flask(__name__)

# Global variable to hold sensor data for testing
sensor_data = [
    {"id": "sensor1", "moisture": 30},
    {"id": "sensor2", "moisture": 45},
    # Add more mock sensors as needed
]

@app.route('/dashboard')
def show_dashboard():
    return render_template('dashboard.html')

@app.route('/api/sensors')
def get_sensors():
    # Return the mock sensor data
    return jsonify({"sensors": sensor_data})

def update(data: dict) -> None:
    """
    Update the dashboard with new data.

    Args:
        data (dict): The new data to update the dashboard with.
    """
    # Update the global sensor data for demonstration purposes
    for sensor in sensor_data:
        if sensor['id'] in data:
            sensor['moisture'] = data[sensor['id']]

if __name__ == "__main__":
    app.run(debug=True)
