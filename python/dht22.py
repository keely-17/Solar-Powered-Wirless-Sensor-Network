import Adafruit_DHT
from datetime import datetime
import sqlite3
import os
import time

def read_and_store_dht_data():
    while True:
        base_dir = '/home/keely/Solar-Powered-Wirless-Sensor-Network'
        db_path = os.path.join(base_dir, 'data', 'weather.db')

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

                print(f"Data recorded at {current_time}")
                print(f"Temperature: {temperature:.1f}°F, Humidity: {humidity:.1f}%")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            time.sleep(300)  # Wait for 60 seconds before reading again

if __name__ == "__main__":
    read_and_store_dht_data()