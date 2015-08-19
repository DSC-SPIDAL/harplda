import sys
import os
import math
import logging
import cPickle as pickle

from docStat import LowDocumentCollection

"""
Test the assumption:
1. local model size V*K is controllable by sharding the document collection
2. local vocabulary size if much less than the global one, so that communication
    optimization is possible.

input:
    mrlda low format document collection file
    docid\twords.....

usage: 
    docSplit lowfile splitCnt splitType logger_level

"""

logger = logging.getLogger(__name__)

# sub functions to run in shell
def load_lowfile(lowfile):
    collection = LowDocumentCollection(lowfile)
    logger.info("%s"%collection)
    print(collection)
    collection.save(lowfile)
    return collection

def split_collection(collection, splitCnt, splitType):
    print('begin to split into %d parts\n'%(splitCnt))
    splits_col = collection.split(splitCnt, splitType)
    
    for split in splits_col:
        split.save()
        logger.info("%s"%split)
        print(split)

    return splits_col


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    lowfile = ''
    splitCnt = 0
    splitType = 'SEQ'
    logger_level = ''

    if len(sys.argv) > 1:
        lowfile = sys.argv[1]
        if len(sys.argv) > 2:
            splitCnt = int(sys.argv[2])
            if len(sys.argv) > 3:
                splitType = sys.argv[3]
                if len(sys.argv) > 4:
                    logger_level = sys.argv[4]

    import logging.config
    if logger_level:
        logging.basicConfig(filename='docStat.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='docStat.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


    if lowfile == '' or splitCnt <= 1:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)
    else:
        collection = load_lowfile(lowfile)

        if splitCnt > 1:
            splits_col = split_collection(collection, splitCnt, splitType)



