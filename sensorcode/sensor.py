from serial import Serial
import time
import string

_SAMPLES_STORED = 150
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

def smooth(rawPoint, prevRawPoint, prevSmoothPoint):
    smoothPoint = [x for x in map(mix, zip(rawPoint, prevSmoothPoint))]
    slope = [sl for sl in map(lambda xy: (xy[0] - xy[1])**2 * 1000, zip(smoothPoint, prevSmoothPoint))]

    return smoothPoint, slope

def mirror(rawPoint, prevRawPoint, prevSmoothPoint):
    return rawPoint, [0.0] * 4

def edge(mstr, begin, end):
    try:
        first = mstr.index(begin) + 1
        last = mstr.index(end) - 1
        return mstr[first:last]
    except ValueError:
        return None

def sample(callback = smooth, frequency = None, sampleTime = None):
    rawPoint = [0.0] * 4
    prevRawPoint = [0.0] * 4
    smoothPoint = [0.0] * 4
    prevSmoothPoint = [0.0] * 4
    slope = [0.0] * 4
    condition = None
    rawString = None
    sleeptime = None

    if frequency != None:
        sleeptime = 1.0/frequency
    else:
        sleeptime = 0.0

    if sampleTime != None:
        condition = lambda x,y,z: z < x*y
    else:
        condition = lambda x,y,z: True

    with Serial(_COM, _BAUD, timeout=None) as ser:
        ser.readline()
        ser.flush()
        frames = 0
        tnext = 0.0
        while condition(sampleTime,frequency,frames):
            pointSampled = False
            while time.time() < tnext or not pointSampled:
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

                #return: (smoothPoint, slope)
                smoothPoint,slope = callback(rawPoint, prevRawPoint, prevSmoothPoint)
                prevRawPoint = rawPoint
                prevSmoothPoint = smoothPoint
            
            tnext = time.time() + sleeptime
            frames += 1
            yield smoothPoint, slope

if __name__ == '__main__':
    for value,slope in sample(callback = smooth, frequency = 60):
        print("{:.2f},{:.2f},{:.2f},{:.2f}".format(*value))
