from flask import Flask, jsonify, render_template
import sqlite3
import os
from flask import Flask, jsonify, render_template
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

base_dir = '/home/keely/Solar-Powered-Wirless-Sensor-Network'
db_path = os.path.join(base_dir, 'data', 'weather.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/latest')
def get_latest_data():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 1")
        data = cursor.fetchone()
        conn.close()

        if data:
            return jsonify({
                "timestamp": data[0],
                "temperature": round(data[1], 1),
                "humidity": round(data[2], 1)
            })
        else:
            return jsonify({"error": "No data available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/historical/<date>')
def get_data_by_date(date):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data WHERE DATE(timestamp) = DATE(?)", (date,))
        data = cursor.fetchall()
        conn.close()
        
        if data:
            return jsonify([{
                "timestamp": row[0],
                "temperature": round(row[1], 1),
                "humidity": round(row[2], 1)
            } for row in data])
        else:
            return jsonify({"error": "No data available for the specified date"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/range/<start_date>/<end_date>')
def get_data_range(start_date, end_date):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data WHERE DATE(timestamp) BETWEEN DATE(?) AND DATE(?)", (start_date, end_date))
        data = cursor.fetchall()
        conn.close()
        
        if data:
            return jsonify([{
                "timestamp": row[0],
                "temperature": round(row[1], 1),
                "humidity": round(row[2], 1)
            } for row in data])
        else:
            return jsonify({"error": "No data available for the specified date range"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001)
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=args.port)