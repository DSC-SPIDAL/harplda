#!/usr/bin/
# -*- coding: utf-8 -*-

"""
Evaluate performance by the time to reach the smae convergence level

Usage:
    fitcurve [-type] [confname] [convergence level]
        -type   :   
        showvar ; show variance ratio for each iteration
        eval    ; print relative performance for each curve
            first curve is the standard base
        speedup ; calcluate the speedup of training time along the convergence level, with the first curve as the base

    examples:
        fitcurve -showvar clueweb30-30x60.conf
        fitcurve -eval clueweb30-30x60.conf 2.605+e11
        fitcurve -speedup clueweb30-30x60.conf

"""

import sys,os,re
import datetime
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Svg')
import matplotlib.pyplot as plt
import logging
from analysis.plot_perf import PerfName, PerfData, PlotEngine
from plot_init import PlotConfigure
from optparse import OptionParser

logger = logging.getLogger(__name__)

plotconf = PlotConfigure()

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

        dataVecs.append((iterVec, rmseVec, timeSumVec))

    #    <cruveid, <rmse, time, speedup>>
    levelCnt = dataVecs[0][ID_RMSE].shape[0]
    result = np.zeros((curveCnt, levelCnt, 3))


    
    #search the time for all convergence level by interpolation
    for iter in range(levelCnt):
        level = dataVecs[0][ID_RMSE][iter]
        baseX = dataVecs[0][ID_TIME][iter]
        logger.debug('Fit Level=%s, %s', level, '='*20)

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
                        iterpolateX = xb - (level - yb)*(xb-xa)/(ya-yb)
                    break

                elif rmseVec[idx] < level and rmseVec[idx+1] >= level:
                    #interpolation
                    xa = timeVec[iterVec[idx]-1]
                    xb = timeVec[iterVec[idx+1]-1]
                    ya = rmseVec[idx]
                    yb = rmseVec[idx+1]

                    iterpolateX = xb - (level - yb)*(xb-xa)/(ya-yb)
                    logger.debug('Curve:%d, [xa=%s,ya=%s]-- [xb=%s,yb=%s], fit level=%s',
                            curveId,xa,ya, xb, yb,level)
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
    usage = 'fitcurve.py --draw [showvar|eval|speedup] --level <converge level> <config file>'
    parser = OptionParser(usage)
    parser.add_option("--draw", type=str, dest="drawtype", default='speedup',help='set the command')
    parser.add_option("--level",type=str, dest="levelValue", help='set the convergence level for eval command')
    parser.add_option("--extrapolation",action="store_true", help='set to use extrapolation in calculate the speedup')
    opt, args = parser.parse_args()

    # check and process input arguments
    if len(args) != 1:
        print(globals()['__doc__'] % locals())
        print(parser.print_help())
        sys.exit(1)

    logger.info("running %s" % ' '.join(sys.argv))

    # check the path
    confname = args[0]

    datadir = plotconf.dataroot

    conf = {}
    perfname = PerfName(confname)
    perfdata = PerfData(datadir)
    
    if opt.drawtype == 'showvar':
        draw_showvar(perfdata, perfname)
    elif opt.drawtype == 'eval':
        logger.info('set convergence level as : %s', opt.levelValue)
        draw_eval(perfdata, perfname, opt.levelValue)
    elif opt.drawtype == 'speedup':
        draw_speedup(perfdata, perfname, opt.extrapolation)
    else:
        print(globals()['__doc__'] % locals())
        print(parser.print_help())





