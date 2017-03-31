#!/usr/bin/
# -*- coding: utf-8 -*-

"""
Plot the accuracy performance firugres on performance data

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
from plot_init import draw_init

logger = logging.getLogger(__name__)

# global share ploter
ploter = PlotEngine(False)

gridFlag = True
prefix = 'nlda'

def call_plot(plotname, datadir, namefile, figname, title):
    conf = {}
    conf['title'] = title
    perfname = PerfName(namefile)
    ploter.init_data(datadir, perfname)
    ploter.plot(plotname, prefix + figname, conf)

def draw_newharp(conffile):
    #conffile='enwiki-1M_30x60-ib'

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('accuracy_overalltime', '../../data', conffile, '-1-1.pdf','') 

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('accuracy_runtime', '../../data', conffile, '-1-2.pdf','') 

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('accuracy_iter', '../../data', conffile, '-1-3.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('accuracy_itertime', '../../data', conffile, '-1-4.pdf','') 


    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', conffile, '-3-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_end', '../../data', conffile, '-3-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('overhead_all', '../../data', conffile, '-3-4.pdf', '')

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('loadbalance_runtime', '../../data', conffile, '-2-3.pdf', '')
    
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overall_runtime', '../../data', conffile, '-4-4.pdf', '')
 


if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    if len(sys.argv) >=3:
        prefix = sys.argv[2]

    draw_init()
    #draw_ylda()
    #draw_petuum()
    #draw_iteracc()
    draw_newharp(sys.argv[1])
