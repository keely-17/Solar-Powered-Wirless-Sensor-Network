import Adafruit_DHT
import time
import board
import busio


sensor = Adafruit_DHT.DHT22
gpio = 4


humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
print(f"hum: {humidity:.1f}")



if humidity is not None and temperature is not None: 
    temperature = (9/5) * temperature + 32
    print(f" Temp: {temperature:.1f}F")