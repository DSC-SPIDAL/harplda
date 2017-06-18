#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage: analy_threadlog.py <logfile> <node> <thread>

"""
import sys, os, math,re
import logging
import numpy as np

logger = logging.getLogger(__name__)

class LDATrainerLog():
    pattern={
        "clock":"\[(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)\]",
        "harp-clock":"(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,[0-9]*)",
        "harp-newformat":"Iteration ([0-9]*): ([0-9]*), compute time: ([0-9]*), comm time: ([0-9]*)",
        "harp-newformat2":"Iteration ([0-9]*): ([0-9]*), compute time: ([0-9]*), misc: ([0-9]*)",
        #"harp-numTokens":"numTokens: ([0-9]*), schedule: [0-9]*",
        "harp-numTokens":"numTokens: ([0-9]*), percentage",
        "harp-compute":"Compute time: ([0-9]*), comm time: ([0-9]*)",
        "harp-iter":"Iteration [0-9]* took: ([0-9]*)",
    }

    def __init__(self):
        self.name = 'harp'

    def load_timelog_harp(self, logfile):
        """
        load elapsed millis of each iteration from logfile
    
        return:
            nparray
        """
        logf = open(logfile,'r')

        logf.seek(0,0)

        # iternum, itertime, computetime, numtokens
        iterinfo=[]
        # threadid, computetime, numtokens
        threadinfo=[] 
        for line in logf:

            #new format first
            #edu.iu.dymoro.Scheduler: Task 4 took 2120, trained 569926
            m = re.search("Scheduler: Task (\d+) took (\d+), trained (\d+)", line)
            if m:
                threadinfo.append((int(m.group(1)), int(m.group(2)),int(m.group(3))))

            #m = re.search(self.pattern[self.name+'-newformat'], line)
            m = re.search(self.pattern[self.name+'-newformat2'], line)
            if m:
                # check the numToken
                mx = re.search(self.pattern[self.name+'-numTokens'], line)
                if mx:
                    # iternum, numTokens
                    iterinfo.append((int(m.group(1)),  int(m.group(2)),int(m.group(3)),int(mx.group(1))))
                continue

        return np.array(iterinfo), np.array(threadinfo)


    def analy_log(self, logfile, node, slice, thread):
        iterinfo, threadinfo = self.load_timelog_harp(logfile)
        logger.info('iterinfo: %s, threadinfo: %s', iterinfo.shape, threadinfo.shape)

        # iternum, itertime, computetime, numtokens
        #iterinfo [][4]
        # threadid, computetime, numtokens
        #threadinfo, [][3]
        iternum = threadinfo.shape[0] / (node *slice* thread)
    
        diter = threadinfo.reshape((iternum, node*slice, thread, 3))
        aiter = iterinfo.reshape((iternum, 4))[:,2]

        #max time analysis
        diter_time = diter[:,:,:,1]
        itertime = np.sum(np.max(diter_time, axis=2), axis=1)
        cv = np.std(diter_time, axis=2)/np.mean(diter_time, axis=2)
        cvmax = np.max(cv, axis = 1)

        overhead = aiter - itertime
        
        logger.info('max thread occupy time: %s', itertime)
        logger.info('cvmax: %s', cvmax)
        logger.info('overhead: %s', overhead)
    
        #thread cpu usage analysis
        #total thread time / total compute time

        diter = threadinfo.reshape((iternum, node*slice*thread, 3))
        diter_time = np.sum(diter[:,:,1], axis = 1)
        #aiter = iterinfo[:,2]*thread
        usage = diter_time * 1.0 / (aiter*thread)
        logger.info('usage: %s', usage)

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    #logging.basicConfig(filename='debug_calcdistance.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                    level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    logfile = sys.argv[1]
    nodes = int(sys.argv[2])
    threads = int(sys.argv[3])
    ldalog = LDATrainerLog()

    ldalog.analy_log(logfile, nodes, 2, threads)
 
