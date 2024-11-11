import Adafruit_DHT
from datetime import datetime
import sqlite3
import json
import os
import time

def read_and_store_dht_data():
    while True:
        base_dir = '/home/keely/Solar-Powered-Wirless-Sensor-Network'
        db_path = os.path.join(base_dir, 'data', 'weather.db')
        json_path = os.path.join(base_dir, 'data', 'latest.json')

        # Database setup
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sensor = Adafruit_DHT.DHT22
        gpio = 4

        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
            temperature = (9/5) * temperature + 32

            current_time = datetime.now().isoformat()

            if humidity is not None and temperature is not None:
                # Insert data into SQLite database
                cursor.execute(
                    "INSERT INTO weather_data (timestamp, temperature, humidity) VALUES (?, ?, ?)",
                    (current_time, temperature, humidity)
                )
                conn.commit()

                # Write latest data to a JSON file for easy access
                # latest_data = {
                #     "timestamp": current_time,
                #     "temperature": round(temperature, 1),
                #     "humidity": round(humidity, 1)
                # }
                # with open(json_path, "w") as f:
                #     json.dump(latest_data, f)

                print(f"Data recorded at {current_time}")
                print(f"Temperature: {temperature:.1f}°F, Humidity: {humidity:.1f}%")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            time.sleep(60)  # Wait for 60 seconds before reading again

if __name__ == "__main__":
    read_and_store_dht_data()