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
        app_start       Log file created at: 2015/10/21 10:27:14
                        Log line format: [IWEF]mmdd hh:mm:ss.uuuuuu threadid file:line] msg
        train_start     W1021 10:37:32.546551 15315 Training_Execution_Strategy.cpp:57] Starting Parallel training Pipeline
        app_end         xxxxxxxxxxxxxxx Model saved
        compute         Iteration 1 done. Took 0.384061 mins
        communicate     Synch pass 1 done. Took 231.369 seconds


    harp   : hadoop user logs, syslog, each node has one directory
        app_start       2015-10-10 19:44:35,269 INFO [main] 
        train_start     initialize Z took
        app_end         Server ends
        compute/comm    Compute time: 88900, comm time: 18103
        iter            Iteration 2 took: 97087
        
    petuum: 
        app_start       I1030 23:35:09.708537 95305 sysparam.hpp:71]  node file  :
        app_init        1030 23:35:27.519075 226328 ll-coordinator.cpp:185] [coordinator] start initialization ...
        train_start     I1030 23:42:20.588816 226328 ll-coordinator.cpp:262] [coordinator] start iteration
        app_end         I1031 01:36:17.615155 34238 ll-worker.cpp:528] [worker 20] terminate job
        compute         compute time: min 37(s), max 52(s)
        iter            I1030 23:44:14.509174 226328 ll-coordinator.cpp:336] iteration0  loglikelihood -2.27239e+11  time 113.29  elapsed time 113.29

    petuum_run : petuum logs

        ### iteration, docll, moll,  docll+moll, time per iter, total elapsed time
        0  -8.768292e+09  -1.122321e+10  -1.999150e+10  28.347012 28.347012 
        

Usage: 
    analy_timelog <trainer> <appdir> <figname>

"""

import sys,os,re
import datetime
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Svg')
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class LDATrainerLog():
    trainers=['mallet','harp','ylda','petuum','petuum-run']
    pattern={
        "mallet":"^([0-9]+)ms",
        "harp-clock":"(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,[0-9]*)",
        "harp-newformat":"Iteration ([0-9]*): ([0-9]*), compute time: ([0-9]*), comm time: ([0-9]*)",
        "harp-numTokens":"numTokens: ([0-9]*), schedule: [0-9]*",
        "harp-compute":"Compute time: ([0-9]*), comm time: ([0-9]*)",
        "harp-iter":"Iteration [0-9]* took: ([0-9]*)",
        "ylda-clock":"[IWEF](\d\d\d\d \d\d:\d\d:\d\d.[0-9]*)",
        "ylda-compute":"Iteration ([0-9]*) done. Took ([0-9\.]*) mins",
        "ylda-commu":"Synch pass ([0-9]*) done. Took ([0-9\.]*) seconds"
    }

    def __init__(self,name):
        if name not in self.trainers:
            raise NameError('no %s trainer support yet, quit.'%name)
        self.name = name
        self.engine={
            'harp':self.load_applog_harp,
            'ylda':self.load_applog_ylda,
            'petuum':self.load_applog_petuum,
            'petuum-run':self.load_applog_petuumrun
        }

    def load_applog(self, logdir):
        return self.engine[self.name](logdir)

    ##############################################################    
    def load_applog_petuumrun(self, appdir, filename='.log'):
        rawdata = None
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f.endswith(filename):
                    rawdata = np.loadtxt(os.path.join(dirpath, f))
                    break

        if rawdata is None:
            logger.error('%s/%s load data failed', dirpath, f)
            return None

        iternum, cols = rawdata.shape

        #min, max, mean analysis
        # mean/std of compute, comm, iter restured
        matrix = np.zeros((6, iternum))

        # compute time, rawdata[:,4]
        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = rawdata[:,4]
        statMatrix[1] = rawdata[:,4]
        statMatrix[2] = rawdata[:,4]
        #statMatrix[3] = np.zeros((1,iternum))

        matrix[0] = statMatrix[2]
        matrix[1] = statMatrix[3]

        np.savetxt(appdir + '.comput-stat', statMatrix,fmt='%.2f')

        # runtime stat
        statMatrix = np.zeros((4, 2 + iternum))
        
        np.copyto(statMatrix[0,2:] , rawdata[:,5])
        statMatrix[0,1] = np.max(rawdata[:,5])
        statMatrix[0,0] = statMatrix[0,1] + 120

        statMatrix[1] = statMatrix[0]
        statMatrix[2] = statMatrix[0]
        np.savetxt(appdir + '.runtime-stat', statMatrix,fmt='%.2f')

        # likelihood
        #maxiternum = iternum - 2
        maxiternum = iternum 
        lhiters = [1]
        lhiters.extend([x for x in range(10, maxiternum+1,10)])
        lhood= [rawdata[0,2]]
        lhood.extend([rawdata[iter-1,2] for iter in range(10,maxiternum+1,10)])
        lhood_row = len(lhood)
        lhMatrix = np.zeros((lhood_row, 3))
        lhMatrix[:,0] = np.array(lhiters)
        lhMatrix[:,1] = np.array(lhood)
        lhMatrix[:,2] = np.array(lhood)

        np.savetxt(appdir + '.likelihood', lhMatrix,fmt='%e')

        return matrix
    
    ##################################################################
    def load_timelog_petuum(self, logfile):
        """
        load elapsed millis of each iteration from logfile
    
        return:
            nparray
        """
        logf = open(logfile,'r')

        # get app starttime, iteration starttime, app endtime
        # appstart: first line
        # trainstart: "Starting Parallel training Pipeline"
        # append:   "Model saved"
        #
        for startline in logf:
            if startline.find('node file  :') > 0:
                break

        if not startline:
            logger.error('start point not found, quit...')
            return None

        string_date = '2015-01-01 ' + startline.split(' ')[1]
        #logger.info('startline= %s', string_date)
        app_starttime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")

        # start init
        for startline in logf:
            if startline.find('start initialization') > 0:
                break

        if not startline:
            logger.error('initialize start point not found, quit...')
            return None

        string_date = '2015-01-01 ' + startline.split(' ')[1]
        #logger.info('startline= %s', string_date)
        init_starttime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")


        # start iteration
        for startline in logf:
            if startline.find('start iteration') > 0:
                break

        if not startline:
            logger.error('iteration start point not found, quit...')
            return None

        string_date = '2015-01-01 ' + startline.split(' ')[1]
        #logger.info('startline= %s', string_date)
        train_starttime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")

        #
        #train_starttime = app_starttime
        #app_endtime = app_starttime

        # computation time and iter time
        itertime = []
        computetime=[]
        for line in logf:

            if line.find("compute time:") > 0:
                m = re.search("min ([0-9]*)\(s\), max ([0-9]*)", line)
                if m:
                    #max_computetime = max(max_computetime, int(m.group(2)))
                    computetime.append(int(m.group(2)))

            if re.search("iteration[0-9]*  loglikelihood",line):
                m = re.search("  time ([0-9\.]*)  elapsed time ([0-9\.]*)", line)
                if m:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    # computetime, iter time, elapse time
                    #min, max, mean, std
                    _compute = np.array(computetime)
                    _min = np.min(_compute)
                    _max = np.max(_compute)
                    _mean = np.mean(_compute)
                    _std = np.std(_compute)

                    itertime.append( (_min, _max, _mean, _std, float(m.group(1)), float(m.group(2))) )
                    #mx_computetime = 0
                    computetime = []

                    string_date = '2015-01-01 ' + line.split(' ')[1]
                    app_endtime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")

            if re.search("I.*terminate job",line):
                string_date = '2015-01-01 ' + line.split(' ')[1]
                #logger.info('startline= %s', string_date)
                app_endtime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f")
                #break

        # end
        logger.info('app_starttime=%s, init_starttime=%s, train_starttime=%s, app_endtime=%s',
                app_starttime, init_starttime, train_starttime, app_endtime)
        app_span = (app_endtime - app_starttime).total_seconds()
        if app_span < 0:
            app_span += 3600*24
        train_span = (app_endtime - train_starttime).total_seconds()
        if train_span < 0:
            train_span += 3600*24

        init_span =  (train_starttime - init_starttime).total_seconds()
        if init_span < 0:
            init_span += 3600*24

        logger.info('runtime total=%d, train=%d, init=%d', app_span, train_span, init_span)

        return app_span, train_span, init_span, itertime


    def load_applog_petuum(self, appdir, filepattern='.info.log'):
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if re.search(filepattern, f):
                    logger.info('load log from %s at %s', f, dirpath)
                    try:
                        # itertime <computetime min, max, mean, std, iter time, elapse time>
                        app_t, train_t, init_t, itertime = self.load_timelog_petuum(os.path.join(dirpath, f))
                    except:
                        logger.error('failed...\n')
                        itertime = []
                    if len(itertime) > 0:
                        #break
                        output_name = f[:f.find(filepattern)]

                        # (dirpath, [(compute time, comm time)])
                        # petuum use (s), harp use (ms)
                        iternum = len(itertime)
                        logger.info('total %d iterations', iternum)
                        # compute time, rawdata[:,4]
                        statMatrix = np.zeros((4, iternum))
                        statMatrix[0] = np.array([x[0]*1000 for x in itertime])
                        statMatrix[1] = np.array([x[1]*1000 for x in itertime])
                        statMatrix[2] = np.array([x[2]*1000 for x in itertime])
                        statMatrix[3] = np.array([x[3]*1000 for x in itertime])

                        np.savetxt(output_name + '.comput-stat', statMatrix,fmt='%.2f')

                        # itertime
                        statMatrix = np.zeros((4, iternum))
                        iterArray = np.array([x[4]*1000 for x in itertime])

                        statMatrix[0] = iterArray
                        statMatrix[1] = iterArray
                        statMatrix[2] = iterArray

                        np.savetxt(output_name + '.iter-stat', statMatrix,fmt='%.2f')

                        # runtime stat
                        statMatrix = np.zeros((4, 2 + iternum))
                        runtimeArray =  np.array([x[5] for x in itertime])

                        np.copyto(statMatrix[0,2:] , runtimeArray)
                        statMatrix[0,1] = train_t
                        #statMatrix[0,0] = app_t
                        statMatrix[0,0] = train_t + init_t

                        statMatrix[1] = statMatrix[0]
                        statMatrix[2] = statMatrix[0]
                        np.savetxt(output_name + '.runtime-stat', statMatrix,fmt='%.2f')

        return None

    #######################################################################
    def load_timelog_harp(self, logfile):
        """
        load elapsed millis of each iteration from logfile
    
        return:
            nparray
        """
        logf = open(logfile,'r')

        # get app starttime, iteration starttime, app endtime
        # appstart: first line
        # trainstart: "Starting Parallel training Pipeline"
        # append:   "Model saved"
        #
        startline = logf.readline().strip()
        string_date = startline[:len("2015-10-10 19:52:05,199")]
        #logger.info('startline= %s', string_date)
        app_starttime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S,%f")
        train_starttime = app_starttime
        app_endtime = app_starttime

        for line in logf:
            if line.find("nitialize Z took") > 0 or line.find('nit Z took') > 0:
                m = re.search(self.pattern[self.name+'-clock'], line)
                if m:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = m.group(1)
                    train_starttime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S,%f")

            if line.find("Server ends") > 0:
                m = re.search(self.pattern[self.name+'-clock'], line)
                if m:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = m.group(1)
                    app_endtime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S,%f")
        
        #
        # there is summer time, app_endtime < app_starttime
        #
        if app_endtime < app_starttime:
            app_span = (app_endtime - app_starttime).total_seconds() +  3600
            train_span = (app_endtime - train_starttime).total_seconds() + 3600
        else:
            app_span = (app_endtime - app_starttime).total_seconds()
            train_span = (app_endtime - train_starttime).total_seconds()
        logger.info('runtime total=%d, train=%d', app_span, train_span)


        #
        # get time for each iterations
        #
        # elapsed: <compute time, commu time>
        # itertime: <accumulate clocktime, one iteration time>
        #       accumulate offset to the train_starttime
        # 
        logf.seek(0,0)

        elapsed=[]
        itertime=[]
        tokencnt=[]
        last_iterspan = 0
        for line in logf:
            #new format first
            m = re.search(self.pattern[self.name+'-newformat'], line)
            if m:
                elapsed.append( (int(m.group(3)), int(m.group(4))) )

                mx = re.search(self.pattern[self.name+'-clock'], line)
                if mx:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = mx.group(1)
                    iter_starttime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S,%f")

                iter_span = (iter_starttime - train_starttime).total_seconds()

                itertime.append( (int(m.group(2)),iter_span) )
                
                # check the numToken
                mx = re.search(self.pattern[self.name+'-numTokens'], line)
                if mx:
                    tokencnt.append(int(m.group(1)))

                continue

            # old format
            m = re.search(self.pattern[self.name+'-compute'], line)
            if m:
                elapsed.append( (int(m.group(1)), int(m.group(2))) )

            m = re.search(self.pattern[self.name+'-iter'], line)
            if m:
                # ok, let's get clock time
                mx = re.search(self.pattern[self.name+'-clock'], line)
                if mx:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = mx.group(1)
                    iter_starttime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S,%f")

                iter_span = (iter_starttime - train_starttime).total_seconds()
                if iter_span < last_iterspan:
                    iter_span += 3600
                last_iterspan = iter_span

                itertime.append( (int(m.group(1)),iter_span) )

        return elapsed, app_span, train_span, itertime, tokencnt

    def load_applog_harp(self, appdir, filename='syslog'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f == filename:
                    elapsed, app_t, train_t, itertime, tokencnt = self.load_timelog_harp(os.path.join(dirpath, f))
                    if len(elapsed) > 0:
                        logger.info('load log from %s at %s', f, dirpath)
                        models.append((dirpath, elapsed, app_t, train_t, itertime, tokencnt))

        # (dirpath, [(compute time, comm time)])
        iternum = len(models[0][1])
        nodenum = len(models)
        models =  sorted(models, key = lambda modeltp : modeltp[0])
        logger.info('total %d iterations, %d nodes', iternum, nodenum)
        
        compute=[]
        comm=[]
        itertime=[]
        iter_t = []
        app_t = []
        train_t = []
 
        for idx in range(nodenum):
            compute.append([x[0] for x in models[idx][1]])
            comm.append([x[1] for x in models[idx][1]])
            app_t.append(models[idx][2])
            train_t.append(models[idx][3])
            itertime.append([x[0] for x in models[idx][4]])
            iter_t.append([x[1] for x in models[idx][4]])

        #logger.debug('computeMatrix: %s', compute[:3])

        # id, compute time, comm time
        computeMatrix = np.array(compute)
        commMatrix = np.array(comm)
        iterMatrix = np.array(itertime)

        # run time: col1:app_time, col2:train_time
        runtimeMatrix = np.zeros((2,nodenum))
        runtimeMatrix[0] = np.array(app_t)
        runtimeMatrix[1] = np.array(train_t)
        runtimeMatrix = np.transpose(runtimeMatrix)

        # add iter_t matrix, (nodenum, iternum)
        iter_tMatrix = np.array(iter_t)
        logger.info('iter shape=%s, runtime shape=%s', iter_tMatrix.shape, runtimeMatrix.shape)
        runtimeMatrix = np.concatenate((runtimeMatrix, iter_tMatrix), axis=1)

        #output the matrix
        np.savetxt(appdir + ".computetime", computeMatrix, fmt='%d')
        np.savetxt(appdir + ".commtime", commMatrix, fmt='%d')
        np.savetxt(appdir + ".runtime", runtimeMatrix, fmt='%d')
        np.savetxt(appdir + ".itertime", iterMatrix, fmt='%d')

        #min, max, mean analysis
        # mean/std of compute, comm, iter restured
        matrix = np.zeros((6, iternum))

        # compute time
        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(computeMatrix, axis=0)
        statMatrix[1] = np.max(computeMatrix, axis=0)
        statMatrix[2] = np.mean(computeMatrix, axis=0)
        statMatrix[3] = np.std(computeMatrix, axis=0)

        matrix[0] = statMatrix[2]
        matrix[1] = statMatrix[3]

        np.savetxt(appdir + '.comput-stat', statMatrix,fmt='%.2f')

        # comm time
        statMatrix[0] = np.min(commMatrix, axis=0)
        statMatrix[1] = np.max(commMatrix, axis=0)
        statMatrix[2] = np.mean(commMatrix, axis=0)
        statMatrix[3] = np.std(commMatrix, axis=0)

        matrix[2] = statMatrix[2]
        matrix[3] = statMatrix[3]

        np.savetxt(appdir + '.comm-stat', statMatrix,fmt='%.2f')

        # itertime
        statMatrix[0] = np.min(iterMatrix, axis=0)
        statMatrix[1] = np.max(iterMatrix, axis=0)
        statMatrix[2] = np.mean(iterMatrix, axis=0)
        statMatrix[3] = np.std(iterMatrix, axis=0)

        matrix[4] = statMatrix[2]
        matrix[5] = statMatrix[3]

        np.savetxt(appdir + '.iter-stat', statMatrix,fmt='%.2f')

        # runtime stat
        statMatrix = np.zeros((4, 2 + iternum))
        statMatrix[0] = np.min(runtimeMatrix, axis=0)
        statMatrix[1] = np.max(runtimeMatrix, axis=0)
        statMatrix[2] = np.mean(runtimeMatrix, axis=0)
        statMatrix[3] = np.std(runtimeMatrix, axis=0)

        np.savetxt(appdir + '.runtime-stat', statMatrix,fmt='%.2f')

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

        # get app starttime, iteration starttime, app endtime
        # appstart: first line
        # trainstart: "Starting Parallel training Pipeline"
        # append:   "Model saved"
        #
        startline = logf.readline().strip()
        string_date = startline[len("Log file created at: "):]
        #logger.info('startline= %s', string_date)
        app_starttime = datetime.datetime.strptime(string_date, "%Y/%m/%d %H:%M:%S")
        train_starttime = app_starttime
        app_endtime = app_starttime

        for line in logf:
            if line.find("Starting Parallel training Pipeline") > 0:
                m = re.search("[IWEF](\d\d\d\d \d\d:\d\d:\d\d.[0-9]*)", line)
                if m:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = '2015' + m.group(1)
                    train_starttime = datetime.datetime.strptime(string_date, "%Y%m%d %H:%M:%S.%f")

            if line.find("Model saved") > 0:
                m = re.search("[IWEF](\d\d\d\d \d\d:\d\d:\d\d.[0-9]*)", line)
                if m:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = '2015' + m.group(1)
                    app_endtime = datetime.datetime.strptime(string_date, "%Y%m%d %H:%M:%S.%f")
        
        app_span = (app_endtime - app_starttime).total_seconds()
        train_span = (app_endtime - train_starttime).total_seconds()
        logger.info('runtime total=%d, train=%d', app_span, train_span)

        #
        # get time for each iterations
        #
        # compute time
        # commu time
        # itertime: <accumulate clocktime, one iteration time>
        #       accumulate offset to the train_starttime
        # 
 
        logf.seek(0,0)
        compute = []
        commu = []
        itertime = []
        for line in logf:
            # compute
            m = re.search(self.pattern[self.name+'-compute'], line)
            if m:
                compute.append( (int(m.group(1)), int(float(m.group(2))*60*1000)) )
                # here , let's get the clock time
                mx = re.search("[IWEF](\d\d\d\d \d\d:\d\d:\d\d.[0-9]*)", line)
                if mx:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = '2015' + mx.group(1)
                    iter_starttime = datetime.datetime.strptime(string_date, "%Y%m%d %H:%M:%S.%f")

                iter_span = (iter_starttime - train_starttime).total_seconds()
                itertime.append( iter_span )
            
            # commu
            m = re.search(self.pattern[self.name+'-commu'], line)
            if m:
                commu.append( (int(m.group(1)), int(float(m.group(2))*1000)) )

        return compute, commu, app_span, train_span, itertime

    def load_applog_ylda(self, appdir, filename='learntopics.INFO'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f.startswith(filename):
                    compute, commu, app_t, train_t, iter_t = self.load_timelog_ylda(os.path.join(dirpath, f))
                    if len(compute) > 0:
                        logger.info('load log from %s at %s', f, dirpath)
                        models.append((dirpath, compute, commu, app_t, train_t, iter_t))

        # (dirpath, [(1,compute time),(2,)...], [(1,comm time),(2,)...])
        nodenum = len(models)
        models =  sorted(models, key = lambda modeltp : modeltp[0])
        
        compute=[]
        comm=[]
        app_t = []
        train_t = []
        iter_t = []
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

            app_t.append(models[idx][3])
            train_t.append(models[idx][4])
            iter_t.append(models[idx][5])

        #iternum = len(models[0][1])
        logger.info('total %d iterations, %d nodes', iternum, nodenum)

        #logger.debug('computeMatrix: %s', compute[:3])
        #logger.debug('commuMatrix: %s', comm[:3])

        #
        # id, compute time, comm time, dtype=object for comm can be different length
        # iternum maybe not the same
        #
        #computeMatrix = np.array(compute)
        #commMatrix = np.array(comm)
        computeMatrix = np.zeros((nodenum, iternum))
        commMatrix = np.zeros((nodenum, iternum))
        #iterMatrix = np.zeros((nodenum, iternum))
        
        for idx in range(nodenum):
            l = len(compute[idx])
            np.copyto(computeMatrix[idx][:l], np.array(compute[idx]))
            l = len(comm[idx])
            np.copyto(commMatrix[idx][:l], np.array(comm[idx]))
            # 

        logger.info('computeMatrix shape=%s, commMatrix shape=%s', computeMatrix.shape, commMatrix.shape)

        logger.debug('computeMatrix[0,:]: %s', computeMatrix[0,:])
        logger.debug('commuMatrix[0,:] %s', commMatrix[0,:])
        
        # run time: col1:app_time, col2:train_time
        runtimeMatrix = np.zeros((2,nodenum))
        runtimeMatrix[0] = np.array(app_t)
        runtimeMatrix[1] = np.array(train_t)
        # they maybe different length
        #np.copyto(runtimeMatrix[0] ,np.array(app_t))
        #np.copyto(runtimeMatrix[1] ,np.array(train_t))
    
        runtimeMatrix = np.transpose(runtimeMatrix)

        # add iter_t matrix, (nodenum, iternum)
        #iter_tMatrix = np.array(iter_t)
        #iter_tMatrix = np.zeros((nodenum, iternum))
        #np.copyto(iter_tMatrix , np.array(iter_t))
        iter_tMatrix = np.array(iter_t)
        runtimeMatrix = np.concatenate((runtimeMatrix, iter_tMatrix), axis=1)

        #output the matrix
        np.savetxt(appdir + ".computetime", computeMatrix, fmt='%d')
        np.savetxt(appdir + ".commtime", commMatrix, fmt='%d')
        np.savetxt(appdir + ".runtime", runtimeMatrix, fmt='%d')

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

        # runtime stat
        K,V = runtimeMatrix.shape
        statMatrix = np.zeros((4, V))
        statMatrix[0] = np.min(runtimeMatrix, axis=0)
        statMatrix[1] = np.max(runtimeMatrix, axis=0)
        statMatrix[2] = np.mean(runtimeMatrix, axis=0)
        statMatrix[3] = np.std(runtimeMatrix, axis=0)
        #np.copyTo(statMatrix[0] , np.min(runtimeMatrix, axis=0))
        #np.copyTo(statMatrix[1] , np.max(runtimeMatrix, axis=0))
        #np.copyTo(statMatrix[2] , np.mean(runtimeMatrix, axis=0))
        #np.copyTo(statMatrix[3] , np.std(runtimeMatrix, axis=0))


        np.savetxt(appdir + '.runtime-stat', statMatrix,fmt='%.2f')

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

    #draw_mvmatrix(mv_matrix, trainer, logdir+'.png')




