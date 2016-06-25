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


def draw_all():
    ploter.init_subplot(1,2)
    width = 8.5
    ploter.fig.set_size_inches(width, width/(4./3 * 1./2))

    matplotlib.rcParams.update({'text.fontsize': 5})
    matplotlib.rcParams.update({'legend.fontsize': 6})

    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', 'all.100-clueweb-ib', '','') 
    ploter.set_subplot(1,2)
    call_plot('overhead', '../../data', 'all.100-clueweb-ib', '', '')
    ploter.set_subplot(1,3)
    call_plot('overhead_all', '../../data', 'all.100-clueweb-ib', '', '')

    ploter.set_subplot(2,1)
    call_plot('accuracy_overalltime', '../../data', 'all.100-enwiki-bigram-ib', '','') 
    ploter.set_subplot(2,2)
    call_plot('overhead', '../../data', 'all.100-enwiki-bigram-ib', '', '')
    ploter.set_subplot(2,3)
    call_plot('overhead_all', '../../data', 'all.100-enwiki-bigram-ib', '', '')

    ploter.set_subplot(3,1)
    call_plot('accuracy_overalltime', '../../data', 'all.100-gutenberg-ib', '','') 
    ploter.set_subplot(3,2)
    call_plot('overhead', '../../data', 'all.100-gutenberg-ib', '', '')
    ploter.set_subplot(3,3)
    call_plot('overhead_all', '../../data', 'all.100-gutenberg-ib', '', '')



    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.fig.subplots_adjust(wspace=0.4)

    ploter.fig.tight_layout()
    ploter.savefig('vspetuum_all.pdf')

def draw_single():
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

    #matplotlib.rcParams.update({'font.weight': 'bold'})
    #matplotlib.rcParams.update({'figure.figsize': (4,3)})
    #matplotlib.rcParams.update({'text.fontsize': 5})
    #matplotlib.rcParams.update({'legend.fontsize': 6})

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', 'all.100-clueweb-ib', 'petuum-1-1.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', 'all.100-clueweb-ib', 'petuum-1-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_end', '../../data', 'all.100-clueweb-ib', 'petuum-1-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_all', '../../data', 'all.100-clueweb-ib', 'petuum-1-4.pdf', '')

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', 'all.100-enwiki-bigram-ib', 'petuum-2-1.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', 'all.100-enwiki-bigram-ib', 'petuum-2-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_end', '../../data', 'all.100-enwiki-bigram-ib', 'petuum-2-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_all', '../../data', 'all.100-enwiki-bigram-ib', 'petuum-2-4.pdf', '')

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', 'all.100-gutenberg-ib', 'petuum-3-1.pdf','') 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', 'all.100-gutenberg-ib', 'petuum-3-2.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_end', '../../data', 'all.100-gutenberg-ib', 'petuum-3-3.pdf', '')
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead_all', '../../data', 'all.100-gutenberg-ib', 'petuum-3-4.pdf', '')

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_single()

