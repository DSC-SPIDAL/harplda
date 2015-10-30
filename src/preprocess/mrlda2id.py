#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
USAGE: mrlda2id <mrlda file> <wordmap> <output>

convert MrLda input txt file to integer-id txt file
The word-id mapping input by wordmap.txt(gibbslda++)

wordmap format:
    totalcnt
    term id

"""

import logging
import os.path
import sys

def old(mrlda, wordmap, output):
    term_cnt = 0
    wmap = dict()
    for line in wordmap:
        if term_cnt == 0:
            #term_cnt = int(line.strip())
            line.strip()
            continue
        tokens = line.strip().split(' ')
        wmap[tokens[0]] = tokens[1]
    
    for line in mrlda:
        tokens = line.split(' ')
        doc_token = tokens[0].split('\t')
        docid = doc_token[0]
        
        # logger.debug('split to : docid = %s, tokens = %s, %s'%(docid, doc_token,tokens))
        
        output.write('%s\t'%docid)
    
        if len(doc_token) > 1:
            tokens[0] = doc_token[1].strip()
    
            if tokens[0] != '':
                # last \n
                tokens[-1] = tokens[-1].strip()
    
                for word in tokens:
                    if word in wmap:
                        output.write('%s '%wmap[word])
    
        else:
            logger.debug('doc_token=0, where docid=%s', docid)
    
        output.write('\n')


def donew(mrlda, wordmap, output):
    term_cnt = 0
    wmap = dict()
    for line in wordmap:
        if term_cnt == 0:
            #term_cnt = int(line.strip())
            #line.strip()
            term_cnt += 1
            continue
        tokens = line.strip().split(' ')
        wmap[tokens[0]] = tokens[1]
        term_cnt += 1
    
    logger.info('%d words loaded into wordmap', term_cnt-1)


    linecnt = 0
    for line in mrlda:
        tp = line.strip().split('\t')
        if len(tp) > 1:
            docid = tp[0]
            tokens = tp[1].split(' ')
        
            # logger.debug('split to : docid = %s, tokens = %s, %s'%(docid, doc_token,tokens))
            output.write('%s'%docid)
            
            cnt = 0
            for word in tokens:
                if word in wmap:
                    if cnt==0:
                        output.write('\t%s'%wmap[word])
                        cnt +=1
                    else:
                        output.write(' %s'%wmap[word])
                #else:
                #    logger.debug('word in text, but not in new map, word=%s', word)
            output.write('\n')

        else:
            logger.debug('tokens=0, where linecnt=%d, line=%s', linecnt, line)

        linecnt += 1
    logger.info('%s lines processed!', linecnt)

def donewX(mrlda, wordmap, output):
    term_cnt = 0
    wmap = dict()
    for line in wordmap:
        if term_cnt == 0:
            #term_cnt = int(line.strip())
            #line.strip()
            term_cnt += 1
            continue
        tokens = line.strip().split(' ')
        wmap[tokens[0]] = tokens[1]
        term_cnt += 1
    
    logger.info('%d words loaded into wordmap', term_cnt-1)


    linecnt = 0
    for line in mrlda:
        tp = line.strip().split('\t')
        if len(tp) > 1:
            docid = tp[0]
            tokens = tp[1].split(' ')
        
            words = [word for word in tokens if word in wmap]
            wordstr = ' '.join(words)
            output.write('%s\t%s\n'%(docid,wordstr[1:]))

        else:
            logger.debug('tokens=0, where linecnt=%d, line=%s', linecnt, line)

        linecnt += 1
    logger.info('%s lines processed!', linecnt)


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, idp, outp = sys.argv[1:4]

    mrlda = open(inp, 'r',1024*1024)
    wordmap = open(idp, 'r')
    output = open(outp, 'w',1024*1024)
    
    donew(mrlda, wordmap, output)
