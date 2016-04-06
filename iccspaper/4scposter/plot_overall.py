#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Plot the overall performance firugres on performance data

"""

import sys,os,re
import datetime
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
#matplotlib.use('Agg')
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
    # output four figures
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overall_traintime', 'data', 'overall_runtime.clueweb', 'overall_traintime.clueweb.png', "Overall TrainTime on Clueweb Dataset")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overall_runtime', 'data', 'overall_runtime.clueweb', 'overall_runtime.clueweb.png', "Overall RunTime on Clueweb Dataset")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overall_traintime', 'data', 'overall_runtime.enwiki', 'overall_traintime.enwiki.png', "Overall TrainTime on Enwiki Dataset")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overall_runtime', 'data', 'overall_runtime.enwiki', 'overall_runtime.enwiki.png', "Overall RunTime on Enwiki Dataset")


def draw_all():
    ploter.init_subplot(2,2)
    ploter.fig.suptitle("LDA Trainers Overall Excution Time")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)

    # output (2,2) subplots
    ploter.set_subplot(1,1)
    call_plot('overall_traintime', 'data', 'overall_runtime.clueweb', '', "Overall TrainTime on Clueweb Dataset")
    ploter.set_subplot(1,2)
    call_plot('overall_runtime', 'data', 'overall_runtime.clueweb', '', "Overall RunTime on Clueweb Dataset")
    ploter.set_subplot(2,1)
    call_plot('overall_traintime', 'data', 'overall_runtime.enwiki', '', "Overall TrainTime on Enwiki Dataset")
    ploter.set_subplot(2,2)
    call_plot('overall_runtime', 'data', 'overall_runtime.enwiki', '', "Overall RunTime on Enwiki Dataset")
    ploter.savefig('overall_all.png')

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
