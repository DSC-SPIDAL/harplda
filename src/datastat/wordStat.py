import sys
import os
import math
import numpy as np
import logging

from docStat import LowDocumentCollection

"""


input:
    source text in low format
    docid\twords.....
    
    dictionary file 
    word\tcnt

"""

class WordStat():
    """
    Statistics on word groups

    """
    def __init__(self):
        pass

    def groupstat(self, collection, splits):
        """
        Word Statistics on document groups in one doc-split result
        input:
            collection: LowDocumentCollection
            splits[]:   LowDocumentCollection[]

        """
        # build a global groupcnt map: <word, groupcnt> 
        groupcnt_map = {}

        splitCnt = len(splits)
        for word in collection.vocabulary:
            cnt = 0
            for split_id in range(splitCnt):
                if word in splits[split_id].vocabulary:
                    cnt += 1
            groupcnt_map[word] = cnt

        # check each doc group
        groupstat = np.zeros((splitCnt, splitCnt))

        for split_id in range(splitCnt):
            for word in splits[split_id].vocabulary:
                groupstat[split_id][groupcnt_map[word] - 1] += 1

        return groupstat

if __name__ == '__main__':
    lowfile = ''
    splitCnt = 0
    partno = 0
    logger_level = ''

    if len(sys.argv) > 1:
        lowfile = sys.argv[1]
        if len(sys.argv) > 2:
            splitCnt = int(sys.argv[2])
            if len(sys.argv) > 3:
                partno = int(sys.argv[3])
                if len(sys.argv) > 4:
                    logger_level = sys.argv[4]

    # logging configure
    import logging.config
    if logger_level:
        logging.basicConfig(filename='wordStat.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    if lowfile == '':
        print("usage: wordStat.py lowfile splitCnt partno partType logger_level")

    else:
        collection = LowDocumentCollection()
        collection.load(lowfile)
        splits_col = collection.load_splits(splitCnt)

        # run stat
        wordStat = wordStat()
        groupstat = wordStat.groupstat(collection, splits)
    
        # print the result
        print(collection)
        for split in splits_col:
            print(split)

        print('group statistics')
        print(groupstat)



