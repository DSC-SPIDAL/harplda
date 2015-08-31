import os, sys

import time

start = time.time()

#cmd = "/scratch/pengb/ylda/learntopics --iter=1000 --topics=2000 --alpha=20 --beta=0.01  --optimizestats=5000 --samplerthreads=8"
cmd = sys.argv[1]
os.system(cmd)

end = time.time()
print end - start
print (end - start)/3600.
