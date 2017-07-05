#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage: analy_threadlog.py <trainer> <logfile> <node> <thread>
    trainer:    harp, nomadlda, lightlda

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

    trainers=['mallet','harp','ylda','warplda','lightlda','nomadlda','petuum','petuum-run','petuum-new']
    def __init__(self,name, node, thread):
        if name not in self.trainers:
            raise NameError('no %s trainer support yet, quit.'%name)
        self.name = name
        self.node = node
        self.thread = thread
        self.engine={
            'harp':self.load_threadlog_harp,
            'nomadlda':self.load_threadlog_nomadlda,
            'lightlda':self.load_threadlog_lightlda
        }

    def load_threadlog(self, logdir):
        return self.engine[self.name](logdir)


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


    def load_threadlog_harp(self, logfile):
        node = self.node
        thread = self.thread
        slice = 2
        iterinfo, threadinfo = self.load_timelog_harp(logfile)
        logger.info('iterinfo: %s, threadinfo: %s', iterinfo.shape, threadinfo.shape)

        appname = logfile[:logfile.rfind('.')]
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

        #save as .compute-stat
        computeMatrix = np.zeros((thread,iternum))
        diter = threadinfo.reshape((iternum, node*slice*thread, 3))
        for iter in range(iternum):
            for idx in range(node*slice*thread):
                threadid = diter[iter,idx,0]
                threadtime = diter[iter,idx,1]
                computeMatrix[threadid , iter] += threadtime

        np.savetxt(appname + ".computetime", computeMatrix, fmt='%d')

        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(computeMatrix, axis=0)
        statMatrix[1] = np.max(computeMatrix, axis=0)
        statMatrix[2] = np.mean(computeMatrix, axis=0)
        statMatrix[3] = np.std(computeMatrix, axis=0)
        np.savetxt(appname + '.comput-stat', statMatrix,fmt='%.2f')

        #overhead = itertime - thread compute time
        aiter = iterinfo.reshape((iternum, 4))[:,1].reshape((1,iternum))
        overheadMatrix = np.zeros((thread,iternum))
        for threadid in range(thread):
            #overheadMatrix[threadid] = aiter - computeMatrix[threadid]
            overheadMatrix[threadid] = (aiter - computeMatrix[threadid]) *1.0 /aiter

        np.savetxt(appname + ".overheadtime", overheadMatrix, fmt='%.4f')

        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(overheadMatrix, axis=0)
        statMatrix[1] = np.max(overheadMatrix, axis=0)
        statMatrix[2] = np.mean(overheadMatrix, axis=0)
        statMatrix[3] = np.std(overheadMatrix, axis=0)
        np.savetxt(appname + '.overhead-stat', statMatrix,fmt='%.4f')

    #=============================================
    def load_timelog_nomadlda(self, logfile):
        """
        #format: "rank 0 iter 1 localthread duration time: 49.4224,19.7859,
        """
        logf = open(logfile,'r')
        # threadid, computetime
        threadinfo=[] 
        for line in logf:

            #new format first
            #edu.iu.dymoro.Scheduler: Task 4 took 2120, trained 569926
            m = re.search("rank \d+ iter (\d+) localthread duration time: (.*)", line)
            if m:
                #threadtime = [x for x in m.group(2).split(',')][:-1]
                #logger.debug('threadtime: %s',threadtime)
                threadtime = [1000 * float(x) for x in m.group(2).split(',')[:-1]]
                threadinfo.append(threadtime)

        return np.array(threadinfo)

       
    def load_threadlog_nomadlda(self, logfile):
        # node parameter here is the timeout, the iter time of nomad
        totaltime = self.node

        threadinfo = self.load_timelog_nomadlda(logfile)
        logger.info('threadinfo: %s', threadinfo.shape)

        iternum, thread = threadinfo.shape

        appname = logfile[:logfile.rfind('.')]
        #save as .compute-stat
        computeMatrix = np.transpose(threadinfo)
        np.savetxt(appname + ".computetime", computeMatrix, fmt='%d')

        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(computeMatrix, axis=0)
        statMatrix[1] = np.max(computeMatrix, axis=0)
        statMatrix[2] = np.mean(computeMatrix, axis=0)
        statMatrix[3] = np.std(computeMatrix, axis=0)
        np.savetxt(appname + '.comput-stat', statMatrix,fmt='%.2f')


        #overheadMatrix = np.zeros((thread,iternum))
        overheadMatrix = (totaltime - computeMatrix)*1.0/ totaltime
        np.savetxt(appname + ".overheadtime", overheadMatrix, fmt='%.4f')

        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(overheadMatrix, axis=0)
        statMatrix[1] = np.max(overheadMatrix, axis=0)
        statMatrix[2] = np.mean(overheadMatrix, axis=0)
        statMatrix[3] = np.std(overheadMatrix, axis=0)
        np.savetxt(appname + '.overhead-stat', statMatrix,fmt='%.4f')

    #===============================================
    def load_timelog_lightlda(self, logfile):
        """
        #[INFO] [2017-06-12 01:40:40] Rank = 0, Threadid = 3, Training Time used: 13.10 s
        """
        logf = open(logfile,'r')
        # threadid, computetime
        threadinfo=[] 
        for line in logf:

            #new format first
            #edu.iu.dymoro.Scheduler: Task 4 took 2120, trained 569926
            m = re.search("Rank = \d+, Threadid = (\d+), Training Time used: (\d+\.\d+) s", line)
            if m:
                #threadid, time
                threadinfo.append((int(m.group(1)), 1000*float(m.group(2))))

        return np.array(threadinfo)


    def load_threadlog_lightlda(self, logfile):
        # node parameter here is the slice number
        slice = self.node
        thread = self.thread

        threadinfo = self.load_timelog_lightlda(logfile)
        logger.info('threadinfo: %s', threadinfo.shape)

        iternumX = threadinfo.shape[0] / (slice* thread)
        appname = logfile[:logfile.rfind('.')]
        #load .itertime
        iterfile = appname + '.itertime'
        if os.path.exists(iterfile):
            itertime = np.loadtxt(iterfile)
            logger.info('itertime shape = %s', itertime.shape)
            iternum = itertime.shape[0]
        else:
            logger.info('.itertime not found, quit')
            return

        #save as .compute-stat
        computeMatrix = np.zeros((thread,iternum))
        diter = threadinfo.reshape((iternumX, slice*thread, 2))
        for iter in range(iternum):
            for idx in range(slice*thread):
                threadid = diter[iter,idx,0]
                threadtime = diter[iter,idx,1]
                computeMatrix[threadid , iter] += threadtime
   
        np.savetxt(appname + ".computetime", computeMatrix, fmt='%d')

        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(computeMatrix, axis=0)
        statMatrix[1] = np.max(computeMatrix, axis=0)
        statMatrix[2] = np.mean(computeMatrix, axis=0)
        statMatrix[3] = np.std(computeMatrix, axis=0)
        np.savetxt(appname + '.comput-stat', statMatrix,fmt='%.2f')

        overheadMatrix = np.zeros((thread,iternum))
        for threadid in range(thread):
            overheadMatrix[threadid] = (itertime - computeMatrix[threadid][:iternum]) *1.0 / itertime
        np.savetxt(appname + ".overheadtime", overheadMatrix, fmt='%.4f')

        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(overheadMatrix, axis=0)
        statMatrix[1] = np.max(overheadMatrix, axis=0)
        statMatrix[2] = np.mean(overheadMatrix, axis=0)
        statMatrix[3] = np.std(overheadMatrix, axis=0)
        np.savetxt(appname + '.overhead-stat', statMatrix,fmt='%.4f')



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

    trainer = sys.argv[1]
    logfile = sys.argv[2]
    nodes = int(sys.argv[3])
    threads = int(sys.argv[4])

    logAnalizer = LDATrainerLog(trainer, nodes, threads)

    logAnalizer.load_threadlog(logfile)
