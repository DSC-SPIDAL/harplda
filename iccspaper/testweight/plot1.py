import numpy as np
import matplotlib.pyplot as plt
from params import *

plt.rcParams.update(params)
# 500MB
lines = plt.plot(
                 x,
                 y500, 'ro-', color='r', markeredgecolor='r', label='Chain 0.5GB')
# 1GB
lines = plt.plot(
                 x,
                 y1000, 'rd-', color='r', markeredgecolor='r', label='Chain 1GB')
# 2GB
lines = plt.plot(
                 x,
                 y2000, 'r^-', color='r', markeredgecolor='r', label='Chain 2GB')
lines = plt.plot(
                 x,
                 [3.89, 4.63, 4.84, 4.83, 4.91, 4.92, 4.92], 'bo-', color='b', markeredgecolor='b', label='MPI 0.5GB')
lines = plt.plot(
                 x,
                 [7.89, 9.23, 9.72, 9.8, 9.75, 9.78, 9.89], 'bd-', color='b', markeredgecolor='b', label='MPI 1GB')
lines = plt.plot(
                 x,
                 [15.39, 18.39, 19.59, 19.74, 19.6, 19.55, 19.7], 'b^-', color='b', markeredgecolor='b', label='MPI 2GB')
plt.xticks(x)
plt.xlabel('Number of Nodes')
plt.ylabel('Execution Time (Seconds)')
plt.ylim(0, 30)
legend = plt.legend(loc='upper center', markerscale=0.5, ncol=2)
for label in legend.get_lines():
    label.set_linewidth(0.5)
plt.grid(True)
plt.tight_layout()
plt.savefig("bcast1.pdf")
