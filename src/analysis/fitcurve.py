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
    examples:
        fitcurve -showvar clueweb30-30x60.conf
        fitcurve -eval clueweb30-30x60.conf 2.605+e11

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

logger = logging.getLogger(__name__)



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
    drawtype = sys.argv[1]
    confname = sys.argv[2]

    datadir='../../data'
    conf = {}
    perfname = PerfName(confname)
    #ploter.init_data(plotconf.datadir, perfname, plotconf.savefmt)
    perfdata = PerfData(datadir)
    
    if drawtype == '-showvar':
        draw_showvar(perfdata, perfname)
    elif drawtype == '-eval':
        if len(sys.argv) >= 4:
            convlevel = float(sys.argv[3])
            logger.info('set convergence level as : %s', convlevel)
            draw_eval(perfdata, perfname, convlevel)
        else:
            logger.error(globals()['__doc__'] % locals())





