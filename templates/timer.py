from subprocess import call
import time

STOP_TIME = 8
tmp = call('cls', shell=True)

with open('longinput-script.txt', 'r') as f:
	ins = f.readlines()

for i in range(0, len(ins)):
	print(ins[i])
	if i < (len(ins) - 1):
		print('Next: ' + ins[i+1])
	else:
		print('Next: NONE')
	timer = time.time()
	elapsed = (time.time() - timer)
	while elapsed < STOP_TIME:
		print('\r {}'.format(STOP_TIME - elapsed), end="")
		elapsed = (time.time() - timer)
	tmp = call('cls', shell=True)