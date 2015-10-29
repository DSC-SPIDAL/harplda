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
    call_plot('accuracy_iter', 'data', 'accuracy_ib.clueweb', 'accuracy_iter_ib.clueweb.png', "LDA Trainers Accuracy on Clueweb Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
 
    call_plot('accuracy_runtime', 'data', 'accuracy_ib.clueweb', 'accuracy_runtime_ib.clueweb.png', "LDA Trainers Accuracy on Clueweb Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
 
    call_plot('accuracy_iter','data', 'accuracy_eth.clueweb', 'accuracy_iter_eth.clueweb.png', "LDA Trainers Accuracy on Clueweb Dataset,Ethernet")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
 
    call_plot('accuracy_runtime', 'data', 'accuracy_eth.clueweb', 'accuracy_runtime_eth.clueweb.png', "LDA Trainers Accuracy on Clueweb Dataset,Ethernet")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
 
    
    # enwiki
    call_plot('accuracy_iter','data','accuracy_ib.enwiki','accuracy_iter_ib.enwiki.png',"LDA Trainers Accuracy on enwiki Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
 
    call_plot('accuracy_runtime', 'data','accuracy_ib.enwiki','accuracy_runtime_ib.enwiki.png',"LDA Trainers Accuracy on enwiki Dataset,IB")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
        
    call_plot('accuracy_iter', 'data','accuracy_eth.enwiki','accuracy_iter_eth.enwiki.png',"LDA Trainers Accuracy on enwiki Dataset,Ethernet")
    ploter.init_subplot(1,1)
    ploter.set_subplot(1,1)
  
    call_plot('accuracy_runtime', 'data','accuracy_eth.enwiki','accuracy_runtime_eth.enwiki.png',"LDA Trainers Accuracy on enwiki Dataset,Ethernet")

def draw_all():
    # output (2,2) subplots
    ploter.init_subplot(2,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)

    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', 'data', 'accuracy_ib.clueweb', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', 'data', 'accuracy_ib.clueweb', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
    call_plot('accuracy_iter','data', 'accuracy_eth.clueweb', '', "Clueweb Dataset, 1Gbps Ethernet")
    ploter.set_subplot(2,2)
    call_plot('accuracy_runtime', 'data', 'accuracy_eth.clueweb', '', "Clueweb Dataset, 1Gpbs Ethernet")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_clueweb.png')
    
    # enwiki
    ploter.init_subplot(2,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
 
    ploter.set_subplot(1,1)
    call_plot('accuracy_iter','data','accuracy_ib.enwiki','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', 'data','accuracy_ib.enwiki','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
    call_plot('accuracy_iter', 'data','accuracy_eth.enwiki','',"Enwiki Dataset, 1Gbps Ethernet")
    ploter.set_subplot(2,2)
    call_plot('accuracy_runtime', 'data','accuracy_eth.enwiki','',"Enwiki Dataset, 1Gbps Ethernet")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_enwiki.svg')

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

def draw_overall_30():
    # output (2,2) subplots
    ploter.init_subplot(1,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)

    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', 'data', 'accuracy_30_ib.clueweb', '', "Clueweb Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
#call_plot('accuracy_overalltime', 'data', 'accuracy_30_eth.clueweb', '', "Clueweb Dataset, 1Gpbs Ethernet")
    call_plot('accuracy_overalltime', 'data', 'accuracy_30_ib.clueweb', '', "Clueweb Dataset, 1Gpbs Ethernet")
    
    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_30_clueweb_excutiontime.png')
    
    # enwiki
    ploter.init_subplot(1,2)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)
 
    ploter.set_subplot(1,1)
    call_plot('accuracy_overalltime', 'data','accuracy_30_ib.enwiki','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(1,2)
#call_plot('accuracy_overalltime', 'data','accuracy_30_eth.enwiki','',"Enwiki Dataset, 1Gbps Ethernet")
    call_plot('accuracy_overalltime', 'data','accuracy_30_ib.enwiki','',"Enwiki Dataset, 1Gbps Ethernet")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_30_enwiki_excutiontime.png')

def draw_30_enwiki_all():
    # output (2,2) subplots
    ploter.init_subplot(2,1)
    ploter.fig.suptitle("LDA Trainers Accuracy")
    ploter.fig.set_size_inches(9.25*1.5, 5.25*1.5)


    ploter.set_subplot(1,1)
    call_plot('accuracy_iter', 'data','accuracy_30_ib.enwiki','',"Enwiki Dataset, 16Gbps Infiniband")
    ploter.set_subplot(2,1)
    call_plot('accuracy_runtime', 'data','accuracy_30_ib.enwiki','',"Enwiki Dataset, 16Gbps Infiniband")

    ploter.fig.subplots_adjust(hspace=0.4)
    ploter.savefig('accuracy_enwiki_30.png')



if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

#    draw_single()
#    draw_all()
    draw_enwiki_overall()

#    draw_overall_30()

#    draw_30_enwiki_all()
