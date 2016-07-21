import numpy as np
import sys

if len(sys.argv) < 3:
    print('usage: reshape <file> <colNum>')
    sys.exit(0)


filename = sys.argv[1]
colNum = int(sys.argv[2])

d = np.loadtxt(filename)
np.savetxt(filename, d[:,:colNum], fmt='%.02f')

