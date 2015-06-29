import sys
import os
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
    docid\twords.....

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

    # constant
    DOC = '.doc'
    DICT = '.dict'

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
        #logger.debug('vocabulary=%s', self.vocabulary)
        # return('Collection doc_no:%d, vocabulary size:%d, wordcnt:%d\n'%(self.get_doc_number(), self.get_vocab_size(), self.wordcnt))
        return('Collection doc_no:%d, vocabulary size:%d, wordcnt:%d'%(self.get_doc_number(), self.get_vocab_size(), self.get_wordcnt()))

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

    def save(self):
        """
        save statistics to files
        documents to storage.DOC 
        vocabulary to storage.DICT

        """
        docfile = self.storage + self.DOC
        dictfile = self.storage + self.DICT
        # save documents
        docf = open(docfile,'w')
        if docf:
            docf.write('%d\n'%self.wordcnt)
            logger.info('save documents to doc file %s', docfile)
            for docid, _tmp in self.documents:
                docf.write('%s\t%d\n'%(docid, _tmp))

            docf.close()
        else:
            logger.error('open doc file %s failed', docfile)

        # save vocabulary
        dictf = open(dictfile,'w')
        if dictf:
            logger.info('write to dict file %s', dictfile)
            for w in self.vocabulary:
                dictf.write('%s\t%d\n'%(w, self.vocabulary[w]))

            dictf.close()
        else:
            logger.error('open dict file %s failed', dictfile)

    def load(self, basename):
        """
        load statistics from files
        documents to storage.DOC 
        vocabulary to storage.DICT

        """
        self.storage = basename
        docfile = self.storage + self.DOC
        dictfile = self.storage + self.DICT

        if os.path.exists(docfile) and os.path.exists(dictfile):
            # load documents
            docf = open(docfile,'r')
            logger.info('load documents from doc file %s', docfile)
            self.wordcnt = int(docf.readline().strip())
            for line in docf:
                docid = line.strip().split('\t')
                self.documents.append((docid[0], docid[1]))

            docf.close()

            # load vocabulary
            dictf = open(dictfile,'r')
            logger.info('load from dict file %s', dictfile)
            for line in dictf:
                data = line.strip().split('\t')
                self.vocabulary[data[0]] = int(data[1])

            dictf.close()
        else:
            logger.error('doc file or dict file of %s not exists error', basename)


    def split(self, splitCnt, splitType = 'SEQ'):
        """
        split the collection into splitCnt parts according to the splitType

        input:
        splitType:  
            SEQ     means by sequential split
            HASH    means by hash function on docid
            PART    read in a part-id file, with group id each line

        return:
        splitCnt LowDocumentCollection objects
        """
        
        docCollection = []
        for i in range(splitCnt):
            docCollection.append( LowDocumentCollection() )
            docCollection[i].storage = self.storage + '_%03d'%(i) 

        part_size = math.ceil( float(self.get_doc_number()) / splitCnt)
        
        self.rewind()
        id = 0
        progress = max(1, int(self.get_doc_number() / 100))

        # initialize
        if splitType == 'PART':
            partid_f = open('part-id','r')
            if partid_f == None:
                logger.error('open part-id failed!')
                return None

        for doc in self:
#            logger.debug('next doc : %s', doc)
            if splitType == 'SEQ':
                part_no = int(id / part_size)
                docCollection[part_no].read_document(doc)
            elif splitType == 'HASH':
                part_no = int(hash(doc[0]) % splitCnt)
                docCollection[part_no].read_document(doc)
            elif splitType == 'PART':
                part_no = int (partid_f.readline().strip())
                docCollection[part_no].read_document(doc)

            # print processing status
            if (id % progress) == 0 :
                finish_ratio = int(id * 100 / self.get_doc_number())
                print "\r%s%02d%%"%('='*int(finish_ratio/10), finish_ratio), 
                sys.stdout.flush()
            id += 1

        # print processing status
        finish_ratio = int(id * 100 / self.get_doc_number())
        print "\r%s%02d%%"%('='*int(finish_ratio/10), finish_ratio)
        sys.stdout.flush()

        return docCollection

    def load_splits(self, splitCnt):
        """
        load statistics from the last split output

        """
        docCollection = []
        for i in range(splitCnt):
            docCollection.append( LowDocumentCollection() )
            storage = self.storage + '_%03d'%(i) 
            docCollection[i].load(storage)

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

        collection.save()

        if splitCnt > 0:
            print('begin to split into %d parts\n'%(splitCnt))
            splits_col = collection.split(splitCnt, splitType)
            
            for split in splits_col:
                split.save()
                print(split)



