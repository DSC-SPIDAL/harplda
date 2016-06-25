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
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-clueweb-ib', 'overhead_ib.clueweb.svg', "Overhead on Clueweb Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-clueweb-eth', 'overhead_eth.clueweb.svg', "Overhead on Clueweb Dataset,eth")
 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-enwiki-ib', 'overhead_ib.enwiki.svg', "Overhead on enwiki Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-enwiki-eth', 'overhead_eth.enwiki.svg', "Overhead on enwiki Dataset,eth")

    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-enwiki-bigram-ib', 'overhead_ib.bigram.svg', "Overhead on enwiki-bigram Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-gutenberg-ib', 'overhead_ib.gutenberg.svg', "Overhead on gugtenberg Dataset,IB")

def draw_all():
    # output (2,2) subplots
    ploter.init_subplot(3,2)
    ploter.fig.suptitle("Overhead")
    ploter.fig.set_size_inches(9.25*3, 5.25*3)

    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-clueweb-ib', '', "Overhead on Clueweb Dataset,IB")
    ploter.set_subplot(1,2)
    call_plot('overhead', '../../data', '100-clueweb-eth', '', "Overhead on Clueweb Dataset,Eth")


    ploter.set_subplot(2,1)
    call_plot('overhead', '../../data', '100-enwiki-ib', '', "Overhead on enwiki Dataset,IB")
    ploter.set_subplot(2,2)
    call_plot('overhead', '../../data', '100-enwiki-eth', '', "Overhead on enwiki Dataset,Eth")
    
    ploter.set_subplot(3,1)
    call_plot('overhead', '../../data', '100-enwiki-bigram-ib', '', "Overhead on enwiki-bigram Dataset,IB")
    ploter.set_subplot(3,2)
    call_plot('overhead', '../../data', '100-gutenberg-ib', '', "Overhead on Gutenberg Dataset,IB")


    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('overhead_all.svg')
   

def draw_bigram():
    # output (2,2) subplots
    ploter.init_subplot(1,1)
    ploter.fig.suptitle("Overhead")
    ploter.fig.set_size_inches(9.25*2*1.5, 5.25*2)

    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-enwiki-bigram-ib', '', "Overhead on enwiki Dataset,IB")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_bigram.svg')

def draw_gutenberg():
    # output (2,2) subplots
    ploter.init_subplot(1,3)
    ploter.fig.suptitle("Overhead")
    ploter.fig.set_size_inches(9.25*2*1.5, 5.25*2)

    ploter.set_subplot(1,1)
    call_plot('overhead', '../../data', '100-gutenberg-ib', '', "Overhead on gugtenberg Dataset,IB")
    ploter.set_subplot(1,2)
    call_plot('overhead', '../../data', '100-gutenberg-ib', '', "Overhead on gugtenberg Dataset,IB")
    ploter.set_subplot(1,3)
    call_plot('overhead', '../../data', '100-gutenberg-ib', '', "Overhead on gugtenberg Dataset,IB")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_gutenberg.svg')



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

#    draw_bigram()

#    draw_gutenberg()
