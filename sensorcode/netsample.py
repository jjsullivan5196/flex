import sensorpure as sensor
import time

conn = sensor.getconnection()
sen = conn.connect()
sleeptime = 1.0/60.0

try:
	while True:
		t1 = time.time()
		data = next(sen)
		print('{:.2f},{:.2f},{:.2f},{:.2f}'.format(*data[0]))
		tsleep = sleeptime - (time.time() - t1)
		time.sleep(tsleep)
except KeyboardInterrupt:
	conn.disconnect()