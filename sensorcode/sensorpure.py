from serial import Serial
from coserver import UdpCoserver
import time
import string

_NETPORT = 5555
_COM = 'COM7'
_BAUD = 57600

def mix(xy, smoothFactor = 0.03, cap = 0.8):
        x,y = xy
        diff = (x - y) * smoothFactor
        if diff > 0:
            diff = min(diff, cap)
        else:
            diff = max(diff, cap * -1)
        return diff + y

def smooth(rawPoint, prevSmoothPoint):
    smoothPoint = [x for x in map(mix, zip(rawPoint, prevSmoothPoint))]
    slope = [sl for sl in map(lambda xy: (xy[0] - xy[1])**2 * 1000, zip(smoothPoint, prevSmoothPoint))]

    return smoothPoint, slope

def mirror(rawPoint, prevSmoothPoint):
    return rawPoint, [0.0] * 4

def edge(mstr, begin, end):
    try:
        first = mstr.index(begin) + 1
        last = mstr.index(end) - 1
        return mstr[first:last]
    except ValueError:
        return None

def readSerial(ser):
    pointSampled = False
    while not pointSampled:
        try:
            rawString = ser.readline().decode()
            ser.flush()
        except UnicodeError:
            print('Bad chars on serial')
            continue

        rawString = edge(rawString, 'a', 'b')

        if rawString == None:
            print('Delimeters not found')
            continue
       
        try:
            rawPoint = [float(x) for x in rawString.split(',')]
        except ValueError:
            print('String parse failed')
            continue

        if len(rawPoint) == 4:
            pointSampled = True
        else:
            print('Not enough data from serial')
            pointSampled = False
            continue
    
    return rawPoint


def sample(callback = smooth):
    prevSmoothPoint = [0.0] * 4
    with Serial(_COM, _BAUD, timeout=None) as ser:
        ser.flush()
        while True:
            rawPoint = readSerial(ser)            

            #return: (smoothPoint, slope)
            smoothPoint,slope = callback(rawPoint, prevSmoothPoint)
            prevRawPoint = rawPoint
            prevSmoothPoint = smoothPoint

            yield smoothPoint + slope

def getconnection(rem = 'localhost'):
    return UdpCoserver('8f', _NETPORT, framecallback = lambda x: (x[:4],x[4:]), remote = rem)

if __name__ == '__main__':
    server = UdpCoserver('8f', _NETPORT, generator = sample)
    server.serve()
