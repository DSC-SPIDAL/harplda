import sys
import os
import math
import logging
import cPickle as pickle

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
    rawdata = []
    rawdataIndex = -1
    documents = []
    vocabulary = {}
    wordcnt = 0
    storage = ''
    cachefile = ''
    fhandle = None
    fcache = None
    useCache = False
    keepInMemory = False

    # constant
    DOC = '.doc'
    DICT = '.dict'
    CACHE = '.pickle'
    MEMCACHE = '.mem'

    def __init__(self):
        self.rawdata = []
        self.rawdataIndex = -1
        self.documents = []
        self.vocabulary = {}
        self.wordcnt = 0
        self.storage = ''
        self.fhandle = None
        self.fcache = None

    def __init__(self, lowfile = ''):
        self.rawdata = []
        self.rawdataIndex = -1
        self.documents = []
        self.vocabulary = {}
        self.storage = lowfile
        self.fhandle = None
        self.fcache = None
        self.useCache = False
        self.keepInMemory = False

        if lowfile:
            lowname = os.path.splitext(os.path.basename(lowfile))[0]
            if os.path.exists(lowname + self.MEMCACHE):
                logger.info('Set keepInMemory=True, %s found', lowname+self.MEMCACHE)
                self.keepInMemory = True

            self.cachefile = lowname + self.CACHE
            if os.path.exists(self.cachefile):
                lowfile = self.cachefile
                self.storage = lowfile
                self.useCache = True
                self.read_lowfile()
            else:
                self.fcache =  open(self.cachefile, 'wb')
                self.useCache = False
                self.read_lowfile()

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
        if not self.fhandle:
            logger.debug('rewind: open new file %s',self.storage)
            self.fhandle = open(self.storage, 'r')
        else:
            logger.debug('rewind: seek 0')
            self.fhandle.seek(0)

        if self.keepInMemory and len(self.rawdata) != 0:
            logger.debug('rewind: use in memory cache')
            self.rawdataIndex = 0

    def __iter__(self):
        return self

    def next(self):
        """
        iterator for the documents
        """
        if self.rawdataIndex >= 0:
            #current in memory cache working
            if self.rawdataIndex == len(self.rawdata):
                raise StopIteration
            else:
                obj = self.rawdata[self.rawdataIndex]
                self.rawdataIndex += 1
                return obj

        if self.useCache:
            try:
                obj = pickle.load(self.fhandle)
            except:
                raise StopIteration
            return obj

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

    def read_lowfile(self):
        self.rewind()
        id = 0
        for doc in self:
            if id % 10000 == 0:
                print '\rloading %d'%id,
                sys.stdout.flush()
            self.read_document(doc)
            id += 1

            # save cache file 
            if not self.useCache:
                pickle.dump(doc, self.fcache, pickle.HIGHEST_PROTOCOL)
                
            # keep in memory
            if self.keepInMemory and self.rawdataIndex < 0:
                self.rawdata.append(doc)

        print '\rloading %d'%id
        sys.stdout.flush()

        if not self.useCache:
            # switch to useCache mode, now
            self.useCache = True
            self.fhandle.close()
            self.fcache.close()
            self.storage = self.cachefile
            self.fhandle = None

    def save(self, basename = ''):
        """
        save statistics to files
        documents to storage.DOC 
        vocabulary to storage.DICT

        """
        if basename == '':
            basename = self.storage 

        docfile = basename + self.DOC
        dictfile = basename + self.DICT
    
        #check file
        if os.path.exists(docfile) and os.path.exists(dictfile):
            logger.info('Skip save existed collection files:%s(%s,%s)', basename,self.DOC, self.DICT)
            return


        logger.info('Save collection to file:%s(%s,%s)', basename,self.DOC, self.DICT)
        # save documents
        docf = open(docfile,'w')
        if docf:
            docf.write('%d\n'%self.wordcnt)
            for docid, _tmp in self.documents:
                docf.write('%s\t%d\n'%(docid, _tmp))

            docf.close()
        else:
            logger.error('open doc file %s failed', docfile)

        # save vocabulary
        dictf = open(dictfile,'w')
        if dictf:
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
        and save to splitxxx/shard_xxx.dict .doc
        """
        logger.info('split_collection splitCnt = %d, splitType = %s', splitCnt, splitType)

        docCollection = []
        for i in range(splitCnt):
            docCollection.append( LowDocumentCollection() )
            split_dir = 'split%d'%splitCnt
            if not os.path.exists(split_dir):
                os.mkdir(split_dir)
            docCollection[i].storage = split_dir + '/shard_%03d'%(i) 

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

        logger.info('split_collection end!')
        return docCollection

    def load_splits(self, splitCnt):
        """
        load statistics from the last split output

        """
        docCollection = []
        for i in range(splitCnt):
            docCollection.append( LowDocumentCollection() )
            storage = 'split%d/shard_%03d'%(splitCnt, i) 
            docCollection[i].load(storage)

        return docCollection


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
    else:
        logging.basicConfig(filename='docStat.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


    if lowfile == '' or splitCnt <= 0:
        print("usage: docStat.py lowfile splitCnt splitType logger_level")

    else:
        collection = load_lowfile(lowfile)

        splits_col = split_collection(collection, splitCnt, splitType)



