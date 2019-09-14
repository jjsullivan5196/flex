import sensorpure as sensor

conn = sensor.getconnection()
try:
	for value in conn.connect():
		print(value)
except KeyboardInterrupt:
	conn.disconnect()