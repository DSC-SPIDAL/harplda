#!/usr/bin/
# -*- coding: utf-8 -*-

"""
Plot the bigram figures in one pdf file for ldascale paper

bigram 500  10x8

accuracy_itertime   
accuracy_iter   
speedup         ; speedup on convergence speed
overhead_only

legend outside

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
from analysis.fitcurve import draw_eval
from plot_init import PlotConfigure

logger = logging.getLogger(__name__)

# global share ploter
plotconf = PlotConfigure()
ploter = PlotEngine(False)

gridFlag = True
prefix = 'nlda'

def call_plot(plotname, datadir, namefile, figname, confset):
    perfname = PerfName(namefile)
    ploter.init_data(plotconf.dataroot, perfname)
    ploter.curax.grid(gridFlag)
    if plotname in confset:
        ploter.plot(plotname, figname, confset[plotname])
    else:
        ploter.plot(plotname, figname, confset['default'])

def draw_ldascale(outname, compact = False):
    nullconf={'default':{'title':''}}

    #
    # conf names
    #
    conffiles={
        'clueweb30b-5k':{
            '1':'distclueweb_40x16_straggler.conf'
            }
    }


    confxlim={
        'clueweb30b-5k':[20000, 10000, 10000,10000]
    }
    confylim={
        'clueweb30b-5k':[0, 0, 0,(0,1.1)]
    }



    #
    # init
    #
    #dnames=['enwiki-1k','enwiki-10k']
    dnames=['clueweb30b-5k']
    rowCnt = len(dnames)
 
    confset = {}
    conf={}
    conf['title']=''
    conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']*10
    conf['lines']=['o-','^-','d-','+-','x-']*10
    #conf['nolegend'] = True
    confset['default'] = conf

    setxlim = True
    #setxlim = False

    #plt.rcParams.update({'figure.figsize':(4.5*5,3*4.5)})
    plt.rcParams.update({'figure.figsize':(4*2,3*2)})
    plt.rcParams.update({'axes.titlesize':12})
    plt.rcParams.update({'axes.titleweight':'bold'})
    plt.rcParams.update({'legend.fontsize':12})
    logger.info('set large view')

    #set number of subplots
    ploter.init_subplot(2,2)

    for idx, dataset in enumerate(dnames):
        logger.info('idx=%d, dataset=%s', idx, dataset)

        confset['default']['nolegend'] = True
        ploter.set_subplot(1,1)
        #confset['default']['sample'] = 3
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][0]
        confset['default']['title'] = '(a) Convergence Speed'
        call_plot('accuracy_itertime', '', conffiles[dataset]['1'], '',confset) 


        confset['default']['nolegend'] = True
        confset['default']['loc'] = 7
        ploter.set_subplot(1,2)
        confset['default']['sample'] = 10
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][1]
        confset['default']['title'] = '(b) Throughput'
        call_plot('throughput_runtime', '', conffiles[dataset]['1'], '',confset) 

        confset['default'].pop('nolegend',None)
        ploter.set_subplot(2,1)
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][2]
        confset['default']['sample'] = 10
        confset['default']['title'] = '(c) Load Balance'
        call_plot('loadbalance_runtime', '', conffiles[dataset]['1'], '',confset) 


        confset['default']['nolegend'] = True
        ploter.set_subplot(2,2)
        confset['default']['sample'] = 10
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][3]
        
        confset['default']['ylim'] = True
        confset['default']['ylim_l'] = confylim[dataset][3][0]
        confset['default']['ylim_h'] = confylim[dataset][3][1]
        confset['default']['title'] = '(d) Overhead'
        call_plot('overhead_only', '', conffiles[dataset]['1'], '',confset) 
    #
    # save
    #
    #ploter.fig.savefig(outname + '.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.tight_layout()
    ploter.fig.savefig(outname + '.pdf')



def draw_ldascale_single(outname, compact = False):
    nullconf={'default':{'title':''}}

    #
    # conf names
    #
    conffiles={
        'bigram-500':{
            '1':'distbigram.conf',
            }
    }

    confxlim={
        'bigram-500':[10000, 200, 10000,10000]
    }


    #
    # init
    #
    #dnames=['enwiki-1k','enwiki-10k']
    dnames=['bigram-500']
    rowCnt = len(dnames)
 
    confset = {}
    conf={}
    conf['title']=''
    conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']*10
    conf['lines']=['o-','^-','d-']*10
    conf['nolegend'] = True
    confset['default'] = conf

    setxlim = True
    #setxlim = False

    #plt.rcParams.update({'figure.figsize':(4.5*5,3*4.5)})
    plt.rcParams.update({'figure.figsize':(4.5*2.4,4.5*3/4.*2)})
    plt.rcParams.update({'axes.titlesize':12})
    plt.rcParams.update({'axes.titleweight':'bold'})
    plt.rcParams.update({'legend.fontsize':12})
    logger.info('set large view')

    #set number of subplots
    ploter.init_subplot(2,2)

    for idx, dataset in enumerate(dnames):
        logger.info('idx=%d, dataset=%s', idx, dataset)

        ploter.set_subplot(1,1)
        if idx == 0:
            confset['default']['title'] = 'Convergence Speed'
        else:
            #remove title
            #confset['default'].pop('title', None)
            confset['default']['title'] = ''

        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][0]
        call_plot('accuracy_itertime', '', conffiles[dataset]['1'], '',confset) 

        ploter.set_subplot(1,2)
        if idx == 0:
            confset['default']['title'] = 'Convergence Rate' 
        else:
            #remove title
            #confset['default'].pop('title', None)
            confset['default']['title'] = ''

        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][1]
        call_plot('accuracy_iter', '', conffiles[dataset]['1'], '',confset) 


        #the middle plot
        if idx == rowCnt - 1:
            conf['xtick_scale'] = 1e+11
        ploter.set_subplot(2,1)
        if idx == 0:
            confset['default']['title'] = 'Speedup of Time'
        #if setxlim:
        #    confset['default']['xlim'] = confxlim[dataset][3]
        call_plot('speedup', '', conffiles[dataset]['1'], '',confset) 

        #the middle plot
        if idx == rowCnt - 1:
            lgd = ploter.curax.legend(loc='upper left', bbox_to_anchor=(-0.05, -0.15),
                  fancybox=True, shadow=True, ncol=5)
 
        ploter.set_subplot(2,2)
        if idx == 0:
            confset['default']['title'] = 'Overhead'
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][3]
        confset['default']['sample'] = 10
        call_plot('overhead_only', '', conffiles[dataset]['1'], '',confset) 


    #
    # save
    #
    ploter.fig.savefig(outname + '.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #ploter.fig.savefig(outname + '.pdf', bbox_extra_artists=(lgd,))


if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    plotconf.draw_init()
    prefix = sys.argv[1].split('.')[0]

    confset = {}
    if len(sys.argv) > 2:
        if sys.argv[2] == 'TRUE':
            if len(sys.argv) > 3:
                #set xlim by sys.argv[3]
                ploter.use_shortest_x = True
                conf={}
                conf['title']=''
                conf['xlim'] = int(sys.argv[3])
                conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']
                conf['lines']=['o-','^-','d-']*10
                confset['default'] = conf
                conf={}
                conf['title']=''
                conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']
                conf['lines']=['o-','^-','d-']*10
                confset['accuracy_iter'] = conf
 
                conf={}
                conf['title']=''
                conf['xlim'] = int(sys.argv[3])
                conf['colors']=['r','r','b','b','g', 'g','c','c','y','k','r','b','m','g','c','y','k']
                conf['lines']=['-','--']*10
                confset['overhead_all'] = conf
                logger.info('set use_xlim_x as : %s', conf['xlim'])
            else:
                #only shortview
                shortview = (sys.argv[2] == 'True')
                ploter.use_shortest_x = shortview
                logger.info('set use_shortest_x as : %s', shortview)
        else:
            # maybe special to STRAGGLER
            # there are 4 lines with 2 groups
            ploter.use_shortest_x = True
            conf={}
            conf['title']=''
            conf['xlim'] = int(sys.argv[3])
#conf['colors']=['r','salmon','g', 'olivedrab','c','y','k','r','b','m','g','c','y','k']
            conf['colors']=['r','r','g', 'g','c','y','k','r','b','m','g','c','y','k']
            conf['lines']=['o-','o--','d-','d--']*10
            confset['default'] = conf
            conf={}
            conf['title']=''
#           conf['colors']=['r','salmon','g', 'olivedrab','c','y','k','r','b','m','g','c','y','k']
            conf['colors']=['r','r','g', 'g','c','y','k','r','b','m','g','c','y','k']
            conf['lines']=['o-','o--','d-','d--']*10
            confset['accuracy_iter'] = conf
 
            conf={}
            conf['title']=''
            conf['xlim'] = int(sys.argv[3])
            conf['colors']=['r','r','salmon','salmon','g', 'g','olivedrab','olivedrab','y','k','r','b','m','g','c','y','k']
#conf['colors']=['r','r','g', 'g','c','y','k','r','b','m','g','c','y','k']
            conf['lines']=['-','--']*10
            confset['overhead_all'] = conf
            logger.info('set use_xlim_x as : %s', conf['xlim'])

    else:
        conf={}
        conf['title']=''
        conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']*10
        conf['lines']=['o-','^-','d-']*10
 
        confset['default'] = conf
        #plt.rcParams.update({'figure.figsize':(8,6)})
        #plt.rcParams.update({'figure.figsize':(6,3*6./4)})
        #plt.rcParams.update({'figure.figsize':(4.5,3*4.5/4)})
        #logger.info('set large view')


    #draw_ylda()
    #draw_petuum()
    #draw_iteracc()
    #draw_newharp(sys.argv[1], confset)
    draw_ldascale(sys.argv[1])
