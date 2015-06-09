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


def progress(width, percent):
    print "%s %d%%\r" % (('%%-%ds' % width) % (width * percent / 100 * "="), percent),
    if percent >= 100:
        print
        sys.stdout.flush()

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
        id = 0
        lf = open(lowfile,'r')
        for line in lf:
#            index =  line.find('\t')
#            docid = line[:index]
#            tokens = line[index:].split()
            tokens = line.split(' ')
            doc_token = tokens[0].split('\t')
            docid = doc_token[0]
            
            # logger.debug('split to : docid = %s, tokens = %s, %s'%(docid, doc_token,tokens))
            
            if len(doc_token) > 1:
                tokens[0] = doc_token[1]
    
                #logger.debug('split to : docid = %s, tokens = %s'%(docid, tokens[:3]))
    
                for word in tokens:
                    if word in self.vocabulary:
                        self.vocabulary[word] += 1
                    else:
                        self.vocabulary[word] = 1
        

#           logger.debug('add document:docid=%s, words=%s'%( docid, words))
            self.documents.append((docid, 0))

            if (id % 10000) == 0 :
                print "\r" + "." * int(id/10000), 
            id += 1

        #close end
        lf.close()

    def read_document(self, doc= (1,{})):
        """
        read from a document:=(docid, wordmap) object

        """
        self.documents.append((doc[0], 0))
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
        #if self.fhandle == '':
        #self.fhandle = open(self.storage, 'r')
        
        line = self.fhandle.readline()
        #logger.debug('read line as %s', line)
        if line == '':
            raise StopIteration
            #yield none

        tokens = line.split(' ')
        doc_token = tokens[0].split('\t')
        docid = doc_token[0]
        
        # logger.debug('split to : docid = %s, tokens = %s, %s'%(docid, doc_token,tokens))
        
        words = {}
        if len(doc_token) > 1:
            tokens[0] = doc_token[1]
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
        progress = int(self.get_doc_number() / 100)
        for doc in self:
            logger.debug('next doc : %s', doc)
            if splitType == 'SEQ':
                part_no = int(id / part_size)
                docCollection[part_no].read_document(doc)
            elif splitType == 'HASH':
                part_no = int(hash(doc[0]) % splitCnt)
                docCollection[part_no].read_document(doc)
            
            
            if (id % progress) == 0 :
                finish_ratio = int(id * 100 / self.get_doc_number())
                print "\r%s%02d%%"%('='*int(finish_ratio/10), finish_ratio), 
            id += 1

        finish_ratio = int(id * 100 / self.get_doc_number())
        print "\r%s%02d%%"%('='*int(finish_ratio/10), finish_ratio)

        return docCollection


def test_main(lowfile, test_cnt):
    for i in range(test_cnt):
        collection = LowDocumentCollection(lowfile)
        print(collection)

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



