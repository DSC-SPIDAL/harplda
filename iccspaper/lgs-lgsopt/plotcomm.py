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
    call_plot('comm_iter', '../data', 'ylda-all.100-clueweb-eth', 'comm_breakdown_ib.clueweb.svg', "Comm/Computation time breakdown on Clueweb Dataset,IB")

    # enwiki
    ploter.init_subplot(1,1)
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
    ploter.set_subplot(1,1)
    call_plot('comm_iter', '../data', 'ylda-all.100-enwiki-eth', 'comm_breakdown_ib.enwiki.svg', "Comm/Computation time breakdown on enwiki Dataset,IB")


if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_single()
