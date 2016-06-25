#!/usr/bin/
# -*- coding: utf-8 -*-

"""
Plot the comm/computation time breakwodn

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

logger = logging.getLogger(__name__)

# global share ploter
ploter = PlotEngine()

def call_plot(plotname, datadir, namefile, figname, title):
    conf = {}
    conf['title'] = title
    perfname = PerfName(namefile)
    ploter.init_data(datadir, perfname)
    ploter.plot(plotname, figname, conf)


def draw_single():
    # clueweb
    ploter.init_subplot(1,1)
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', 'docslice.100-clueweb-ib', 'sync_freq.overhead.ib.clueweb.svg', "Overhead on Clueweb Dataset,IB")

    ploter.init_subplot(1,1)
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
    ploter.set_subplot(1,1)
    call_plot('comm_breakdown','../../data', 'docslice.100-clueweb-ib', 'sync_freq.comm_breakdown.ib.clueweb.svg', "Comm/Computation time breakdown on Clueweb Dataset,IB")

def draw_all():
    # output (2,2) subplots
    ploter.init_subplot(2,2)
    ploter.fig.suptitle("Sync Frequency Analysis on Clueweb Dataset, IB")
    ploter.fig.set_size_inches(9.25*3, 5.25*3)

    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', 'docslice.100-clueweb-ib', '', "Overhead")
    ploter.set_subplot(1,2)
    call_plot('comm_breakdown','../../data', 'docslice.100-clueweb-ib', '', "Comm/Computation Time Breakdown")
    
    ploter.set_subplot(2,1)
    call_plot('accuracy_iter', '../../data', 'docslice.100-clueweb-ib', '', "Accuracy over Iteration")
    ploter.set_subplot(2,2)
    call_plot('accuracy_runtime','../../data', 'docslice.100-clueweb-ib', '', "Accuracy over Training Time")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('syncfreq_clueweb.svg')
    


if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_single()
    draw_all()
