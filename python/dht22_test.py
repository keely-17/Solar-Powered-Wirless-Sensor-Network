import Adafruit_DHT
import time


sensor = Adafruit_DHT.DHT22
gpio = 4
wait = 5
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
temperature = (9/5) * temperature + 32

if humidity is not None and temperature is not None: 
    print(f"Temp: {temperature:.1f}F")
    print(f"hum: {humidity:.1f}")
    time.sleep(wait)
    print("goodbye")