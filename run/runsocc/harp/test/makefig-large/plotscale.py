#!/usr/bin/
# -*- coding: utf-8 -*-

"""
Plot the accuracy performance firugres on performance data

Usage:
    plotit <confname> <shortview True|False>

"""

import sys,os,re
import datetime
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Svg')
import matplotlib.pyplot as plt
import logging
from analysis.plot_perf import PerfName, PlotEngine
from analysis.fitcurve import draw_eval
from plot_init import draw_init

logger = logging.getLogger(__name__)

# global share ploter
ploter = PlotEngine(False)

gridFlag = True
prefix = 'nlda'

def call_plot(plotname, datadir, namefile, figname, confset):
    perfname = PerfName(namefile)
    ploter.init_data(datadir, perfname)
    if plotname in confset:
        ploter.plot(plotname, prefix + figname, confset[plotname])
    else:
        ploter.plot(plotname, prefix + figname, confset['default'])


def draw_eval_bars(namefile, conf):

    level = 1.36e+11

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
 
    perfname = PerfName(namefile)
    ploter.init_data('../../data', perfname)
    #draw eval_bar chart
    figdata = draw_eval(ploter.perfdata, ploter.perfname, level)
    ploter.plot_converge_level(prefix + '-converge-bar.pdf', figdata)


def draw_newharp(conffile, conf):
    nullconf={'default':{'title':''}}

    #draw_eval_bars(conffile, nullconf)

    #conffile='enwiki-1M_30x60-ib'
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('scalability', '../../data', conffile, '-throughput-2.pdf',conf) 
    
    return

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('throughput_runtime', '../../data', conffile, '-throughput-1.pdf',conf) 

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('accuracy_overalltime', '../../data', conffile, '-1-1.pdf',conf) 

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('accuracy_runtime', '../../data', conffile, '-1-2.pdf',conf) 

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('accuracy_iter', '../../data', conffile, '-1-3.pdf',conf) 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('accuracy_itertime', '../../data', conffile, '-1-4.pdf',conf) 


    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', conffile, '-3-2.pdf', nullconf)
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_end', '../../data', conffile, '-3-3.pdf', nullconf)
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('overhead_all', '../../data', conffile, '-3-4.pdf', conf)

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('loadbalance_runtime', '../../data', conffile, '-2-3.pdf', conf)
    
#ploter.init_subplot(1,1)
#ploter.set_subplot(1,1)
#call_plot('overall_runtime', '../../data', conffile, '-4-4.pdf', '')
 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('converge_level', '../../data', conffile, '-converge-bar-1.pdf',conf) 



if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    draw_init()
    prefix = sys.argv[1].split('.')[0]

    confset = {}
    if len(sys.argv) > 2:
        if sys.argv[2] == 'TRUE':
            if len(sys.argv) > 3:
                #set xlim by sys.argv[3]
                ploter.use_shortest_x = True
                conf={}
                conf['title']=''
                conf['xlim'] = int(sys.argv[3])
                conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']
                conf['lines']=['o-','^-','d-']*10
                confset['default'] = conf
                conf={}
                conf['title']=''
                conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']
                conf['lines']=['o-','^-','d-']*10
                confset['accuracy_iter'] = conf
 
                conf={}
                conf['title']=''
                conf['xlim'] = int(sys.argv[3])
                conf['colors']=['r','r','b','b','g', 'g','c','c','y','k','r','b','m','g','c','y','k']
                conf['lines']=['-','--']*10
                confset['overhead_all'] = conf
                logger.info('set use_xlim_x as : %s', conf['xlim'])
            else:
                #only shortview
                shortview = (sys.argv[2] == 'True')
                ploter.use_shortest_x = shortview
                logger.info('set use_shortest_x as : %s', shortview)
        else:
            # maybe special to STRAGGLER
            # there are 4 lines with 2 groups
            ploter.use_shortest_x = True
            conf={}
            conf['title']=''
            conf['xlim'] = int(sys.argv[3])
#conf['colors']=['r','salmon','g', 'olivedrab','c','y','k','r','b','m','g','c','y','k']
            conf['colors']=['r','r','g', 'g','c','y','k','r','b','m','g','c','y','k']
            conf['lines']=['o-','o--','d-','d--']*10
            confset['default'] = conf
            conf={}
            conf['title']=''
#           conf['colors']=['r','salmon','g', 'olivedrab','c','y','k','r','b','m','g','c','y','k']
            conf['colors']=['r','r','g', 'g','c','y','k','r','b','m','g','c','y','k']
            conf['lines']=['o-','o--','d-','d--']*10
            confset['accuracy_iter'] = conf
 
            conf={}
            conf['title']=''
            conf['xlim'] = int(sys.argv[3])
            conf['colors']=['r','r','salmon','salmon','g', 'g','olivedrab','olivedrab','y','k','r','b','m','g','c','y','k']
#conf['colors']=['r','r','g', 'g','c','y','k','r','b','m','g','c','y','k']
            conf['lines']=['-','--']*10
            confset['overhead_all'] = conf
            logger.info('set use_xlim_x as : %s', conf['xlim'])

    else:
        conf={}
        conf['title']=''
        confset['default'] = conf
        plt.rcParams.update({'figure.figsize':(8,6)})
        logger.info('set large view')


    #draw_ylda()
    #draw_petuum()
    #draw_iteracc()
    draw_newharp(sys.argv[1], confset)
