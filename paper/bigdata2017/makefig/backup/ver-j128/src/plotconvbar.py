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

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('converge_level', '../../data', conffile, '-convergebar.pdf',conf) 



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

    shortview = (sys.argv[2] == 'True')
    ploter.use_shortest_x = shortview
    logger.info('set use_shortest_x as : %s', shortview)
 
    conf={}
    conf['title']=''
    conf['xticks']=['30x30','60x20']
    conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']
    conf['lines']=['o-','^-','d-']*10
    conf['loc'] = 0
    conf['xlabel'] = 'Nodes x Threads'
    confset['converge_level'] = conf
 
    draw_newharp(sys.argv[1], confset)
