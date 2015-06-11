#This script slip corpus into 15 70 15 percentage for DEV, TRAIN, TEST
import sys
import scipy.io
import numpy as np
import random
import re
import os
import glob
import math
import string

if len(sys.argv) < 2:
    print "usage: gibbs phi input, output blei beta file"
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

##########get beta in ldac format from sequence file format#########3
def getBeta(rawBeta, vSize):
    values = rawBeta.split(" ")
    output =list()

    sum = 0.0
    for prob in values:
        sum += float(prob)
        output.append(str(math.log(float(prob))))

    print "SUM is ",str(sum)
    return " ".join(output)


#########
output =open(output_file,"w")
#read all text file from dir
with open(input_file) as docFile:
    for docLine in docFile:
        output.write(getBeta(docLine.rstrip(), vocab_size)+"\n")
output.close()
