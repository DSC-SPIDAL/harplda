import sys
import os
import math
import logging

from docStat import LowDocumentCollection

"""
find a proper partition function for words (also calls model partition)

input:
    source text in low format
    docid\twords.....
    
    dictionary file 
    word\tcnt

"""

class WordPartition():
    """

    """
    partmap = {}
    partno = 0

    def __init__(self, partno):
        self.partno = partno
        self.partmap = {}

    def partition(self, word):
        """
        input: word
        return: partiton id
        """
        return self.partmap[word]

    def part_by_hash(self, dictfile):
        """
        Partition on data, simple hash
        
        input:
        dictfile

        """
        # load dictionary
        dictf = open(dictfile, 'r')
        wordlist = []
        totalCnt = 0
        for line in dictf:
            data = line.strip().split('\t')
            wordlist.append( ( data[0], int(data[1])) )

            totalCnt += int(data[1])

        for id in xrange(len(wordlist)):
            self.partmap[wordlist[id][0]] = int(hash(wordlist[id]) % self.partno)
 
    def part_by_freq(self, dictfile):
        """
        Partition on power-law data, group the words by their frequencies
        
        input:
        dictfile, a reversed sorted dictionary by freq

        """
        # load dictionary
        dictf = open(dictfile, 'r')
        wordlist = []
        totalCnt = 0
        for line in dictf:
            data = line.strip().split('\t')
            wordlist.append( ( data[0], int(data[1])) )

            totalCnt += int(data[1])

        # sort by freq
        wordlist = sorted(wordlist, key = lambda x: x[1], reverse = True)

        # build partition group
        blockCnt = int (totalCnt / self.partno)
        cnt = 0
        blockid = 0
        for id in xrange(len(wordlist)):
            #if cnt + cntlist[id] > blockCnt:
            if cnt < blockCnt or blockid == blockCnt - 1:
                self.partmap[wordlist[id][0]] = blockid
                cnt += wordlist[id][1]
            else:
                # change to a new block
                blockid += 1
                cnt = wordlist[id][1]
                self.partmap[wordlist[id][0]] = blockid

def test_partition():
    pass



if __name__ == '__main__':
    """ usage: wordpartition lowfile splitCnt splitType logger_level

    """
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
        logging.basicConfig(filename='wordPartition.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='wordPartition.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if lowfile == '':
        print("usage: wordPartition.py lowfile splitCnt partno partType logger_level")

    else:
        collection = LowDocumentCollection()
        collection.load(lowfile)
        print(collection)

        # test partition
        wordPartition = WordPartition(partno)
    
        splitType = 'HASH'
        if splitType == 'HASH':
            wordPartition.part_by_hash(lowfile + '.dict')
        else:
            wordPartition.part_by_freq(lowfile + '.dict')

        # test each splits, output it's partition count
        if splitCnt > 0:
            splits_col = collection.load_splits(splitCnt)
            
            for split in splits_col:
                print(split)

                partmap = {}
                for w in split.vocabulary:
                    partid = wordPartition.partition(w)
                    if partid in partmap:
                        partmap[partid] += 1
                    else:
                        partmap[partid] = 1

                print('part count = %d'%len(partmap))

