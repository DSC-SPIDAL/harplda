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
    call_plot('comm_breakdown', 'data', 'vsylda-accuracy.100-clueweb-ib', 'comm_breakdown_ib.clueweb.svg', "Comm/Computation time breakdown on Clueweb Dataset,IB")

    ploter.init_subplot(1,1)
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
    ploter.set_subplot(1,1)
    call_plot('comm_breakdown','data', 'vsylda-accuracy.100-clueweb-eth', 'comm_breakdown_eth.clueweb.svg', "Comm/Computation time breakdown on Clueweb Dataset,Ethernet")

    # enwiki
    ploter.init_subplot(1,1)
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
    ploter.set_subplot(1,1)
    call_plot('comm_breakdown', 'data', 'vsylda-accuracy.100-enwiki-ib', 'comm_breakdown_ib.enwiki.svg', "Comm/Computation time breakdown on enwiki Dataset,IB")

    ploter.init_subplot(1,1)
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
    ploter.set_subplot(1,1)
    call_plot('comm_breakdown','data', 'vsylda-accuracy.100-enwiki-eth', 'comm_breakdown_eth.enwiki.svg', "Comm/Computation time breakdown on enwiki Dataset,Ethernet")


def draw_all():
    # output (2,2) subplots
    ploter.init_subplot(2,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)

    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', 'data', 'vsylda-accuracy.100-clueweb-ib', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', 'data', 'vsylda-accuracy.100-clueweb-ib', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
    call_plot('accuracy_iter','data', 'vsylda-accuracy.100-clueweb-eth', '', "Clueweb Dataset, 1Gbps Ethernet")
    ploter.set_subplot(2,2)
    call_plot('accuracy_runtime', 'data', 'vsylda-accuracy.100-clueweb-eth', '', "Clueweb Dataset, 1Gpbs Ethernet")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_clueweb.svg')
    
    # enwiki
    ploter.init_subplot(2,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
 
    ploter.set_subplot(1,1)
    call_plot('accuracy_iter','data','vsylda-accuracy.100-enwiki-ib','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', 'data','vsylda-accuracy.100-enwiki-ib','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
    call_plot('accuracy_iter', 'data','vsylda-accuracy.100-enwiki-eth','',"Enwiki Dataset, 1Gbps Ethernet")
    ploter.set_subplot(2,2)
    call_plot('accuracy_runtime', 'data','vsylda-accuracy.100-enwiki-eth','',"Enwiki Dataset, 1Gbps Ethernet")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_enwiki.svg')

def draw_enwiki_overall():
    # output (2,2) subplots
    ploter.init_subplot(1,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)

    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', 'data', 'vsylda-accuracy.100-clueweb-ib', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
    call_plot('accuracy_overalltime', 'data', 'vsylda-accuracy.100-clueweb-eth', '', "Clueweb Dataset, 1Gpbs Ethernet")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_clueweb_excutiontime.svg')
    
    # enwiki
    ploter.init_subplot(1,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
 
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', 'data','vsylda-accuracy.100-enwiki-ib','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
    call_plot('accuracy_overalltime', 'data','vsylda-accuracy.100-enwiki-eth','',"Enwiki Dataset, 1Gbps Ethernet")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_enwiki_excutiontime.svg')

def draw_overall_30():
    # output (2,2) subplots
    ploter.init_subplot(1,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)

    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', 'data', 'vsylda-accuracy.30-clueweb-ib', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
#call_plot('accuracy_overalltime', 'data', 'accuracy_30_eth.clueweb', '', "Clueweb Dataset, 1Gpbs Ethernet")
    call_plot('accuracy_overalltime', 'data', 'vsylda-accuracy.30-clueweb-ib', '', "Clueweb Dataset, 1Gpbs Ethernet")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_30_clueweb_excutiontime.svg')
    
    # enwiki
    ploter.init_subplot(1,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
 
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', 'data','vsylda-accuracy.30-enwiki-ib','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
#call_plot('accuracy_overalltime', 'data','accuracy_30_eth.enwiki','',"Enwiki Dataset, 1Gbps Ethernet")
    call_plot('accuracy_overalltime', 'data','vsylda-accuracy.30-enwiki-ib','',"Enwiki Dataset, 1Gbps Ethernet")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_30_enwiki_excutiontime.svg')

def draw_30_enwiki_all():
    # output (2,2) subplots
    ploter.init_subplot(2,1)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)


    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', 'data','vsylda-accuracy.30-enwiki-ib','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', 'data','vsylda-accuracy.30-enwiki-ib','',"Enwiki Dataset, 16Gbps Infiniband")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_enwiki_30.svg')



if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    draw_single()
