#!/usr/bin/env python
import sys

import os

fp = open(sys.argv[1]);
mtrain = int(sys.argv[2]);

trainname = sys.argv[1]+".train";
testname = sys.argv[1]+".test";
fmeta = open("meta","w");
ftrain = open(trainname,"w");
ftest = open(testname, "w");

m = int(fp.readline().strip());
n = int(fp.readline().strip());
nnz = int(fp.readline().strip());
totaltrain = 0;
nnztrain = 0;
totaltest = 0;
nnztest = 0;

for i in range(nnz):
	line =fp.readline();
	if len(line) == 0:
		print "error format!\n"
		break
	sp = line.strip().split(" ");
	d = int(sp[0]);
	w = int(sp[1]);
	v = int(sp[2]);
	if d <= mtrain:
		ftrain.write(line);
		totaltrain = totaltrain + v;
		nnztrain = nnztrain + 1;
	else:
		ftest.write("%d %d %d\n"%(d-mtrain, w, v));
		totaltest = totaltest + v;
		nnztest = nnztest + 1;

fmeta.write("%d\n"%(n));
fmeta.write("%d %d %d %s\n"%(mtrain, nnztrain, totaltrain, trainname));
fmeta.write("%d %d %d %s\n"%(m-mtrain, nnztest, totaltest, testname));
ftrain.close();
ftest.close();
fmeta.close();
