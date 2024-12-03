from flask import Flask, jsonify, render_template, request
import sqlite3
import os
from datetime import datetime, timedelta
import statistics

app = Flask(__name__)

base_dir = '/home/keely/Solar-Powered-Wirless-Sensor-Network'
db_path = os.path.join(base_dir, 'data', 'weather.db')

@app.route('/')
def index():
    return render_template('historical.html')

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

@app.route('/api/historical')
def get_historical_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date', start_date)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query = """
        SELECT 
            DATE(timestamp) as date,
            AVG(temperature) as avg_temp,
            MIN(temperature) as min_temp,
            MAX(temperature) as max_temp,
            AVG(humidity) as avg_humidity,
            MIN(humidity) as min_humidity,
            MAX(humidity) as max_humidity
        FROM weather_data 
        WHERE DATE(timestamp) BETWEEN DATE(?) AND DATE(?)
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
        """
        
        cursor.execute(query, (start_date, end_date))
        data = cursor.fetchall()
        conn.close()
        
        if data:
            result = [{
                "date": row[0],
                "avg_temperature": round(row[1], 1),
                "min_temperature": round(row[2], 1),
                "max_temperature": round(row[3], 1),
                "avg_humidity": round(row[4], 1),
                "min_humidity": round(row[5], 1),
                "max_humidity": round(row[6], 1)
            } for row in data]
            return jsonify(result)
        else:
            return jsonify({"error": "No data available for the specified date range"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/historical/details')
def get_historical_details():
    date = request.args.get('date')
    
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
            return jsonify({"error": "No detailed data available for the specified date"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/detail')
def detail_page():
    return render_template('detail.html')

@app.route('/api/detail/<date>')
def get_detail_data(date):
    try:
        # Validate the date format
        datetime.strptime(date, '%Y-%m-%d')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data WHERE DATE(timestamp) = DATE(?)", (date,))
        data = cursor.fetchall()

        if data:
            return jsonify([{
                "timestamp": row[0],
                "temperature": round(row[1], 1),
                "humidity": round(row[2], 1)
            } for row in data])
        else:
            return jsonify({"error": "No data available for the specified date"}), 404
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001)
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=args.port)