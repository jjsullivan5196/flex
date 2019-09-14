import random
import numpy as np
import scipy.stats as st

np.seterr(all='raise')

_FRAC = [0.5,0.7]

def writedata(series, name):
    f = open(name, 'w')
    for s in series:
        label, values = s
        f.write(str(label + 1))
        for v in values:
            f.write(',' + str(v))
        f.write('\n')
    f.close()

def writedatalines(series, name):
    f = open(name, 'w')
    for s in series:
        label, values = s
        for v in values:
            f.write(str(label) + ',' + str(v))
            f.write('\n')
    f.close()

def partition(snames, classes):
    # Sample data
    for i,sname in enumerate(snames):
        train,test,ex = [],[],[]
        for cl in classes:
            cls = cl[i]
            if len(cls) > 0:
                train.extend(cls[:int(len(cls) * _FRAC[0])])
                test.extend(cls[int(len(cls) * _FRAC[0]):int(len(cls) * _FRAC[1])])
                ex.extend(cls[int(len(cls) * _FRAC[1]):])

        writedata(train, 'ArmSensor_' + sname + '_TRAIN')
        writedata(test, 'ArmSensor_' + sname + '_TEST')
        writedata(test, 'ArmSensor_' + sname + '_EX')

def writeout(snames, classes):
    for i,sname in enumerate(snames):
        out = []
        for cl in classes:
            cls = cl[i]
            if len(cls) > 0:
                out.extend(cls)
        writedata(out, 'ArmSensor_' + sname + '_EX')

def red(x, y):
    if x == y:
        return 1
    else:
        return 0

def process(dirnames, seed, sample):
    random.seed(seed)
    snames = ['s0','s1','s2','s3']
    sensors = ([],[],[],[])
    classes = [[[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]]]

    # Organize and normalize data
    '''
    for dname in dirnames:
        for name,sensor in zip(snames, sensors):
            f = open(dname + '/' + name + '.csv', 'r')
            for line in f:
                sep = line.split(',')
                label = int(sep.pop(0))
                values = np.array([float(x) for x in sep])
                try:
                    normvalues = st.zscore(values)
                except Exception:
                    print('Divide by zero')
                    continue
                sensor.append((label,normvalues))
            f.close()
    '''
    for dname in dirnames:
        files = [open(dname + '/' + name + '.csv', 'r') for name in snames]
        for lines in zip(*files):
            separated = [line.split(',') for line in lines]
            labels = [red(int(sep.pop(0)),4) for sep in separated]
            try:
                normalized = [st.zscore(np.array([float(x) for x in sep])) for sep in separated]
            except Exception:
                print('Divide by zero')
                continue
            for label,normed,sensor in zip(labels,normalized, sensors):
                sensor.append((label,normed))

    # Separate classes
    for i,sensor in enumerate(sensors):
        for s in sensor:
            label,values = s
            classes[label][i].append(s)
    
    # Shuffle lists, sample data
    for cl,value in enumerate(classes):
        rows = [row for row in zip(*value)]
        random.shuffle(rows)
        reshape = [[],[],[],[]]
        for row in rows:
            for ent,lst in zip(row,reshape):
                lst.append(ent)
        classes[cl] = reshape

        #for sensor in value:
            #random.shuffle(sensor)

    sample(snames, classes)


if __name__ == '__main__':
    process(['theospread','theodbtap','theowr','theowl','theofist','johnfist','johnwl','johnspread','johnwr','johndbtap','phucdbtap','phucwr','phucspread','phucwl','phucfist'], 48093720473, partition)
	
