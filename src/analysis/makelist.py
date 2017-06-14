#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
make namefile from the experiment results

input format:
    trainer_...._nodexthread_.....

output:
    namefile    trainer node|thread

Usage: 
    makelist.py <resultdir> <outfile name> <thread|node>

"""

import sys,os,re
import datetime
import numpy as np
import logging

logger = logging.getLogger(__name__)

def make_listfile(appdir, outname, outthread):

    outf = open(outname,'w')
    namepat = '([^_]*)_.*_(\d+)x(\d+)_.*'

    for dirpath, dnames, fnames in os.walk(appdir):
        for f in fnames:
            if f.endswith('.likelihood'):
                basename = f[:f.rfind('.')]
                #extract the <trainer, node, thread> from f

                m = re.search(namepat, f)
                if m:
                    trainer = m.group(1)
                    node = m.group(2)
                    thread = m.group(3)
                    if outthread:
                        outf.write('%s %s %s\n'%(basename, trainer, thread)) 
                    else:
                        outf.write('%s %s %s\n'%(basename, trainer, node)) 

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # check the path
    logdir = sys.argv[1]
    outname = sys.argv[2]
    outthread = True if sys.argv[3]=='thread' else False

    make_listfile(logdir, outname, outthread)





