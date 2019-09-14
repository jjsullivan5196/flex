from serial import Serial
import struct
import time

bpack = struct.Struct('BHBHBHBH')

with Serial('COM7', 57600, timeout=None) as ser:
	while True:
		print(ser.readline())
			