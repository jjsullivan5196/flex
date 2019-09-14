import sys
import os


fnames = ['joined.csv','s0.csv','s1.csv','s2.csv','s3.csv']
dirname = sys.argv[1]
label = sys.argv[2]
newdir = dirname + '-label' + str(label)


if not os.path.exists(newdir):
    os.makedirs(newdir)

nfnames = [newdir + '/' + name for name in fnames]
oldnames = [dirname +'/' + name for name in fnames]

for name,oldname in zip(nfnames,oldnames):
    infile = open(oldname, 'r')
    outfile = open(name, 'w')

    for line in infile:
        lsline = list(line)
        if lsline[0] != '0':
            lsline[0] = str(label)
        line = ''.join(lsline)
        outfile.write(line)

    infile.close()
    outfile.close()
