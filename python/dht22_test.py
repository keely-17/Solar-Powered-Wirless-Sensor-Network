import sys
import Adafruit_DHT
import time


sensor = Adafruit_DHT.DHT22
gpio = 4
wait = 5
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
temperature = (9/5) * temperature + 32

while True:
    try:
        if humidity is not None and temperature is not None: 
            
            with open("/home/keely/Solar-Powered-Wirless-Sensor-Network/data/log.data", 'a') as file:
                file.write(f"{temperature}\n{humidity}\n")
            print(f"Temp: {temperature:.1f}F")
            print(f"hum: {humidity:.1f}")
            time.sleep(wait)
    except KeyboardInterrupt:
        with open("/home/keely/Solar-Powered-Wirless-Sensor-Network/data/log.data", 'a') as file:
            file.write("Session ended by Administrator. Goodbye.")        
        sys.exit("Session ended by Administrator. Goodbye")