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




def draw_ylda():
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', 'ylda-all.100-clueweb-ib', 'ylda-1-1.pdf','') 

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('iter_trend_all', '../../data', 'ylda-all.100-clueweb-ib', 'ylda-1-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)

    call_plot('overall_runtime', '../../data', 'ylda-opt.100-clueweb-eth-ib', 'ylda-1-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)

    call_plot('accuracy_overalltime', '../../data', 'ylda-all.100-enwiki-ib', 'ylda-2-1.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)

    call_plot('iter_trend_all', '../../data', 'ylda-all.100-enwiki-ib', 'ylda-2-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)

    call_plot('overall_runtime', '../../data', 'ylda-opt.100-enwiki-eth-ib', 'ylda-2-3.pdf', '')

def draw_petuum():
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', 'petuum-all.100-clueweb-ib', 'petuum-1-1.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', 'petuum-all.100-clueweb-ib', 'petuum-1-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_end', '../../data', 'petuum-all.100-clueweb-ib', 'petuum-1-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_all', '../../data', 'petuum-all.100-clueweb-ib', 'petuum-1-4.pdf', '')

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', 'petuum-all.100-enwiki-bigram-ib', 'petuum-2-1.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', 'petuum-all.100-enwiki-bigram-ib', 'petuum-2-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_end', '../../data', 'petuum-all.100-enwiki-bigram-ib', 'petuum-2-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_all', '../../data', 'petuum-all.100-enwiki-bigram-ib', 'petuum-2-4.pdf', '')

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', 'petuum-all.100-gutenberg-ib', 'petuum-3-1.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', 'petuum-all.100-gutenberg-ib', 'petuum-3-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_end', '../../data', 'petuum-all.100-gutenberg-ib', 'petuum-3-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_all', '../../data', 'petuum-all.100-gutenberg-ib', 'petuum-3-4.pdf', '')

def draw_update():
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)

    call_plot('overall_runtime', '../../../data', 'ylda-opt.100-clueweb-eth-ib', 'ylda-1-3-16gbps.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)

    call_plot('overall_runtime', '../../../data', 'ylda-opt.100-enwiki-eth-ib', 'ylda-2-3-16gbps.pdf', '')

def draw_iteracc():
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', '../../data', 'iteracc-all.100-clueweb-ib', 'iter-acc-1.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)

    call_plot('accuracy_iter', '../../data', 'iteracc-all.100-enwiki-ib', 'iter-acc-2.pdf', '')

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
