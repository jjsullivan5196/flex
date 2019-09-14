from os import mkdir,path,listdir
from collections import deque
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import csv
import sensorpure as sensor

font = { 'weight' : 'bold',
         'size'   : 50}
matplotlib.rc('font', **font)

SAMPLES_STORED = 450

colors = ['r','g','b','m']
fig = plt.figure(1, figsize=(40,40), dpi=20)
smooth = fig.add_subplot(211)
slope = fig.add_subplot(212)
smooth.set_ylabel('0-5V')

smooth.set_ylim([0.0,5.0])
slope.set_ylim([0.0,2.0])

smoothdata = [
        deque([0.0] * SAMPLES_STORED, maxlen=SAMPLES_STORED),
        deque([0.0] * SAMPLES_STORED, maxlen=SAMPLES_STORED),
        deque([0.0] * SAMPLES_STORED, maxlen=SAMPLES_STORED),
        deque([0.0] * SAMPLES_STORED, maxlen=SAMPLES_STORED)
]

slopedata = [
        deque([0.0] * SAMPLES_STORED, maxlen=SAMPLES_STORED),
        deque([0.0] * SAMPLES_STORED, maxlen=SAMPLES_STORED),
        deque([0.0] * SAMPLES_STORED, maxlen=SAMPLES_STORED),
        deque([0.0] * SAMPLES_STORED, maxlen=SAMPLES_STORED)
]

smoothlines = []
slopelines = []

#stuff here

for series,color in zip(smoothdata,colors):
    smoothlines.extend(smooth.plot(series, color))

for series,color in zip(slopedata,colors):
    slopelines.extend(slope.plot(series, color))

def animate(sampler):
    value,deriv = sampler
    for v,d,vseries,dseries,vline,dline in zip(value,deriv,smoothdata, slopedata, smoothlines, slopelines):
        vseries.append(v)
        dseries.append(d)
        vline.set_ydata(vseries)
        dline.set_ydata(dseries)
    return tuple(smoothlines + slopelines)

def init():
    return animate(([0.0] * 4, [0.0] * 4))

conn = sensor.getconnection()

ani = animation.FuncAnimation(fig, animate, conn.connect(), init_func=init, interval=0, blit = True)

plt.show()
conn.disconnect()
