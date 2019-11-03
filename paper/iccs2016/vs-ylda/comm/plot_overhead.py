#!/usr/bin/
# -*- coding: utf-8 -*-

"""
Plot the overhead firugres on performance data

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


def draw_overhead_single():
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', 'data', 'overhead.bigram', 'overhead_ib.bigram.svg', "Computation Overhead on Enwiki-Bigram Dataset,IB")

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', 'data', 'overhead.gutenberg', 'overhead_ib.gutenberg.svg', "Computation Overhead on Gutenberg Dataset,IB")

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', 'data', 'clueweb.ib.word', 'overhead_ib.clueweb_word.svg', "Computation Overhead on Clueweb Dataset,Sample word")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', 'data', 'clueweb.ib.doc', 'overhead_ib.clueweb_doc.svg', "Computation Overhead on Clueweb Dataset,Sample doc")


def draw_enwiki_overall():
    # output (2,2) subplots
    ploter.init_subplot(1,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)

    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', 'data', 'accuracy_ib.clueweb', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
    call_plot('accuracy_overalltime', 'data', 'accuracy_eth.clueweb', '', "Clueweb Dataset, 1Gpbs Ethernet")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_clueweb_excutiontime.svg')
    
    # enwiki
    ploter.init_subplot(1,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
 
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', 'data','accuracy_ib.enwiki','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
    call_plot('accuracy_overalltime', 'data','accuracy_eth.enwiki','',"Enwiki Dataset, 1Gbps Ethernet")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_enwiki_excutiontime.svg')

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_overhead_single()
