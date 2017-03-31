import sys
import numpy as np

#load in .runtime-stat
if len(sys.argv) < 3:
    print('usage: loadRuntimeByIter <runtimefile> <iter number>')
    sys.exit(0)

runtime=np.loadtxt(sys.argv[1])
print('Iter %d, runtime=%s', sys.argv[2], runtime[2][int(sys.argv[2])-1 + 2])
