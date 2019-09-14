import sys
import os
import sensor
import argparse

_SAMPLES = 60
_TEMPLATES = 2000
_FREQUENCY = 60
_NAME = 'test'
_LABEL = 1

def saveseries(name, series):
    if not os.path.exists(name):
        os.makedirs(name)

    joined = open(name + '/joined.csv', 'a')
    idv = []
    classLabel = series[0][0]
    for i in range(4):
        idv.append(open(name + '/s' + str(i) + '.csv', 'a'))
        idv[i].write(str(classLabel))
    
    for value in series:
        if classLabel != value[0]:
            classLabel = value[0]
            for f in idv:
                f.write('\n' + str(classLabel))

        joined.write('{},{},{},{},{}\n'.format(*value))
        for f,x in zip(idv, value[1:]):
            f.write(',' + str(x))

    joined.close()
    for f in idv:
        f.write('\n')
        f.close()

series = []

if __name__ == '__main__':
    print('')
    goText = 'STOP'
    samples = 0
    templates = 0
    classLabel = 0

    parser = argparse.ArgumentParser(description = 'Record training templates')
    parser.add_argument('--ntemp', dest='numtemplates', type=int, default=_TEMPLATES, help='number of templates to store')
    parser.add_argument('--nsample', dest='numsamples', type=int, default=_SAMPLES, help='number of samples per template')  
    parser.add_argument('--freq', dest='frequency', type=int, default=_FREQUENCY, help='sampling frequency (Hz)')
    parser.add_argument('--name', dest='output', type=str, default=_NAME, help='output directory')
    parser.add_argument('--label', dest='classLabel', type=int, default=_LABEL, help='class label number')
    
    args = parser.parse_args()

    try:
        for value,slope in sensor.sample(frequency = args.frequency): 
            if samples >= args.numsamples:
                templates += 1
                if templates >= args.numtemplates:
                    break
                samples = 0
                if classLabel == args.classLabel:
                    goText = 'STOP'
                    classLabel = 0
                else:
                    goText = '  GO'
                    classLabel = args.classLabel

            print('\r{}: {:02} - Samples left: {:04}'.format(goText,int((args.numsamples - samples)/args.frequency),(args.numtemplates - templates)), end='')
            series.append([classLabel, *value])
            samples += 1
        
        saveseries(args.output, series)
    except KeyboardInterrupt:
        saveseries(args.output, series)
