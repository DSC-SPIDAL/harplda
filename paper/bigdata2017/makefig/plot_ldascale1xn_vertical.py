#!/usr/bin/
# -*- coding: utf-8 -*-

"""
Plot the 1xn figures in one pdf file for ldascale paper

nytimes 1k, 10k   accuracy_itertime   
pubmed  1k, 10k
enwiki  1k, 10k

accuracy_itertime   1x1
accuracy_iter
throughput_runtime
accuracy_itertime   1x32
scalability

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
        ploter.plot(plotname, '', confset[plotname])
    else:
        ploter.plot(plotname, '', confset['default'])


def draw_ldascale(outname, compact = False):
    nullconf={'default':{'title':''}}

    #
    # conf names
    #
    conffiles={
        'nytimes':{
            '1':'newlda_nytimes_1x1.conf',
            '32':'newlda_nytimes_1x32.conf',
            'scale':'newlda_nytimes_scale.conf'
            },
        'pubmed2m':{
            '1':'newlda_pubmed2m_1x1.conf',
            '32':'newlda_pubmed2m_1x32.conf',
            'scale':'newlda_pubmed2m_scale.conf'
            },
        'enwiki-1k':{
            '1':'newlda_enwiki-1k_1x1.conf',
            '32':'newlda_enwiki-1k_1x32.conf',
            'scale':'newlda_enwiki-1k_scale.conf'
            },
        'enwiki-10k':{
            '1':'newlda_enwiki-10k_1x1.conf',
            '32':'newlda_enwiki-10k_1x32.conf',
            'scale':'newlda_enwiki-10k_scale.conf'
            }
    }

    confxlim={
        'nytimes':[6000,200,6000,500],
        'pubmed2m':[10000, 200, 10000, 2000],
        'enwiki-1k':[100000,200,100000, 6000],
        'enwiki-10k':[100000, 200, 100000, 6000]
    }



    #
    # init
    #
    #plt.rcParams.update({'figure.figsize':(4.5*5,3*4.5)})
    plt.rcParams.update({'figure.figsize':(4.5*5*4/5,4.5*3*3/4)})
    plt.rcParams.update({'axes.titlesize':14})
    plt.rcParams.update({'axes.titleweight':'bold'})
    plt.rcParams.update({'legend.fontsize':14})
    logger.info('set large view')

    ploter.init_subplot(3,4)

    setxlim = True

    #nytimes
    dnames=['nytimes','pubmed2m','enwiki-1k','enwiki-10k']
    for idx, dataset in enumerate(dnames):
        logger.info('idx=%d, dataset=%s', idx, dataset)

        confset = {}
        conf={}
        conf['title']=''
        conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']*10
        conf['lines']=['o-','^-','d-']*10
        conf['nolegend'] = True
        confset['default'] = conf


        ploter.set_subplot(1,idx+1)
        if idx == 0:
            confset['default']['title'] = 'Convergence Speed'
        else:
            #remove title
            #confset['default'].pop('title', None)
            confset['default']['title'] = ''

        confset['default']['sample'] = 10
        confset['default']['dosample'] = 'warp nomad'
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][0]
        call_plot('accuracy_itertime', '', conffiles[dataset]['1'], '',confset) 

        ploter.set_subplot(2,idx+1)
        if idx == 0:
            confset['default']['title'] = 'Convergence Rate'
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][1]
        confset['default']['sample'] = 10
        confset['default']['dosample'] = 'warp nomad'
            
        call_plot('accuracy_iter', '', conffiles[dataset]['1'], '',confset) 

        ploter.set_subplot(3,idx+1)
        if idx == 0:
            confset['default']['title'] = 'Throughput'
        confset['default']['sample'] = 10
        confset['default']['yscale'] = 'log'
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][2]
        call_plot('throughput_runtime', '', conffiles[dataset]['1'], '',confset) 

        #the middle plot
        if idx == 2:
            lgd = ploter.curax.legend(loc='upper center', bbox_to_anchor=(-0.1, -0.15),
                  fancybox=True, shadow=True, ncol=5)

       
    #
    # save
    #
    ploter.fig.savefig(outname + '.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')


    plt.rcParams.update({'figure.figsize':(4.5*5*4/5,4.5*3*2/4)})
    plt.rcParams.update({'axes.titlesize':14})
    plt.rcParams.update({'axes.titleweight':'bold'})
    plt.rcParams.update({'legend.fontsize':14})
    logger.info('set large view')


    ploter.init_subplot(2,4)
    for idx, dataset in enumerate(dnames):
        logger.info('idx=%d, dataset=%s', idx, dataset)

        confset = {}
        conf={}
        conf['title']=''
        conf['colors']=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']*10
        conf['lines']=['o-','^-','d-']*10
        conf['nolegend'] = True
        confset['default'] = conf

        ploter.set_subplot(1, idx+1)
        if idx == 0:
            confset['default']['title'] = 'Convergence Speed'
     
        if setxlim:
            confset['default']['xlim'] = confxlim[dataset][3]
        call_plot('accuracy_itertime', '', conffiles[dataset]['32'], '',confset) 


        ploter.set_subplot(2, idx+1)
        if idx == 0:
            confset['default']['title'] = 'Scalability'
        confset['default']['xlabel'] = 'Threads Number'
     
        call_plot('scalability', '', conffiles[dataset]['scale'], '',confset) 

        #the middle plot
        if idx == 2:
            lgd = ploter.curax.legend(loc='upper center', bbox_to_anchor=(-0.1, -0.15),
                  fancybox=True, shadow=True, ncol=5)


    #
    # save
    #
    ploter.fig.savefig(outname + '-2.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')



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
