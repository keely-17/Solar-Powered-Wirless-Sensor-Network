import sys
import Adafruit_DHT
import time
from datetime import datetime#+
import sqlite3#+
import json#+

# Database setup#+
conn = sqlite3.connect('/home/keely/Solar-Powered-Wirless-Sensor-Network/data/weather.db')#+
cursor = conn.cursor()#+
cursor.execute('''#+
    CREATE TABLE IF NOT EXISTS weather_data#+
    (timestamp TEXT, temperature REAL, humidity REAL)#+
''')#+
conn.commit()#+

sensor = Adafruit_DHT.DHT22
gpio = 4
wait = 300  # 5 minutes#+

while True:
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        temperature = (9/5) * temperature + 32
 
        current_time = datetime.now().isoformat()#+
#+
        if humidity is not None and temperature is not None:#+
            # Insert data into SQLite database#+
            cursor.execute(#+
                "INSERT INTO weather_data (timestamp, temperature, humidity) VALUES (?, ?, ?)",#+
                (current_time, temperature, humidity)#+
            )#+
            conn.commit()#+
#+
            # Write latest data to a JSON file for easy access#+
            latest_data = {#+
                "timestamp": current_time,#+
                "temperature": round(temperature, 1),#+
                "humidity": round(humidity, 1)#+
            }#+
            with open("/home/keely/Solar-Powered-Wirless-Sensor-Network/data/latest.json", "w") as f:#+
                json.dump(latest_data, f)#+
#+
            print(f"Data recorded at {current_time}")#+
            print(f"Temperature: {temperature:.1f}°F, Humidity: {humidity:.1f}%")#+
#+
        time.sleep(wait)#+
    except KeyboardInterrupt:
        conn.close()#+
        sys.exit("Session ended by Administrator. Goodbye")