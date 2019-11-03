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
        'font.weight': 900,
        'font.serif': ['Times', 'Palatino', 'New Century Schoolbook', 'Bookman', 'Computer Modern Roman'],
        'font.sans-serif' : ['Helvetica', 'Avant Garde', 'Computer Modern Sans serif'],
        'font.family': 'sans-serif',
        #font.cursive       : Zapf Chancery
        #font.monospace     : Courier, Computer Modern Typewriter
        'text.usetex': False,
        
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

    params2 = {\
        'backend': 'GTKAgg',
        'font.weight': 900,
        'font.family': 'serif',
        'text.usetex': False,
        'axes.labelsize': 8,
        'axes.linewidth': .75,
        'figure.figsize': (4, 3),
        'figure.subplot.left' : 0.175,
        'figure.subplot.right': 0.95,
        'figure.subplot.bottom': 0.15,
        'figure.subplot.top': .95,
        'figure.dpi':150,
        'text.fontsize': 5,
        'legend.fontsize': 8,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'lines.linewidth':1.25,
        'lines.markersize': 5,
        'savefig.dpi':600,
        }

    plt.rcParams.update(params)

def draw_modelsplit():

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('model_split', '.', 'modelsplit.name', 'model-split.pdf','') 

def draw_modelzipf():
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    ploter.curax.grid(gridFlag)
    call_plot('model_zipf', '.', 'modelzipf.name', 'model-zipf.pdf','') 


if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_init()
    draw_modelsplit()
    draw_modelzipf()

