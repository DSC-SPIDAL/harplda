#!/usr/bin/
# -*- coding: utf-8 -*-

"""
Detect Straggler from the running logs

.update-raw
    <iter, rankid, updatecnt, ..>

.update-cv
    each line is the statistics of one iteration
    <mean, std, cv, argmin, argmax>

"""

import sys,os,re
import datetime
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Svg')
import matplotlib.pyplot as plt
import logging
#from analysis.plot_perf import PerfName, PerfData, PlotEngine
#from plot_init import PlotConfigure
from optparse import OptionParser

logger = logging.getLogger(__name__)

#plotconf = PlotConfigure()


class LDATrainerLog():
    trainers=['mallet','harp','ylda','warplda','lightlda','nomadlda','petuum','petuum-run','petuum-new']

    def __init__(self,name):
        if name not in self.trainers:
            raise NameError('no %s trainer support yet, quit.'%name)
        self.name = name
        self.engine={
            #'harp':self.load_applog_harp,
            'nomadlda':self.load_applog_nomadlda
        }

    def load_applog(self, logdir):
        return self.engine[self.name](logdir)


    #
    # nomadlda
    #
    def load_timelog_nomadlda(self, logfile):
        """
        input:
            rank 22 iter 2 localNwt 6171993862 localNt 1920

        """
        logf = open(logfile,'r')

        nomadlda_format="rank ([0-9]*) iter (\d+) localNwt (\d+) localNt (\d+)"
        tokeninfo=[]

        for line in logf:
            m = re.search(nomadlda_format, line)
            if m:
                tokeninfo.append(( int(m.group(2)), int(m.group(1)),int(m.group(3)),int(m.group(4))))


        #check the integral <iter, rank, localNwt, localNt>
        mat = np.array(tokeninfo)
        maxiter = np.max(mat[:,0])
        maxrank = np.max(mat[:,1])

        #sort by iter, then by rank
        mat.view('i8,i8,i8,i8').sort(order=['f0','f1'], axis = 0)

        rows = mat.shape[0]
        #check all the iters
        checkedIter = 0
        for iter in range(1, maxiter+1):
            rowcnt = mat[mat[:,0] == iter].shape[0]
            if rowcnt != maxrank+1:
                logger.error('rank count(%d) error in iter %d (should be %d)', rowcnt, iter, maxrank+1)
                break
            checkedIter = iter

        #reshape, to retain the good logs
        localNwt = np.copy(mat[:,2].reshape((checkedIter,  (maxrank + 1))))

        return localNwt , mat


    def load_applog_nomadlda(self, appdir, filepattern='.log'):
        models = []
        for dirpath, dnames, fnames in os.walk(appdir):
            for f in fnames:
                if f.startswith('nomadlda') and f.endswith(filepattern):
                    logger.info('load log from %s at %s', f, dirpath)
                    #shape <iternum, nodenum>
                    localNwt, mat = self.load_timelog_nomadlda(os.path.join(dirpath, f))
                    iternum, nodenum = localNwt.shape

                    if iternum > 0:
                        #bname=appdir +'/' + f[:f.rfind(filepattern)]
                        bname= f[:f.rfind(filepattern)]
                        logger.info('total %d iterations, %d nodes, shape=%s', iternum, nodenum, 0)

                        #localNwt for each iteration
                        for iter in range(iternum-1, 0, -1):
                            localNwt[iter] = localNwt[iter] - localNwt[iter-1]
                        
                        #<mean, std, cv, argmin, argmax>
                        statMatrix = np.zeros((iternum, 5))
                        statMatrix[:,0] = np.mean(localNwt, axis = 1)
                        statMatrix[:,1] = np.std(localNwt, axis = 1)
                        statMatrix[:,2] = statMatrix[:,1] / statMatrix[:,0]

                        statMatrix[:,3] = np.argmin(localNwt, axis = 1)
                        statMatrix[:,4] = np.argmax(localNwt, axis = 1)

                        np.savetxt(bname + '.update-cv', statMatrix,fmt='%.2f')
                        np.savetxt(bname + '.update-raw', mat,fmt='%.2f')


def draw_showvar(perfdata, perfname):
    dataflist = []
    #for name,label in self.perfname:
    for tp in perfname:
        name = tp[0]
        fname = name + '.likelihood'
        dataflist.append(fname)
        fname = name + '.runtime-stat'
        dataflist.append(fname)
    perfdata.load(dataflist)

    #rmse: iternum, time, rmse,...
    logger.info('likelihood variance for each iteration')
    for tp in perfname:
        name = tp[0] + '.likelihood'
        pdata = perfdata[name] 
        logger.info('name: %s', name)

        varMat = np.diff(pdata, axis=0)
        varVec = varMat[1:,1] / varMat[1:,0]
        logger.info('varVec = %s', varVec)

        for idx in range(varVec.shape[0]):
            print('%s\t:%s, ratio = %s\n'%(pdata[idx + 1,1] ,varVec[idx], varVec[idx]/pdata[idx+1,1]))

def draw_eval(perfdata, perfname, level):
    figdata = []
    dataflist = []
    #for name,label in self.perfname:
    for tp in perfname:
        name = tp[0]
        label = tp[1]
        fname = name + '.likelihood'
        dataflist.append(fname)
        fname = name + '.runtime-stat'
        dataflist.append(fname)

        figdata.append(label)

    perfdata.load(dataflist)

    #rmse: iternum, time, rmse,...
    result=[]
    for id in range(len(perfname.perfname)):
        logger.info('name: %s', perfname.perfname[id])

        name = perfname.perfname[id][0] + '.likelihood'
        rmseVec = perfdata[name][:,1] 
        iterVec = perfdata[name][:,0] 
        itercnt = rmseVec.shape[0]

        name = perfname.perfname[id][0] + '.runtime-stat'
        timeVec = perfdata[name][2,2:]

        for idx in range(rmseVec.shape[0]):
            if idx == itercnt -1 and rmseVec[idx] < level:
                #interpolation
                xa = timeVec[iterVec[idx-1]-1]
                xb = timeVec[iterVec[idx]-1]
                ya = rmseVec[idx-1]
                yb = rmseVec[idx]
               
            elif rmseVec[idx] < level and rmseVec[idx+1] >= level:
                #interpolation
                xa = timeVec[iterVec[idx]-1]
                xb = timeVec[iterVec[idx+1]-1]
                ya = rmseVec[idx]
                yb = rmseVec[idx+1]
 
            else:
                continue

            iterpolateX = xb - (level - yb)*(xb-xa)/(ya-yb)
            if id == 0:
                # the base line
                baseX = iterpolateX
                print('iter=%s, X = %s, Y = %s, ratio = %s\n'%(iterVec[idx], iterpolateX, rmseVec[idx], iterpolateX / baseX))
                result.append([figdata[id],perfname.perfname[id][0], iterpolateX, iterpolateX/baseX])
            else:
                print('iter=%s, X = %s, Y = %s, ratio = %s\n'%(iterVec[idx], iterpolateX, rmseVec[idx], iterpolateX / baseX))
                result.append([figdata[id],perfname.perfname[id][0], iterpolateX, iterpolateX/baseX])
                break

    #output
    print('converge level = %s'%level)
    for item in result:
        print('%s\t%s\t%s\t%s'%(item[0], item[1], item[2], item[3]))

        #write into result file
        with open(item[1] + '.converge' , 'a') as wf:
            wf.write('%s %s\n'%(level, item[2]))


    return np.array(result)




def draw_speedup(perfdata, perfname, extrapolation = False):
    """
    Input:
        .conf   ; perfnames
    Ouput:
        <cruveid, rmse, time, speedup>

        find the time to reach each convergence level of the first curve
        by interpolation and extrapolation on the convergence curve

    """
    figdata = []
    dataflist = []
    #for name,label in self.perfname:
    for tp in perfname:
        name = tp[0]
        label = tp[1]
        fname = name + '.likelihood'
        dataflist.append(fname)
        fname = name + '.iter-stat'
        dataflist.append(fname)

        figdata.append(label)

    perfdata.load(dataflist)

   #<curve, iter|rmse|time>
    ID_ITER, ID_RMSE, ID_TIME = 0,1,2
    RID_RMSE, RID_TIME, RID_SPEEDUP = 0,1,2
    dataVecs=[]


    curveCnt = len(perfname.perfname)
    for id in range(curveCnt):
        logger.info('name: %s', perfname.perfname[id])

        name = perfname.perfname[id][0] + '.likelihood'
        rmseVec = perfdata[name][:,1] 
        iterVec = perfdata[name][:,0] 

        name = perfname.perfname[id][0] + '.iter-stat'
        #get the average iter-time
        timeVec = perfdata[name][2,:]

        #cumsum to get the runtime
        timeSumVec = np.cumsum(timeVec)

        #get the time at the lh point
        #timeVec = timeSumVec[iterVec - 1]

        dataVecs.append((iterVec, rmseVec, timeSumVec))

    #    <cruveid, <rmse, time, speedup>>
    levelCnt = dataVecs[0][ID_RMSE].shape[0]
    result = np.zeros((curveCnt, levelCnt, 3))


    
    #search the time for all convergence level by interpolation
    for iter in range(levelCnt):
        level = dataVecs[0][ID_RMSE][iter]
        iterval = dataVecs[0][ID_ITER][iter]
        #baseX = dataVecs[0][ID_TIME][iter]
        baseX = dataVecs[0][ID_TIME][iterval-1]
        logger.debug('Fit Level=%s, baseX=%s, %s', level, baseX, '='*20)

        #set the first row
        result[0, iter, RID_RMSE] = level
        result[0, iter, RID_TIME] = baseX
        result[0, iter, RID_SPEEDUP] = 1

        # search for all other curves
        for curveId in range(1, curveCnt):
            rmseVec = dataVecs[curveId][ID_RMSE]
            iterVec = dataVecs[curveId][ID_ITER]
            timeVec = dataVecs[curveId][ID_TIME]
            itercnt = rmseVec.shape[0]

            #search this curve
            iterpolateX = -1
            for idx in range(rmseVec.shape[0]):
                if idx == itercnt -1 and rmseVec[idx] < level:
                    #extrapolation for the last point, or just skip it

                    xa = timeVec[iterVec[idx-1]-1]
                    xb = timeVec[iterVec[idx]-1]
                    ya = rmseVec[idx-1]
                    yb = rmseVec[idx]

                    if extrapolation:
                        iterpolateX = xb + (level - yb)*(xb-xa)/(yb-ya)
                    break

                elif rmseVec[idx] < level and rmseVec[idx+1] >= level:
                    #interpolation
                    xa = timeVec[iterVec[idx]-1]
                    xb = timeVec[iterVec[idx+1]-1]
                    ya = rmseVec[idx]
                    yb = rmseVec[idx+1]

                    iterpolateX = xa + (level - ya)*(xb-xa)/(yb-ya)
                    logger.debug('Curve:%d, [xa=%s,ya=%s]-- [xb=%s,yb=%s], iterpolateX=%s, speedup=%s',
                            curveId,xa,ya, xb, yb,iterpolateX, iterpolateX/baseX)
                    break

            #find the X if X > 0
            #speedup = T(1)/T(N)
            speedup = iterpolateX / baseX
            result[curveId, iter, RID_RMSE] = level
            result[curveId, iter, RID_TIME] = iterpolateX
            result[curveId, iter, RID_SPEEDUP] = speedup if speedup > 0 else 0

    #show result
    for curveId in range(curveCnt):
        logger.info('curveId=%s, Speedup = %s\n'%(perfname.perfname[curveId][1], result[curveId, :, RID_SPEEDUP]))

    #output
    result = result.reshape((curveCnt , 3* levelCnt))
    np.savetxt(perfname.confname + '.speedup', result, fmt='%.4f')

    return result

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)

    # cmd argument parser
    usage = 'straggler.py [options] <trainer> <logdir>'
    parser = OptionParser(usage)
    parser.add_option("--log", type=str, dest="logfile",help='input logfile name')
    parser.add_option("--fig",type=str, dest="figfile", default='output_straggler.pdf', help='set the output fig filename')
    opt, args = parser.parse_args()

    # check and process input arguments
    if len(args) != 2:
        print(globals()['__doc__'] % locals())
        print(parser.print_help())
        sys.exit(1)

    logger.info("running %s" % ' '.join(sys.argv))

    # check the path
    logAnalizer = LDATrainerLog(args[0])
    logAnalizer.load_applog(args[1])




