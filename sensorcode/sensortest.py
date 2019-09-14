import sensor
import time

sensor.start()

while True:
    if len(sensor.data) > 1:
        print(sensor.slope)
