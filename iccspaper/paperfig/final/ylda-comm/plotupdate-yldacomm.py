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
#matplotlib.use('Svg')
import matplotlib.pyplot as plt
import logging
from analysis.plot_perf import PerfName, PlotEngine
import mplrc.ieee.transaction

logger = logging.getLogger(__name__)

# global share ploter
ploter = PlotEngine()

gridFlag = True

def call_plot(plotname, datadir, namefile, figname, title):
    conf = {}
    conf['title'] = title
    perfname = PerfName(namefile)
    ploter.init_data(datadir, perfname)
    ploter.plot(plotname, figname, conf)



def draw_init():
    params ={\
        'backend': 'GTKAgg',
        
        #'font.fontname':'Calibri',
        'font.weight': 900,
        'font.family': 'serif',
        'font.serif': ['Times', 'Palatino', 'New Century Schoolbook', 'Bookman', 'Computer Modern Roman'],
        'font.sans-serif' : ['Helvetica', 'Avant Garde', 'Computer Modern Sans serif'],
    #font.cursive       : Zapf Chancery
    #font.monospace     : Courier, Computer Modern Typewriter
        'text.usetex': True,
        
        'axes.labelsize': 12,
        'axes.linewidth': .75,
        
        'figure.figsize': (4, 3),
        'figure.subplot.left' : 0.175,
        'figure.subplot.right': 0.95,
        'figure.subplot.bottom': 0.15,
        'figure.subplot.top': .95,
        
        'figure.dpi':150,
        
        'text.fontsize': 5,
        'legend.fontsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        
        'lines.linewidth':1.25,
        'savefig.dpi':600,
        }
    
    plt.rcParams.update(params)

def draw_update():
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('comm_iter', '../../../data', 'ylda-all.100-clueweb-ib', 'ylda-comm-1-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('comm_iter', '../../../data', 'ylda-all.100-clueweb-eth', 'ylda-comm-1-4.pdf', '')

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('comm_iter', '../../../data', 'ylda-all.100-enwiki-ib', 'ylda-comm-2-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('comm_iter', '../../../data', 'ylda-all.100-enwiki-eth', 'ylda-comm-2-4.pdf', '')


if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_init()
#    draw_ylda()
#    draw_petuum()
    draw_update()
#    draw_iteracc()

