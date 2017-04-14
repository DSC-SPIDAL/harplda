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
        newformat:      Iteration 1: 161738, compute time: 67431, comm time: 212347, misc: 75982, numTokens: 101884477, percentage(): 10
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
        

    petuum-new:
         753 [coordinator] Log Likelihood: doc -8.772923e+09 + word : -1.122329e+10 = -1.999622e+10
         @@@ iteration: 0  loglikelihood -1.999622e+10   per iter: 145.277585 (146.898611)(151.962421) elapsed 145.277585(146.898611)(151.962421)sendbytes(17773.148438 KB) recbytes (1872402.289062 KB)        I0316 23:39:49.720991 148882 ll-coordinator.cpp:336] iteration0  loglikelihood -1.99962e+10  time 151.962  elapsed time 151.962


    nomadlda:
        :iter 12 time 10 totaltime 120.1 time-1 10.64 time-2 0.5058 eplasetime 136.2 training-LL -1.20181e+09 Nwt 856822054 avg 5.74928 Nt 19970 nxt 1x16, throughput 4.171974e+05

    lightlda:
        [INFO] [2017-03-28 21:03:13] Rank = 0, Training Time used: 10.59 s
        [INFO] [2017-04-11 19:08:03] doc likelihood : -7.185419e+09
        [INFO] [2017-04-11 19:08:04] word likelihood : 3.489482e+09
        [INFO] [2017-04-11 19:08:04] log_likelihood : -2.262308e+10
        [INFO] [2017-03-28 21:03:17] word_log_likelihood : -1.554106e+09

    warplda:
        Iteration 199, 2.744135 s, 1697154.799260 tokens/thread/sec, 32 threads, log_likelihood (per token) -9.064325, total -1.350866e+09, word_likelihood -6.696219e+08

    
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
    trainers=['mallet','harp','ylda','warplda','lightlda','nomadlda','petuum','petuum-run','petuum-new']
    pattern={
        "mallet":"^([0-9]+)ms",
        "harp-clock":"(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,[0-9]*)",
        "harp-newformat":"Iteration ([0-9]*): ([0-9]*), compute time: ([0-9]*), comm time: ([0-9]*)",
        "harp-newformat2":"Iteration ([0-9]*): ([0-9]*), compute time: ([0-9]*), misc: ([0-9]*)",
        #"harp-numTokens":"numTokens: ([0-9]*), schedule: [0-9]*",
        "harp-numTokens":"numTokens: ([0-9]*), percentage",
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
            'nomadlda':self.load_applog_nomadlda,
            'lightlda':self.load_applog_lightlda,
            'warplda':self.load_applog_warplda,
            'petuum':self.load_applog_petuum,
            'petuum-new':self.load_applog_petuum_new,
            'petuum-run':self.load_applog_petuumrun
        }

    def load_applog(self, logdir):
        return self.engine[self.name](logdir)

    ##############################################################    
    def load_applog_petuumrun(self, appdir, filename='learntopics.*\.log'):
        rawdata = None
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                #if f.endswith(filename):
                if re.search(filename,f):
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
        itertimeFull = []
        computetime=[]
        
        for line in logf:

            if line.find("compute time:") > 0:
                m = re.search("\[worker ([0-9]*)\].* min ([0-9]*)\(s\), max ([0-9]*)", line)
                if m:
                    #max_computetime = max(max_computetime, int(m.group(2)))
                    #computetime.append(int(m.group(2)))
                    computetime.append([int(m.group(1)), int(m.group(3))])

            if re.search("iteration[0-9]*  loglikelihood",line):
                m = re.search("  time ([0-9\.]*)  elapsed time ([0-9\.]*)", line)
                if m:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    # computetime, iter time, elapse time
                    #min, max, mean, std
                    #_compute = np.array(computetime)
                    _compute = np.array([x[1] for x in computetime])

                    _min = np.min(_compute)
                    _max = np.max(_compute)
                    _mean = np.mean(_compute)
                    _std = np.std(_compute)

                    itertime.append( (_min, _max, _mean, _std, float(m.group(1)), float(m.group(2))) )

                    #save raw computetime data
                    _sort_compute = sorted(computetime, key = lambda x:x[0])
                    itertimeFull.append([x[1] for x in _sort_compute])
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

        return app_span, train_span, init_span, itertime, itertimeFull


    def load_applog_petuum(self, appdir, filepattern='.info.log'):
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if re.search(filepattern, f):
                    logger.info('load log from %s at %s', f, dirpath)
                    try:
                        # itertime <computetime min, max, mean, std, iter time, elapse time>
                        app_t, train_t, init_t, itertime, itertimeFull = self.load_timelog_petuum(os.path.join(dirpath, f))
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

                        iterMatrix = np.transpose(np.array(itertimeFull)) * 1000
                        np.savetxt(output_name + '.computetime', iterMatrix,fmt='%.2f')

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

    ###################################################################
    # new petuum, train time only, wordlike ll only, 
    ###################################################################
    def load_timelog_petuum_new(self, logfile):
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
        itertimeFull = []
        computetime=[]
        wordll=[]
        traintime=[]
        
        for line in logf:

            if line.find("compute time:") > 0:
                m = re.search("\[worker ([0-9]*)\].* min ([0-9]*)\(s\), max ([0-9]*)", line)
                if m:
                    #max_computetime = max(max_computetime, int(m.group(2)))
                    #computetime.append(int(m.group(2)))
                    computetime.append([int(m.group(1)), int(m.group(3))])

            #if line.find("\[coordinator\] Log Likelihood: doc") > 0:
            if line.find("Log Likelihood: doc") > 0:
                logger.info('*')
                m = re.search("word : ([-+]\d+\.\d+e\+\d+)", line)
                if m:
                    #max_computetime = max(max_computetime, int(m.group(2)))
                    #computetime.append(int(m.group(2)))
                    wordll.append([float(m.group(1))])

            #if line.find("@@@ iteration: \d+  loglikelihood ") > 0:
            if re.search("@@@ iteration: \d+  loglikelihood ", line):
                logger.info('=')
                m = re.search("per iter: (\d+\.\d+) \(", line)
                if m:
                    #max_computetime = max(max_computetime, int(m.group(2)))
                    #computetime.append(int(m.group(2)))
                    traintime.append([float(m.group(1))])

            if re.search("iteration[0-9]*  loglikelihood",line):
                m = re.search("  time ([0-9\.]*)  elapsed time ([0-9\.]*)", line)
                if m:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    # computetime, iter time, elapse time
                    #min, max, mean, std
                    #_compute = np.array(computetime)
                    _compute = np.array([x[1] for x in computetime])

                    _min = np.min(_compute)
                    _max = np.max(_compute)
                    _mean = np.mean(_compute)
                    _std = np.std(_compute)

                    itertime.append( (_min, _max, _mean, _std, float(m.group(1)), float(m.group(2))) )

                    #save raw computetime data
                    _sort_compute = sorted(computetime, key = lambda x:x[0])
                    itertimeFull.append([x[1] for x in _sort_compute])
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

        return app_span, train_span, init_span, itertime, itertimeFull, wordll, traintime

    def load_applog_petuum_new(self, appdir, filepattern='.info.log'):
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if re.search(filepattern, f):
                    logger.info('load log from %s at %s', f, dirpath)
                    try:
                        # itertime <computetime min, max, mean, std, iter time, elapse time>
                        app_t, train_t, init_t, itertime, itertimeFull, wordll, traintime = self.load_timelog_petuum_new(os.path.join(dirpath, f))
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
                        logger.info('wordll : %s', wordll)
                        logger.info('taintime shape: %s', traintime)
                        # compute time, rawdata[:,4]
                        statMatrix = np.zeros((4, iternum))
                        statMatrix[0] = np.array([x[0]*1000 for x in itertime])
                        statMatrix[1] = np.array([x[1]*1000 for x in itertime])
                        statMatrix[2] = np.array([x[2]*1000 for x in itertime])
                        statMatrix[3] = np.array([x[3]*1000 for x in itertime])

                        np.savetxt(output_name + '.comput-stat', statMatrix,fmt='%.2f')

                        iterMatrix = np.transpose(np.array(itertimeFull)) * 1000
                        np.savetxt(output_name + '.computetime', iterMatrix,fmt='%.2f')

                        # itertime
                        statMatrix = np.zeros((4, iternum))
                        #iterArray = np.array([x[4]*1000 for x in itertime])
                        iterArray = np.array([x[0]*1000 for x in traintime])

                        statMatrix[0] = iterArray
                        statMatrix[1] = iterArray
                        statMatrix[2] = iterArray

                        np.savetxt(output_name + '.iter-stat', statMatrix,fmt='%.2f')

                        # runtime stat

                        statMatrix = np.zeros((4, 2 + iternum))
                        #runtimeArray =  np.array([x[5] for x in itertime])
                        traintime=np.array([[x[0] for x in traintime]])
                        runtimeArray =  np.cumsum(traintime)

                        np.copyto(statMatrix[0,2:] , runtimeArray)
                        statMatrix[0,1] = train_t
                        #statMatrix[0,0] = app_t
                        statMatrix[0,0] = train_t + init_t

                        statMatrix[1] = statMatrix[0]
                        statMatrix[2] = statMatrix[0]
                        np.savetxt(output_name + '.runtime-stat', statMatrix,fmt='%.2f')


                        #word likelihood
                        likelihood=[[id,wordll[id][0]] for id in range(len(wordll))]
                        logger.info('likelihood:%s', likelihood)
                        self.save_likelihood(likelihood, output_name + '.likelihood')

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

        totalNumTokens = 0
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
                    #add Total num of tokens check

            if totalNumTokens == 0:
                m = re.search('Total number of tokens ([0-9]*)', line)
                if m:
                    totalNumTokens = int(m.group(1))

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
            #m = re.search(self.pattern[self.name+'-newformat'], line)
            m = re.search(self.pattern[self.name+'-newformat2'], line)
            if m:
                elapsed.append( (int(m.group(3)), int(m.group(4))) )

                mx = re.search(self.pattern[self.name+'-clock'], line)
                if mx:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = mx.group(1)
                    iter_starttime = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S,%f")

                iter_span = (iter_starttime - train_starttime).total_seconds()

                #
                # itertime< traintime from app,  traintime from wall clock>
                #
                itertime.append( (int(m.group(2)),iter_span) )
                
                # check the numToken
                mx = re.search(self.pattern[self.name+'-numTokens'], line)
                if mx:
                    # iternum, numTokens
                    tokencnt.append((int(m.group(1)), int(mx.group(1))) )

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

        return elapsed, app_span, train_span, itertime, tokencnt, totalNumTokens

    def load_applog_harp(self, appdir, filename='syslog'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f == filename:
                    elapsed, app_t, train_t, itertime, tokencnt, totalNumTokens = self.load_timelog_harp(os.path.join(dirpath, f))
                    if len(elapsed) > 0:
                        logger.info('load log from %s at %s', f, dirpath)
                        models.append((dirpath, elapsed, app_t, train_t, itertime, tokencnt, totalNumTokens))

        nodenum = len(models)
        models =  sorted(models, key = lambda modeltp : modeltp[0])

        #iternum = len(models[0][1])
        # find the largest iter number
        iternum = 0
        for idx in range(nodenum):
            if len(models[idx][1]) > iternum:
                iternum =  len(models[idx][1]) 
        # there should all be the same
        logger.info('total %d iterations, %d nodes, shape=%s', iternum, nodenum, models[0])

        totalNumTokens = models[0][6]

        logger.info('total %d iterations, %d nodes, totalNumTokens=%d', iternum, nodenum, totalNumTokens)
        
        compute=[]
        comm=[]
        itertime=[]
        iter_t = []
        app_t = []
        train_t = []
        update=[]

        for idx in range(nodenum):
           compute.append([x[0] for x in models[idx][1]])
           comm.append([x[1] for x in models[idx][1]])
           app_t.append(models[idx][2])
           train_t.append(models[idx][3])
           itertime.append([x[0] for x in models[idx][4]])
           iter_t.append([x[1] for x in models[idx][4]])
           update.append([x[1] for x in models[idx][5]])


        if False:
            # old style, iternum are the same for all the nodes
            # id, compute time, comm time
            computeMatrix = np.array(compute)
            commMatrix = np.array(comm)
            iterMatrix = np.array(itertime)
            updateMatrix = np.array(update)
            iter_tMatrix = np.array(iter_t)
        else:
            # new style, iternum are NOT the same for all the nodes, analysis in the middle
            # code from _ylda
            computeMatrix = np.zeros((nodenum, iternum))
            commMatrix = np.zeros((nodenum, iternum))
            iterMatrix = np.zeros((nodenum, iternum))
            updateMatrix = np.zeros((nodenum, iternum))
            iter_tMatrix = np.zeros((nodenum, iternum))
            for idx in range(nodenum):
                l = len(compute[idx])
                np.copyto(computeMatrix[idx][:l], np.array(compute[idx]))
                l = len(comm[idx])
                np.copyto(commMatrix[idx][:l], np.array(comm[idx]))
                l = len(itertime[idx])
                np.copyto(iterMatrix[idx][:l], np.array(itertime[idx]))
                l = len(iter_t[idx])
                np.copyto(iter_tMatrix[idx][:l], np.array(iter_t[idx]))
                l = len(update[idx])
                np.copyto(updateMatrix[idx][:l], np.array(update[idx]))

        # run time: col1:app_time, col2:train_time
        runtimeMatrix = np.zeros((2,nodenum))
        runtimeMatrix[0] = np.array(app_t)
        runtimeMatrix[1] = np.array(train_t)
        runtimeMatrix = np.transpose(runtimeMatrix)

        # add iter_t matrix, (nodenum, iternum)
        logger.info('iter shape=%s, runtime shape=%s', iter_tMatrix.shape, runtimeMatrix.shape)
        runtimeMatrix = np.concatenate((runtimeMatrix, iter_tMatrix), axis=1)

        #output the matrix
        np.savetxt(appdir + ".computetime", computeMatrix, fmt='%d')
        np.savetxt(appdir + ".commtime", commMatrix, fmt='%d')
        np.savetxt(appdir + ".runtime", runtimeMatrix, fmt='%d')
        np.savetxt(appdir + ".itertime", iterMatrix, fmt='%d')
        np.savetxt(appdir + ".update", updateMatrix, fmt='%d')

        #min, max, mean analysis
        # mean/std of compute, comm, iter restured

        # compute time
        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(computeMatrix, axis=0)
        statMatrix[1] = np.max(computeMatrix, axis=0)
        statMatrix[2] = np.mean(computeMatrix, axis=0)
        statMatrix[3] = np.std(computeMatrix, axis=0)
        np.savetxt(appdir + '.comput-stat', statMatrix,fmt='%.2f')

        # comm time
        statMatrix[0] = np.min(commMatrix, axis=0)
        statMatrix[1] = np.max(commMatrix, axis=0)
        statMatrix[2] = np.mean(commMatrix, axis=0)
        statMatrix[3] = np.std(commMatrix, axis=0)
        np.savetxt(appdir + '.comm-stat', statMatrix,fmt='%.2f')

        # itertime
        statMatrix[0] = np.min(iterMatrix, axis=0)
        statMatrix[1] = np.max(iterMatrix, axis=0)
        statMatrix[2] = np.mean(iterMatrix, axis=0)
        statMatrix[3] = np.std(iterMatrix, axis=0)
        np.savetxt(appdir + '.iter-stat', statMatrix,fmt='%.2f')

        # runtime stat
        statMatrix = np.zeros((4, 2 + iternum))
        statMatrix[0] = np.min(runtimeMatrix, axis=0)
        statMatrix[1] = np.max(runtimeMatrix, axis=0)
        statMatrix[2] = np.mean(runtimeMatrix, axis=0)
        statMatrix[3] = np.std(runtimeMatrix, axis=0)
        np.savetxt(appdir + '.runtime-stat', statMatrix,fmt='%.2f')

        # update stat, add sum at row[4], ratio of iteration
        statMatrix = np.zeros((6, iternum))
        statMatrix[0] = np.min(updateMatrix, axis=0)
        statMatrix[1] = np.max(updateMatrix, axis=0)
        statMatrix[2] = np.mean(updateMatrix, axis=0)
        statMatrix[3] = np.std(updateMatrix, axis=0)
        statMatrix[4] = np.cumsum(np.sum(updateMatrix, axis=0))
        statMatrix[5] = statMatrix[4] / totalNumTokens
        np.savetxt(appdir + '.update-stat', statMatrix,fmt='%.2f')


        #logger.info('min = %s', np.min(computeMatrix, axis=0))
        #logger.info('max = %s', np.max(computeMatrix, axis=0))
        #logger.info('mean = %s', np.mean(computeMatrix, axis=0))
        #logger.info('std = %s', np.std(computeMatrix, axis=0))

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
                    string_date = '2016' + m.group(1)
                    train_starttime = datetime.datetime.strptime(string_date, "%Y%m%d %H:%M:%S.%f")

            elif line.find("Model saved") > 0:
                m = re.search("[IWEF](\d\d\d\d \d\d:\d\d:\d\d.[0-9]*)", line)
                if m:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = '2016' + m.group(1)
                    app_endtime = datetime.datetime.strptime(string_date, "%Y%m%d %H:%M:%S.%f")
            
            #save the last timestamp in the case of abnormal quit of program, endtime not exist
            else:
                mx = re.search("[IWEF](\d\d\d\d \d\d:\d\d:\d\d.[0-9]*)", line)
                if mx:
                    #logger.info('match at %s , string_date=%s', line, m.group(1))
                    string_date = '2016' + mx.group(1)
                    logtime = datetime.datetime.strptime(string_date, "%Y%m%d %H:%M:%S.%f")

        if app_endtime == app_starttime:
            app_endtime = logtime

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
                    string_date = '2016' + mx.group(1)
                    iter_starttime = datetime.datetime.strptime(string_date, "%Y%m%d %H:%M:%S.%f")

                iter_span = (iter_starttime - train_starttime).total_seconds()
                itertime.append( iter_span)
            
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
        iterMatrix = np.zeros((nodenum, iternum))
        
        for idx in range(nodenum):
            l = len(compute[idx])
            np.copyto(computeMatrix[idx][:l], np.array(compute[idx]))
            l = len(comm[idx])
            np.copyto(commMatrix[idx][:l], np.array(comm[idx]))
            # 
            l = len(iter_t[idx])
            np.copyto(iterMatrix[idx][:l], np.array(iter_t[idx]))

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
        #iter_tMatrix = np.array(iter_t)
        logger.debug('iter_tMatrix shape=%s,runtimeMatrix.shape=%s', iterMatrix.shape, runtimeMatrix.shape)
        logger.debug('iter_Matrix = %s', iterMatrix)
        #runtimeMatrix = np.concatenate((runtimeMatrix, iter_tMatrix), axis=1)
        runtimeMatrix = np.concatenate((runtimeMatrix, iterMatrix), axis=1)

        #output the matrix
        np.savetxt(appdir + ".computetime", computeMatrix, fmt='%d')
        np.savetxt(appdir + ".commtime", commMatrix, fmt='%d')
        np.savetxt(appdir + ".runtime", runtimeMatrix, fmt='%d')
        
        #for ylda, itermatrix is a accu sum of iter time
        np.copyto(iterMatrix[:,1:], np.diff(iterMatrix, axis=1)) 
        iterMatrix = iterMatrix * 1000
        np.savetxt(appdir + ".itertime", iterMatrix, fmt='%d')

        #min, max, mean analysis
        # mean/std of compute, comm restured
        statMatrix = np.zeros((4, iternum))
        statMatrix[0] = np.min(computeMatrix, axis=0)
        statMatrix[1] = np.max(computeMatrix, axis=0)
        statMatrix[2] = np.mean(computeMatrix, axis=0)
        statMatrix[3] = np.std(computeMatrix, axis=0)
        np.savetxt(appdir + '.comput-stat', statMatrix,fmt='%.2f')

        statMatrix[0] = np.min(commMatrix, axis=0)
        statMatrix[1] = np.max(commMatrix, axis=0)
        statMatrix[2] = np.mean(commMatrix, axis=0)
        statMatrix[3] = np.std(commMatrix, axis=0)
        np.savetxt(appdir + '.comm-stat', statMatrix,fmt='%.2f')

        # itertime
        statMatrix[0] = np.min(iterMatrix, axis=0)
        statMatrix[1] = np.max(iterMatrix, axis=0)
        statMatrix[2] = np.mean(iterMatrix, axis=0)
        statMatrix[3] = np.std(iterMatrix, axis=0)
        #np.savetxt(appdir + '.iter-stat', statMatrix*1000,fmt='%.2f')
        np.savetxt(appdir + '.iter-stat', statMatrix,fmt='%.2f')
 
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

    #
    # warplda
    #
    def load_timelog_warplda(self, logfile):
        logf = open(logfile,'r')

        totalNumTokens = 0
        app_span = 0
        train_span = 0
        elapsed=[]
        itertime=[]
        tokencnt=[]
        likelihood=[]
        last_iterspan = 0
        warplda_format="Iteration ([0-9]*), (\d+\.\d+]*) s,.* word_likelihood ([-+]?\d*\.\d+e\+\d+]*)"
        for line in logf:
            #new format first
            #m = re.search(self.pattern[self.name+'-newformat'], line)
            m = re.search(warplda_format, line)
            if m:
                #
                # itertime< traintime from app,  traintime from wall clock>
                #
                itertime.append(( float(m.group(2))*1000, 0) )
                likelihood.append(( int(m.group(1)), float(m.group(3))))
                continue
        return itertime, likelihood


    def save_likelihood(self,likelihood, fname):
        with open(fname, 'w') as outf:
            for lineid in range(len(likelihood)):
                iterid = lineid + 1
                if (iterid == 1) or (iterid %10 == 0):
                    outf.write("%d %e\n"%(iterid, likelihood[lineid][1]))

    def load_applog_warplda(self, appdir, filepattern='.log'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f.startswith('warplda') and f.endswith(filepattern):
                    itertime, likelihood = self.load_timelog_warplda(os.path.join(dirpath, f))
                    if len(itertime) > 0:
                        logger.info('load log from %s at %s', f, dirpath)
                        #bname=appdir +'/' + f[:f.rfind(filepattern)]
                        bname= f[:f.rfind(filepattern)]

                        # get this runid of log
                        idx = 0
                        iternum =  len(itertime) 
                        nodenum = 1
                        # there should all be the same
                        logger.info('total %d iterations, %d nodes, shape=%s', iternum, nodenum, 0)
                        #logger.info('itertime: %s', itertime)
                        #logger.info('likelihood: %s', likelihood)

                        itertime=[[x[0] for x in itertime]]
                        likelihood=[[x[0],x[1]] for x in likelihood]
                        #logger.info('itertime: %s', itertime)
                        #logger.info('likelihood: %s', likelihood)


                        iterMatrix = np.array(itertime)
                        lhMatrix = np.array(likelihood)
                        # run time: col1:app_time, col2:train_time
                        runtimeMatrix = np.zeros((1,2))
                        # add iter_t matrix, (nodenum, iternum)
                        imat = np.cumsum(iterMatrix).reshape((1,iternum))
                        runtimeMatrix = np.concatenate((runtimeMatrix, imat), axis=1)
 
                        runtimeMatrix = runtimeMatrix / 1000



                        # run time: col1:app_time, col2:train_time
                        np.savetxt(bname + ".itertime", iterMatrix, fmt='%d')
                        np.savetxt(bname + ".runtime", runtimeMatrix, fmt='%d')
                        #np.savetxt(bname + ".likelihood", likelihood, fmt='%e')
                        self.save_likelihood(likelihood, bname + '.likelihood')

                        #min, max, mean analysis
                        # mean/std of compute, comm, iter restured
                        # runtime stat
                        statMatrix = np.zeros((4, 2 + iternum))
                        statMatrix[0] = np.min(runtimeMatrix, axis=0)
                        statMatrix[1] = np.max(runtimeMatrix, axis=0)
                        statMatrix[2] = np.mean(runtimeMatrix, axis=0)
                        statMatrix[3] = np.std(runtimeMatrix, axis=0)
                        np.savetxt(bname + '.runtime-stat', statMatrix,fmt='%.2f')

                        # itertime
                        statMatrix = np.zeros((4, iternum))
                        statMatrix[0] = np.min(iterMatrix, axis=0)
                        statMatrix[1] = np.max(iterMatrix, axis=0)
                        statMatrix[2] = np.mean(iterMatrix, axis=0)
                        statMatrix[3] = np.std(iterMatrix, axis=0)
                        np.savetxt(bname + '.iter-stat', statMatrix,fmt='%.2f')


    #
    # lightlda
    #
    def load_timelog_lightlda(self, logfile):
        logf = open(logfile,'r')

        totalNumTokens = 0
        app_span = 0
        train_span = 0
        elapsed=[]
        itertime=[]
        tokencnt=[]
        likelihood=[]
        last_iterspan = 0
        lightlda_startiter = "num_slice:\d+, num_block:\d+"
        lightlda_time="Time used: (\d+\.\d+]*) s"
        #lightlda_doclh="doc likelihood : ([-+]?\d+\.\d+e\+\d+)"
        lightlda_wordlh="word likelihood : ([-+]?\d+\.\d+e\+\d+)"
        lightlda_likelihood="word_log_likelihood : ([-+]?\d+\.\d+e\+\d+)"

        iterid = 0
        slice = 0
        A , B, _time = 0.,0., 0.
        for line in logf:
            m = re.search(lightlda_startiter, line)
            if m:
                if _time !=0.:
                    itertime.append(( _time, 0) )

                #update the last one
                if A != 0.:
                    _wlh = (A-B)/slice + B
                    likelihood.append(( iterid, _wlh))
                    #logger.info('iter=%d, slice=%d, wlh=%f, time=%f', iterid, slice, _wlh, _time)

                #start a new iteration
                A , B, _time = 0.,0., 0.
                slice = 0

                iterid += 1

            m = re.search(lightlda_time, line)
            if m:
                #
                # itertime< traintime from app,  traintime from wall clock>
                #
                _time += float(m.group(1))*1000
            
            m = re.search(lightlda_wordlh, line)
            if m:
                B += float(m.group(1))
                slice += 1
 
            m = re.search(lightlda_likelihood, line)
            if m:
                A += float(m.group(1))

        return itertime, likelihood

    def load_applog_lightlda(self, appdir, filepattern='.log'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f.startswith('lightlda') and f.endswith(filepattern):
                    itertime, likelihood = self.load_timelog_lightlda(os.path.join(dirpath, f))
                    if len(itertime) > 0:
                        logger.info('load log from %s at %s', f, dirpath)
                        #bname=appdir +'/' + f[:f.rfind(filepattern)]
                        bname= f[:f.rfind(filepattern)]

                        # get this runid of log
                        idx = 0
                        iternum =  len(itertime) 
                        nodenum = 1
                        # there should all be the same
                        logger.info('total %d iterations, %d nodes, shape=%s', iternum, nodenum, 0)
                        #logger.info('itertime: %s', itertime)
                        #logger.info('likelihood: %s', likelihood)

                        itertime=[[x[0] for x in itertime]]
                        likelihood=[[x[0],x[1]] for x in likelihood]
                        #logger.info('itertime: %s', itertime)
                        #logger.info('likelihood: %s', likelihood)


                        iterMatrix = np.array(itertime)
                        lhMatrix = np.array(likelihood)
                        # run time: col1:app_time, col2:train_time
                        runtimeMatrix = np.zeros((1,2))
                        # add iter_t matrix, (nodenum, iternum)
                        imat = np.cumsum(iterMatrix).reshape((1,iternum))
                        runtimeMatrix = np.concatenate((runtimeMatrix, imat), axis=1)
                        runtimeMatrix = runtimeMatrix / 1000


                        np.savetxt(bname + ".itertime", iterMatrix, fmt='%d')
                        np.savetxt(bname + ".runtime", runtimeMatrix, fmt='%d')
                        np.savetxt(bname + ".likelihood", likelihood, fmt='%e')
                        #self.save_likelihood(likelihood, bname + '.likelihood')

                        #min, max, mean analysis
                        # mean/std of compute, comm, iter restured
                        # runtime stat
                        statMatrix = np.zeros((4, 2 + iternum))
                        statMatrix[0] = np.min(runtimeMatrix, axis=0)
                        statMatrix[1] = np.max(runtimeMatrix, axis=0)
                        statMatrix[2] = np.mean(runtimeMatrix, axis=0)
                        statMatrix[3] = np.std(runtimeMatrix, axis=0)
                        np.savetxt(bname + '.runtime-stat', statMatrix,fmt='%.2f')

 
                        # itertime
                        statMatrix = np.zeros((4, iternum))
                        statMatrix[0] = np.min(iterMatrix, axis=0)
                        statMatrix[1] = np.max(iterMatrix, axis=0)
                        statMatrix[2] = np.mean(iterMatrix, axis=0)
                        statMatrix[3] = np.std(iterMatrix, axis=0)
                        np.savetxt(bname + '.iter-stat', statMatrix,fmt='%.2f')

    #
    # nomadlda
    #
    def load_timelog_nomadlda(self, logfile):
        logf = open(logfile,'r')

        totalNumTokens = 0
        lastcnt = 0
        itertime=[]
        tokencnt=[]
        likelihood=[]

        totaltoken_format="init phase done! (\d+) tokens"
        nomadlda_format=":iter ([0-9]*) .*time-1 (\d+\.\d+]*) .*training-LL ([-+]?\d*\.\d+e\+\d+]*) Nwt (\d+)"
        for line in logf:
            #new format first
            m = re.search(totaltoken_format, line)
            if m:
                totalNumTokens = int(m.group(1))

            #m = re.search(self.pattern[self.name+'-newformat'], line)
            m = re.search(nomadlda_format, line)
            if m:
                #
                # itertime< traintime from app,  traintime from wall clock>
                #
                itertime.append(( float(m.group(2))*1000, 0) )
                likelihood.append(( int(m.group(1)), float(m.group(3))))
                newcnt = int(m.group(4))
                tokencnt.append( (newcnt - lastcnt , 0))
                lastcnt = newcnt
                continue
        return itertime, likelihood, tokencnt, totalNumTokens


    def load_applog_nomadlda(self, appdir, filepattern='.log'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f.startswith('nomadlda') and f.endswith(filepattern):
                    itertime, likelihood,tokencnt,totalNumTokens = self.load_timelog_nomadlda(os.path.join(dirpath, f))
                    if len(itertime) > 0:
                        logger.info('load log from %s at %s', f, dirpath)
                        #bname=appdir +'/' + f[:f.rfind(filepattern)]
                        bname= f[:f.rfind(filepattern)]

                        # get this runid of log
                        idx = 0
                        iternum =  len(itertime) 
                        nodenum = 1
                        # there should all be the same
                        logger.info('total %d iterations, %d nodes, shape=%s', iternum, nodenum, 0)
                        #logger.info('itertime: %s', itertime)
                        #logger.info('likelihood: %s', likelihood)

                        itertime=[[x[0] for x in itertime]]
                        likelihood=[[x[0],x[1]] for x in likelihood]
                        updatecnt=[[x[0] for x in tokencnt]]
                        #logger.info('itertime: %s', itertime)
                        #logger.info('likelihood: %s', likelihood)


                        iterMatrix = np.array(itertime)
                        lhMatrix = np.array(likelihood)
                        updateMatrix = np.array(updatecnt)
                        # run time: col1:app_time, col2:train_time
                        runtimeMatrix = np.zeros((1,2))
                        # add iter_t matrix, (nodenum, iternum)
                        imat = np.cumsum(iterMatrix).reshape((1,iternum))
                        runtimeMatrix = np.concatenate((runtimeMatrix, imat), axis=1)
                        runtimeMatrix = runtimeMatrix / 1000


                        # run time: col1:app_time, col2:train_time
                        np.savetxt(bname + ".itertime", iterMatrix, fmt='%d')
                        np.savetxt(bname + ".runtime", runtimeMatrix, fmt='%d')
                        #np.savetxt(bname + ".likelihood", likelihood, fmt='%e')
                        self.save_likelihood(likelihood, bname + '.likelihood')

                        np.savetxt(bname + ".update", updateMatrix, fmt='%d')

                        #min, max, mean analysis
                        # mean/std of compute, comm, iter restured
                        # runtime stat
                        statMatrix = np.zeros((4, 2 + iternum))
                        statMatrix[0] = np.min(runtimeMatrix, axis=0)
                        statMatrix[1] = np.max(runtimeMatrix, axis=0)
                        statMatrix[2] = np.mean(runtimeMatrix, axis=0)
                        statMatrix[3] = np.std(runtimeMatrix, axis=0)
                        np.savetxt(bname + '.runtime-stat', statMatrix,fmt='%.2f')


                        # itertime
                        statMatrix = np.zeros((4, iternum))
                        statMatrix[0] = np.min(iterMatrix, axis=0)
                        statMatrix[1] = np.max(iterMatrix, axis=0)
                        statMatrix[2] = np.mean(iterMatrix, axis=0)
                        statMatrix[3] = np.std(iterMatrix, axis=0)
                        np.savetxt(bname + '.iter-stat', statMatrix,fmt='%.2f')

                        # update stat, add sum at row[4], ratio of iteration
                        statMatrix = np.zeros((6, iternum))
                        statMatrix[0] = np.min(updateMatrix, axis=0)
                        statMatrix[1] = np.max(updateMatrix, axis=0)
                        statMatrix[2] = np.mean(updateMatrix, axis=0)
                        statMatrix[3] = np.std(updateMatrix, axis=0)
                        statMatrix[4] = np.cumsum(np.sum(updateMatrix, axis=0))
                        statMatrix[5] = statMatrix[4] / totalNumTokens
                        np.savetxt(bname + '.update-stat', statMatrix,fmt='%.2f')



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




