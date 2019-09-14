import os
import numpy as np
import scipy.stat as st

def normdata(dirs):
    for name in dirs:
        outname = name + '-znorm'
        if not os.path.exists(outname):
            os.makedirs(outname)
        for fname in os.listdir(name):
            values = [[],[],[],[],[]]
            zvalues = []
            f = open(fname, 'r')
            for line in f:
                items = line.split(',')
                for item,dlist in zip(items, values): dlist.append(item)
            zvalues.extend(np.array(values.pop(0)))
            for vlist in values:
                arr = np.array(vlist)
                zvalues.extend(st.zscore(arr))
            f.close()

            fout = open(outname + '/' + fname, 'w')
            for val in zip(*zvalues):
                fout.write('{},{},{},{},{}\n'.format(*val))

normdata(['inputs','separated-templates'])
