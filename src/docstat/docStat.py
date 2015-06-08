import sys
import math
import logging

"""
statistics on word distribution of the document collection

test the assumption:
1. local model size V*K is controllable by sharding the document collection
2. local vocabulary size if much less than the global one, so that communication
    optimization is possible.

input:
low format document collection file

"""

logger = logging.getLogger(__name__)

class LowDocumentCollection():
    documents = []
    vocabulary = {}
    storage = ''
    fhandle = ''

    def __init__(self):
        self.documents = []
        self.vocabulary = {}
        self.storage = ''

    def __init__(self, lowfile = ''):
        self.documents = []
        self.vocabulary = {}
        self.storage = lowfile
        if lowfile:
            self.read_lowfile(lowfile)

    def read_lowfile(self, lowfile):
        lf = open(lowfile,'r')
        for line in lf:
            index =  line.find('\t')
            docid = line[:index]
            tokens = line[index:].split()

#            logger.debug('split to : docid = %s, tokens = %s'%(docid, tokens[:3]))

            words = {}
            for word in tokens:
#it's too memeory hungry for this simple implemntation
#                if word in words:
#                    words[word] += 1
#                else:
#                    words[word] = 1

                if word in self.vocabulary:
                    self.vocabulary[word] += 1
                else:
                    self.vocabulary[word] = 1
    

#           logger.debug('add document:docid=%s, words=%s'%( docid, words))
            self.documents.append((docid, words))

    def read_document(self, doc= (1,{})):
        """
        read from a document:=(docid, wordmap) object

        """
        self.documents.append((doc[0], {}))
        for word in doc[1]:
            if word in self.vocabulary:
                self.vocabulary[word] += 1
            else:
                self.vocabulary[word] = 1

    def get_doc_number(self):
        return len(self.documents)

    def get_vocab_size(self):
        return len(self.vocabulary)

    def get_lowfile(self):
        return self.storage

    def __str__(self):
        return('Collection doc_no:%d, vocabulary size:%d\n'%(self.get_doc_number(), self.get_vocab_size()))

    def rewind(self):
        if self.fhandle == '':
            self.fhandle = open(self.storage, 'r')
        else:
            self.fhandle.seek(0)

    def __iter__(self):
        return self

    def next(self):
        """
        iterator for the documents
        """
        if self.fhandle == '':
            self.fhandle = open(self.storage, 'r')
        
        line = self.fhandle.readline()
        logger.debug('read line as %s', line)
        if line == '':
            raise StopIteration
            #yield none

        index =  line.find('\t')
        docid = line[:index]
        tokens = line[index:].split()

        words = {}
        for word in tokens:
            if word in words:
                words[word] += 1
            else:
                words[word] = 1

        return (docid, words)
        # yield (docid, words)

    def split(self, splitCnt, splitType = 'SEQ'):
        """
        split the collection into splitCnt parts according to the splitType

        input:
        splitType:  
            SEQ     means by sequential split
            HASH    means by hash function on docid

        return:
        splitCnt LowDocumentCollection objects
        """
        
        docCollection = []
        for i in range(splitCnt):
            docCollection.append( LowDocumentCollection() )
            docCollection[i].sotrage = self.storage + '_%03d'%(i) 

        part_size = math.ceil( float(self.get_doc_number()) / splitCnt)
        
        self.rewind()
        id = 0
        for doc in self:
            logger.debug('next doc : %s', doc)
            if splitType == 'SEQ':
                part_no = int(id / part_size)
                docCollection[part_no].read_document(doc)
                id += 1

            elif splitType == 'HASH':
                    part_no = int(hash(doc[0]) % splitCnt)
                    docCollection[part_no].read_document(doc)

        return docCollection

if __name__ == '__main__':
    """ usage: docStat.py lowfile splitCnt splitType logger_level

    """
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

    # logging configure
    import logging.config
    if logger_level:
        logging.basicConfig(filename='docStat.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    if lowfile == '':
        print("usage: docStat.py lowfile splitCnt splitType logger_level")

    else:
        collection = LowDocumentCollection(lowfile)
        
        print(collection)

        if splitCnt > 0:
            print('begin to split into %d parts\n'%(splitCnt))
            splits_col = collection.split(splitCnt, splitType)
            
            for split in splits_col:
                print(split)



