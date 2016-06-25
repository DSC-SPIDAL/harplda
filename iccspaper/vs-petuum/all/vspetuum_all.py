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

logger = logging.getLogger(__name__)

# global share ploter
ploter = PlotEngine()

def call_plot(plotname, datadir, namefile, figname, title):
    conf = {}
    conf['title'] = title
    perfname = PerfName(namefile)
    ploter.init_data(datadir, perfname)
    ploter.plot(plotname, figname, conf)


def draw_all(conf, figname):
    # output (2,2) subplots
    ploter.init_subplot(3,4)
    ploter.fig.suptitle("LDA Trainers by Local-Global Sync")
    ploter.fig.set_size_inches(9.25*8, 5.25*6)

    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', '../../data', conf, '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', '../../data', conf, '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(3,1)
    call_plot('accuracy_overalltime', '../../data', conf, '', "Clueweb Dataset, 16Gbps Infiniband")
 

    ploter.set_subplot(1,2)
    #call_plot('comm_breakdown', '../../data', conf, '', "Comm/Computation Time Breakdown,First 10 Iters")
    call_plot('overhead', '../../data', conf, '', "Overhead/Computation Time Breakdown,First 10 Iters")
    ploter.set_subplot(2,2)
    call_plot('overhead_end', '../../data', conf, '', "Overhead/Computation Time Breakdown,End 10 Iters")
    ploter.set_subplot(3,2)
    call_plot('overhead_all', '../../data', conf, '', "Overhead/Computation Time Breakdown")

    ploter.set_subplot(1,3)
    call_plot('comm_breakdown', '../../data', conf, '', "Comm/Computation Time Breakdown,First 10 Iters")
    ploter.set_subplot(2,3)
    call_plot('comm_breakdown_end', '../../data', conf, '', "Comm/Computation Time Breakdown,End 10 Iters")
    ploter.set_subplot(3,3)
    call_plot('comm_breakdown_all', '../../data', conf, '', "Comm/Computation Time Breakdown")

    ploter.set_subplot(1,4)
    call_plot('network', '../../data', conf, '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,4)
    call_plot('freemem', '../../data', conf, '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(3,4)
    call_plot('cpu', '../../data', conf, '', "Clueweb Dataset, 16Gbps Infiniband")


    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig(figname)

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_all(sys.argv[1], sys.argv[2])

