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
    call_plot('accuracy_iter', '../../data', '100-clueweb-ib', 'accuracy_iter_ib.clueweb.svg', "LDA Trainers Accuracy on Clueweb Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_runtime', '../../data', '100-clueweb-ib', 'accuracy_runtime_ib.clueweb.svg', "LDA Trainers Accuracy on Clueweb Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', '100-clueweb-ib', 'accuracy_overalltime_ib.clueweb.svg', "LDA Trainers Accuracy on Clueweb Dataset,IB")
 
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', '../../data', '100-enwiki-ib', 'accuracy_iter_ib.enwiki.svg', "LDA Trainers Accuracy on enwiki Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_runtime', '../../data', '100-enwiki-ib', 'accuracy_runtime_ib.enwiki.svg', "LDA Trainers Accuracy on enwiki Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', '../../data', '100-enwiki-ib', 'accuracy_overalltime_ib.enwiki.svg', "LDA Trainers Accuracy on enwiki Dataset,IB")
 
def draw_all():
    # output (2,2) subplots
    ploter.init_subplot(3,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*3, 5.25*3)

    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', '../../data', '100-clueweb-ib', '', "LDA Trainers Accuracy on Clueweb Dataset,IB")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', '../../data', '100-clueweb-ib', '', "LDA Trainers Accuracy on Clueweb Dataset,IB")
    ploter.set_subplot(3,1)
    call_plot('accuracy_overalltime', '../../data', '100-clueweb-ib', '', "LDA Trainers Accuracy on Clueweb Dataset,IB")

    ploter.set_subplot(1,2)
    call_plot('accuracy_iter', '../../data', '100-clueweb-eth', '', "LDA Trainers Accuracy on Clueweb Dataset,Eth")
    ploter.set_subplot(2,2)
    call_plot('accuracy_runtime', '../../data', '100-clueweb-eth', '', "LDA Trainers Accuracy on Clueweb Dataset,Eth")
    ploter.set_subplot(3,2)
    call_plot('accuracy_overalltime', '../../data', '100-clueweb-eth', '', "LDA Trainers Accuracy on Clueweb Dataset,Eth")
 

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_clueweb.svg')
 

    ploter.init_subplot(3,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*3, 5.25*3)

    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', '../../data', '100-enwiki-eth', '', "LDA Trainers Accuracy on enwiki Dataset,Eth")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', '../../data', '100-enwiki-eth', '', "LDA Trainers Accuracy on enwiki Dataset,Eth")
    ploter.set_subplot(3,1)
    call_plot('accuracy_overalltime', '../../data', '100-enwiki-eth', '', "LDA Trainers Accuracy on enwiki Dataset,Eth")
 

    ploter.set_subplot(1,2)
    call_plot('accuracy_iter', '../../data', '100-enwiki-ib', '', "LDA Trainers Accuracy on enwiki Dataset,IB")
    ploter.set_subplot(2,2)
    call_plot('accuracy_runtime', '../../data', '100-enwiki-ib', '', "LDA Trainers Accuracy on enwiki Dataset,IB")
    ploter.set_subplot(3,2)
    call_plot('accuracy_overalltime', '../../data', '100-enwiki-ib', '', "LDA Trainers Accuracy on enwiki Dataset,IB")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_enwiki.svg')
   

def draw_bigram():
    # output (2,2) subplots
    ploter.init_subplot(1,3)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*2*1.5, 5.25*2)

    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', '../../data', '100-enwiki-bigram-ib', '', "LDA Trainers Accuracy on enwiki Dataset,IB")
    ploter.set_subplot(1,2)
    call_plot('accuracy_runtime', '../../data', '100-enwiki-bigram-ib', '', "LDA Trainers Accuracy on enwiki Dataset,IB")
    ploter.set_subplot(1,3)
    call_plot('accuracy_overalltime', '../../data', '100-enwiki-bigram-ib', '', "LDA Trainers Accuracy on enwiki Dataset,IB")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_bigram.svg')

def draw_gutenberg():
    # output (2,2) subplots
    ploter.init_subplot(1,3)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*2*1.5, 5.25*2)

    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', '../../data', '100-gutenberg-ib', '', "LDA Trainers Accuracy on gugtenberg Dataset,IB")
    ploter.set_subplot(1,2)
    call_plot('accuracy_runtime', '../../data', '100-gutenberg-ib', '', "LDA Trainers Accuracy on gugtenberg Dataset,IB")
    ploter.set_subplot(1,3)
    call_plot('accuracy_overalltime', '../../data', '100-gutenberg-ib', '', "LDA Trainers Accuracy on gugtenberg Dataset,IB")
    
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

#    draw_single()
    draw_all()

    draw_bigram()

    draw_gutenberg()
