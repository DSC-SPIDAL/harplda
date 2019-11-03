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
from plot_init import PlotConfigure

logger = logging.getLogger(__name__)

# global share ploter
plotconf = PlotConfigure()
ploter = PlotEngine(False)

gridFlag = True
prefix = 'nlda'

def call_plot(plotname, datadir, namefile, figname, confset):
    perfname = PerfName(namefile)
    ploter.init_data(plotconf.dataroot, perfname)
    ploter.curax.grid(gridFlag)
    if plotname in confset:
        ploter.plot(plotname, figname, confset[plotname])
    else:
        ploter.plot(plotname, figname, confset['default'])

def draw_newharp(outname, conffile):

    plt.rcParams.update({'figure.figsize':(4*2,3)})
    plt.rcParams.update({'axes.titlesize':12})
    plt.rcParams.update({'axes.titleweight':'bold'})
    plt.rcParams.update({'legend.fontsize':12})

    nullconf={'default':{'title':''}}
    confset = {}
    conf={}
    conf['title']=''
    conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']*10
    conf['lines']=['o-','^-','d-','+-']*10
    confset['default'] = conf

    #set number of subplots
    ploter.init_subplot(1,2)

    #confset['default']['sample'] = 10
    #confset['default']['dosample'] = 'warp nomad'
    confset['default']['xlim'] = 1000
 
    conf['loc'] = 7
    ploter.set_subplot(1,1)
    confset['default']['title'] = '(a) Load Balance'
    call_plot('loadbalance_runtime', '', conffile, '', confset)

    conf['nolegend'] = True
    #confset['default']['errorbar'] = False 
    ploter.set_subplot(1,2)
    confset['default']['title'] = '(b) Overhead Ratio'
    call_plot('overhead_only', '', conffile, '', confset)

    #
    # save
    #
    plt.tight_layout()
    ploter.fig.savefig(outname + '.pdf')


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

    plotconf.draw_init()
    outname = sys.argv[1].split('.')[0]

    #draw_ylda()
    #draw_petuum()
    #draw_iteracc()
    draw_newharp(outname,sys.argv[1])
