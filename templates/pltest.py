from os import mkdir,path,listdir
import matplotlib.pyplot as plt
import sys
import csv

dirname = sys.argv[1] + '-trim'

try:
    mkdir(dirname)
except FileExistsError:
    pass

filelist = [f for f in listdir(sys.argv[1]) if path.isfile(path.join(sys.argv[1], f))]
origfiles = [path.join(sys.argv[1], f) for f in filelist]
writelist = [path.join(dirname, f) for f in filelist]
zlist = zip(origfiles, writelist)
origfile, newfile = next(zlist)

bline = None
btrim = 0

eline = None
etrim = 0

rawdata = None
datalines = []

colors = ['r','g','b','m']
fig = plt.figure(1)
pl = fig.add_subplot(111)
pl.set_ylabel('0-5V')


def plotgesture(fname):
    global rawdata
    global datalines
    rawdata = [[],[],[],[],[]]
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for num,datalist in zip(row, rawdata):
                datalist.append(float(num))
    if len(datalines) > 0:
        for line in datalines:
            line.remove()
        datalines = []
    for dlist,color in zip(rawdata[1:],colors):
        datalines.extend(pl.plot(dlist, color))
    plt.draw()
    

def boundevent(event):
    global bline
    global eline
    global btrim
    global etrim

    if event.button == 2:
        advance()
        return

    if event.xdata != None:
        if event.button == 1:
            if bline != None:
                bline.remove()
            bline = pl.axvline(event.xdata, color='r')
            btrim = int(event.xdata)
            print(btrim)
        elif event.button == 3:
            if eline != None:
                eline.remove()
            eline = pl.axvline(event.xdata, color = 'g')
            etrim = int(event.xdata)
            print(etrim)
    plt.draw()

def advance():
    global origfile
    global newfile
    global zlist
    global btrim
    global etrim
    with open(newfile, 'w') as nfile:
        wdata = list(zip(*rawdata))[btrim:etrim]
        wstrings = ['{},{},{},{},{}\n'.format(*row) for row in wdata]
        print('Template length: {}\nBegin: {}\nEnd: {}'.format(len(wdata), btrim, etrim))
        nfile.writelines(wstrings)
    try:
        origfile, newfile = next(zlist)
    except StopIteration:
        sys.exit(0)
    plotgesture(origfile)

fig.canvas.mpl_connect('button_press_event', boundevent)
plotgesture(origfile)
plt.show()
