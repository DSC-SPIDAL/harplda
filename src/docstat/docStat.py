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
    wordcnt = 0
    storage = ''
    fhandle = ''

    def __init__(self):
        self.documents = []
        self.vocabulary = {}
        self.wordcnt = 0
        self.storage = ''

    def __init__(self, lowfile = ''):
        self.documents = []
        self.vocabulary = {}
        self.storage = lowfile
        if lowfile:
            self.read_lowfile(lowfile)

    def read_document(self, doc= (1,{})):
        """
        read from a document:=(docid, wordmap) object

        """
        self.documents.append((doc[0], 0))
        for word in doc[1]:
            self.wordcnt += 1
            if word in self.vocabulary:
                self.vocabulary[word] += doc[1][word]
            else:
                self.vocabulary[word] = doc[1][word]

    def get_doc_number(self):
        return len(self.documents)

    def get_vocab_size(self):
        return len(self.vocabulary)

    def get_wordcnt(self):
        wordcnt = 0
        for word in self.vocabulary:
            wordcnt += self.vocabulary[word]
        return wordcnt

    def get_lowfile(self):
        return self.storage

    def __str__(self):
        logger.debug('vocabulary=%s', self.vocabulary)
        # return('Collection doc_no:%d, vocabulary size:%d, wordcnt:%d\n'%(self.get_doc_number(), self.get_vocab_size(), self.wordcnt))
        return('Collection doc_no:%d, vocabulary size:%d, wordcnt:%d\n'%(self.get_doc_number(), self.get_vocab_size(), self.get_wordcnt()))

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
            tokens[0] = doc_token[1].strip()
            if tokens[0] != '':
                # last \n
                tokens[-1] = tokens[-1].strip()
                for word in tokens:
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1
    
        return (docid, words)
        # yield (docid, words)

    def read_lowfileX(self, lowfile):
        """
        return : total word count
        """
        id = 0
        cnt = 0
        lf = open(lowfile,'r')
        for line in lf:
            tokens = line.split(' ')
            doc_token = tokens[0].split('\t')
            docid = doc_token[0]
            
            # logger.debug('split to : docid = %s, tokens = %s, %s'%(docid, doc_token,tokens))
            
            if len(doc_token) > 1:
                tokens[0] = doc_token[1].strip()

                if tokens[0] != '':
                    # last \n
                    tokens[-1] = tokens[-1].strip()

                    for word in tokens:
                        cnt += 1
                        if word in self.vocabulary:
                            self.vocabulary[word] += 1
                        else:
                            self.vocabulary[word] = 1
            else:
                logger.debug('doc_token=0, where docid=%s', docid)

#           logger.debug('add document:docid=%s, words=%s'%( docid, words))
            self.documents.append((docid, 0))

            if (id % 10000) == 0 :
                print "\r" + "." * int(id/10000), 
            id += 1

        #close end
        lf.close()
        self.wordcnt = cnt
        return cnt

    def read_lowfile(self, lowfile):
        self.rewind()
        id = 0
        for doc in self:
            if id % 10000 == 0:
                print '\rloading %d'%id,
                sys.stdout.flush()
            self.read_document(doc)
            id += 1

        print '\rloading %d'%id
        sys.stdout.flush()

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
        progress = max(1, int(self.get_doc_number() / 100))
        for doc in self:
#            logger.debug('next doc : %s', doc)
            if splitType == 'SEQ':
                part_no = int(id / part_size)
                docCollection[part_no].read_document(doc)
            elif splitType == 'HASH':
                part_no = int(hash(doc[0]) % splitCnt)
                docCollection[part_no].read_document(doc)
            
            
            if (id % progress) == 0 :
                finish_ratio = int(id * 100 / self.get_doc_number())
                print "\r%s%02d%%"%('='*int(finish_ratio/10), finish_ratio), 
                sys.stdout.flush()
            id += 1

        finish_ratio = int(id * 100 / self.get_doc_number())
        print "\r%s%02d%%"%('='*int(finish_ratio/10), finish_ratio)
        sys.stdout.flush()

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



