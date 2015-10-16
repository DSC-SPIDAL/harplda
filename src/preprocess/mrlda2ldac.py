#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
USAGE: mrlda2ldac <mrlda file> <output>

convert MrLda input txt file to ldac file
ldac format
    docid word:cnt


"""

import logging
import os.path
import sys

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, outp = sys.argv[1:3]

    mrlda = open(inp, 'r')
    output = open(outp, 'w')
    
    for line in mrlda:
        tokens = line.strip().split(' ')
        doc_token = tokens[0].split('\t')
        docid = doc_token[0]
        
        # logger.debug('split to : docid = %s, tokens = %s, %s'%(docid, doc_token,tokens))
        
        wmap={}
        if len(doc_token) > 1:
            tokens[0] = doc_token[1].strip()
    
            if tokens[0] != '':
                # last \n
                tokens[-1] = tokens[-1].strip()
    
                for word in tokens:
                    if word=='':
                        continue

                    if word in wmap:
                        wmap[word] += 1
                    else:
                        wmap[word] = 1
        
            # output to ldac
            output.write('%d '%len(tokens))
            wordid = sorted([int(x) for x in wmap.keys()])
            for w in wordid:
                output.write("%s:%s "%(w,wmap[str(w)]))
    
            output.write('\n')

        else:
            logger.debug('doc_token=0, where docid=%s', docid)
    


