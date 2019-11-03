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


def draw_all():
    # output (2,2) subplots
    ploter.init_subplot(3,2)
    ploter.fig.suptitle("System Reource Utilization")
    ploter.fig.set_size_inches(9.25*3, 5.25*3)

    ploter.set_subplot(1,1)
    call_plot('network', '../../data', '100-clueweb-ib', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,1)
    call_plot('freemem', '../../data', '100-clueweb-ib', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(3,1)
    call_plot('cpu', '../../data', '100-clueweb-ib', '', "Clueweb Dataset, 16Gbps Infiniband")


    ploter.set_subplot(1,2)
    call_plot('network','../../data', '100-clueweb-eth', '', "Clueweb Dataset, 1Gbps Ethernet")
    ploter.set_subplot(2,2)
    call_plot('freemem', '../../data', '100-clueweb-eth', '', "Clueweb Dataset, 1Gpbs Ethernet")
    ploter.set_subplot(3,2)
    call_plot('cpu', '../../data', '100-clueweb-eth', '', "Clueweb Dataset, 1Gpbs Ethernet")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('system_clueweb.png')
    

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_all()
