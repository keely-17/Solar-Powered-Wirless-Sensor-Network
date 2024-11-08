from flask import Flask, jsonify, render_template
import sqlite3
# import json

app = Flask(__name__)

@app.route('/templates/home.html')
def home():
    return render_template('home.html')

@app.route('/api/latest')
def get_latest_data():
    # Connect to the database
    conn = sqlite3.connect('/home/keely/Solar-Powered-Wirless-Sensor-Network/data/weather.db')
    cursor = conn.cursor()
    
    # Fetch the latest data
    cursor.execute("SELECT timestamp, temperature, humidity FROM weather_data ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            "timestamp": row[0],
            "temperature": row[1],
            "humidity": row[2]
        })
    else:
        return jsonify({"error": "No data available"}), 404

@app.route('/api/data/<date>')
def get_data_by_date(date):
    conn = sqlite3.connect('/home/keely/Solar-Powered-Wirless-Sensor-Network/data/weather.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_data WHERE timestamp LIKE ?", (f"{date}%",))
    data = cursor.fetchall()
    conn.close()
    return jsonify([{"timestamp": row[0], "temperature": row[1], "humidity": row[2]} for row in data])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)