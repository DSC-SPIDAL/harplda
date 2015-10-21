#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Analysis the log file of lda trainers to measure the performance

input:
    lda trainer's log dir

format:
    mallet : ^[0-9]+ms  
        pass
        
    ylda   : learntopics.INFO.$HOSTNAME, all nodes' log in one directory
        $appname/interval_model/global/learntopics.INFO.$HOSTNAME
         1 Log file created at: 2015/10/21 10:27:14
         Log line format: [IWEF]mmdd hh:mm:ss.uuuuuu threadid file:line] msg
         W1021 10:37:32.546551 15315 Training_Execution_Strategy.cpp:57] Starting Parallel training Pipeline
         Iteration 1 done. Took 0.384061 mins
         Synch pass 1 done. Took 231.369 seconds


    harp   : hadoop user logs, syslog, each node has one directory
        Compute time: 88900, comm time: 18103


Usage: 
    analy_timelog <trainer> <appdir> <figname>

"""

import sys,os,re
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class LDATrainerLog():
    trainers=['mallet','harp','ylda']
    pattern={
        "mallet":"^([0-9]+)ms",
        "harp":"Compute time: ([0-9]*), comm time: ([0-9]*)",
        "ylda-compute":"Iteration ([0-9]*) done. Took ([0-9\.]*) mins",
        "ylda-commu":"Synch pass ([0-9]*) done. Took ([0-9\.]*) seconds"
    }

    def __init__(self,name):
        if name not in self.trainers:
            raise NameError('no %s trainer support yet, quit.'%name)
        self.name = name
        self.engine={
            'harp':self.load_applog_harp,
            'ylda':self.load_applog_ylda
        }

    def load_applog(self, logdir):
        return self.engine[self.name](logdir)

    def load_timelog_harp(self, logfile):
        """
        load elapsed millis of each iteration from logfile
    
        return:
            nparray
        """
        logf = open(logfile,'r')
        elapsed=[]
        for line in logf:
            m = re.search(self.pattern[self.name], line)
            if m:
                elapsed.append( (int(m.group(1)), int(m.group(2))) )
            
        return elapsed

    def load_applog_harp(self, appdir, filename='syslog'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f == filename:
                    elapsed = self.load_timelog_harp(os.path.join(dirpath, f))
                    if len(elapsed) > 0:
                        logger.info('load log from %s at %s', f, dirpath)
                        models.append((dirpath, elapsed))

        # (dirpath, [(compute time, comm time)])
        iternum = len(models[0][1])
        nodenum = len(models)
        models =  sorted(models, key = lambda modeltp : modeltp[0])
        logger.info('total %d iterations, %d nodes', iternum, nodenum)
        
        compute=[]
        comm=[]
        for idx in range(nodenum):
            compute.append([x[0] for x in models[idx][1]])
            comm.append([x[1] for x in models[idx][1]])

        #logger.debug('computeMatrix: %s', compute[:3])

        # id, compute time, comm time
        computeMatrix = np.array(compute)
        commMatrix = np.array(comm)

        #output the matrix
        np.savetxt(appdir + ".computetime", computeMatrix, fmt='%d')
        np.savetxt(appdir + ".commtime", commMatrix, fmt='%d')

        #min, max, mean analysis
        # mean/std of compute, comm restured
        matrix = np.zeros((4, iternum))

        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(computeMatrix, axis=0)
        statMatrix[1] = np.max(computeMatrix, axis=0)
        statMatrix[2] = np.mean(computeMatrix, axis=0)
        statMatrix[3] = np.std(computeMatrix, axis=0)

        matrix[0] = statMatrix[2]
        matrix[1] = statMatrix[3]

        np.savetxt(appdir + '.comput-stat', statMatrix,fmt='%.2f')

        statMatrix[0] = np.min(commMatrix, axis=0)
        statMatrix[1] = np.max(commMatrix, axis=0)
        statMatrix[2] = np.mean(commMatrix, axis=0)
        statMatrix[3] = np.std(commMatrix, axis=0)

        matrix[2] = statMatrix[2]
        matrix[3] = statMatrix[3]

        np.savetxt(appdir + '.comm-stat', statMatrix,fmt='%.2f')

        #logger.info('min = %s', np.min(computeMatrix, axis=0))
        #logger.info('max = %s', np.max(computeMatrix, axis=0))
        #logger.info('mean = %s', np.mean(computeMatrix, axis=0))
        #logger.info('std = %s', np.std(computeMatrix, axis=0))

        return matrix

    def load_timelog_ylda(self, logfile):
        """
        load elapsed millis of each iteration from logfile
    
        return:
            nparray
        """
        logf = open(logfile,'r')
        compute = []
        commu = []
        for line in logf:
            m = re.search(self.pattern[self.name+'-compute'], line)
            if m:
                compute.append( (int(m.group(1)), int(float(m.group(2))*60*1000)) )

            m = re.search(self.pattern[self.name+'-commu'], line)
            if m:
                commu.append( (int(m.group(1)), int(float(m.group(2))*1000)) )

        return compute, commu

    def load_applog_ylda(self, appdir, filename='learntopics.INFO'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f.startswith(filename):
                    compute, commu = self.load_timelog_ylda(os.path.join(dirpath, f))
                    if len(compute) > 0:
                        logger.info('load log from %s at %s', f, dirpath)
                        models.append((dirpath, compute, commu))

        # (dirpath, [(1,compute time),(2,)...], [(1,comm time),(2,)...])
        nodenum = len(models)
        models =  sorted(models, key = lambda modeltp : modeltp[0])
        
        compute=[]
        comm=[]
        iternum = 0
        for idx in range(nodenum):
            t = ([x[1] for x in models[idx][1]])
            if len(t) > iternum:
                iternum = len(t)
            compute.append(t)

            t =[x[1] for x in models[idx][2]]
            if len(t) > iternum:
                iternum = len(t)
            comm.append(t)

        #iternum = len(models[0][1])
        logger.info('total %d iterations, %d nodes', iternum, nodenum)

        logger.debug('computeMatrix: %s', compute[:3])
        logger.debug('commuMatrix: %s', comm[:3])

        #
        # id, compute time, comm time, dtype=object for comm can be different length
        # iternum maybe not the same
        #
        #computeMatrix = np.array(compute)
        #commMatrix = np.array(comm)
        computeMatrix = np.zeros((nodenum, iternum))
        commMatrix = np.zeros((nodenum, iternum))

        for idx in range(nodenum):
            l = len(compute[idx])
            np.copyto(computeMatrix[idx][:l], np.array(compute[idx]))
            l = len(comm[idx])
            np.copyto(commMatrix[idx][:l], np.array(comm[idx]))

        logger.info('computeMatrix shape=%s, commMatrix shape=%s', computeMatrix.shape, commMatrix.shape)

        logger.debug('computeMatrix[0,:]: %s', computeMatrix[0,:])
        logger.debug('commuMatrix[0,:] %s', commMatrix[0,:])

        #output the matrix
        np.savetxt(appdir + ".computetime", computeMatrix, fmt='%d')
        np.savetxt(appdir + ".commtime", commMatrix, fmt='%d')

        #min, max, mean analysis
        # mean/std of compute, comm restured
        matrix = np.zeros((4, iternum))

        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(computeMatrix, axis=0)
        statMatrix[1] = np.max(computeMatrix, axis=0)
        statMatrix[2] = np.mean(computeMatrix, axis=0)
        statMatrix[3] = np.std(computeMatrix, axis=0)

        matrix[0] = statMatrix[2]
        matrix[1] = statMatrix[3]

        np.savetxt(appdir + '.comput-stat', statMatrix,fmt='%.2f')

        statMatrix[0] = np.min(commMatrix, axis=0)
        statMatrix[1] = np.max(commMatrix, axis=0)
        statMatrix[2] = np.mean(commMatrix, axis=0)
        statMatrix[3] = np.std(commMatrix, axis=0)

        matrix[2] = statMatrix[2]
        matrix[3] = statMatrix[3]

        np.savetxt(appdir + '.comm-stat', statMatrix,fmt='%.2f')

        #logger.info('min = %s', np.min(computeMatrix, axis=0))
        #logger.info('max = %s', np.max(computeMatrix, axis=0))
        #logger.info('mean = %s', np.mean(computeMatrix, axis=0))
        #logger.info('std = %s', np.std(computeMatrix, axis=0))

        return matrix



def draw_mvmatrix(mv_matrix, trainer, fig, show = False):
    logger.info('draw the mean-var figure')

    row , col = mv_matrix.shape
    x = np.arange(1, col + 1 )

    plt.title('Performance of LDA Trainers')
    plt.xlabel('Iteration Number')
    plt.ylabel('Elapsed Millis')

    plt.errorbar(x, mv_matrix[0], mv_matrix[1] ,label=trainer + ' compute')
    plt.errorbar(x, mv_matrix[2], mv_matrix[3] ,label=trainer + ' comm')

    plt.legend()

    plt.savefig(fig)
    if show:
        plt.show()

def draw_time(elapsed, trainer, fig, show = False):
    logger.debug('plot the elapsed time fig')

    x = np.arange(1, len(elapsed) + 1 )
    y = np.array(elapsed)
    plt.title('Performance of LDA Trainers')
    plt.xlabel('Iteration Number')
    plt.ylabel('Elapsed Millis')
    #plt.plot(x, y, 'b.-', label=modelname+' likelihood' )
    plt.plot(x, y, 'c.-', label=trainer )
    plt.legend()

    plt.savefig(fig)
    if show:
        plt.show()

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # check the path
    trainer = sys.argv[1]
    logdir = sys.argv[2]
    figname = 'runtime.png'
    if len(sys.argv) > 3:
        figname = sys.argv[3]

    logAnalizer = LDATrainerLog(trainer)

    #draw_time(logAnalizer.load_timelog(logfile), trainer, figname)
    mv_matrix = logAnalizer.load_applog(logdir)

    draw_mvmatrix(mv_matrix, trainer, figname)




