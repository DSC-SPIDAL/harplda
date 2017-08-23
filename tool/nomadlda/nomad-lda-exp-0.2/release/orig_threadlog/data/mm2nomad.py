#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Convert mm file to PETsc format

Simple Matrix Market Format:
    #dataset-[train,test].mm
    rowid   colid   val

PETSc format:
    ID                  ; 1211216 or 1015
    nrows, ncols, nnz   ; int, int, long/long long
    total_nnz_rows[nrows]    ; int, cumsum of items count for each row
    col_index[nnz]      ; int, colid for each data point
    data[nnz]           ; double

Usage:
    usage: mm2petsc -type [train_filename] [test_filename] [output path] [train_rowcolonly]
        -type: 
            nomad    ; original nomad converter
            big      ; deal with hugh mm file, nnz > 4G

"""
import sys,os
from scipy import *
from scipy.sparse import *
import random
import numpy as np
import struct
import numpy.random
import logging

logger = logging.getLogger(__name__)

chunk_rowsize = 1000000
#chunk_rowsize = 10000000

def nomad_convert(train_filename, test_filename, output_path='.'):
    random.seed(12345)
    
    #output_path = sys.argv[3]
    user_ids = set()
    item_ids = set()
    
    # index users and items
    
    for index, line in enumerate(open(train_filename)):
    
        if index % 1000000 == 0:
            print "1st pass training:", index
        
        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()
        user_ids.add(tokens[0])
        item_ids.add(tokens[1])
    
        #if index > 200:
        #    break
    nnz = index + 1 
    
    for index, line in enumerate(open(test_filename)):
    
        if index % 1000000 == 0:
            print "1st pass test:", index
        
        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()
    
        user_ids.add(tokens[0])
        item_ids.add(tokens[1])
    
        #if index > 200:
        #    break
    
    
    
    user_id_list = list(user_ids)
    item_id_list = list(item_ids)
    random.shuffle(user_id_list)
    random.shuffle(item_id_list)
    
    user_indexer = {key:value for value, key in enumerate(user_id_list)}
    item_indexer = {key:value for value, key in enumerate(item_id_list)}
    
    
    # now parse the data
    train_user_indices = list()
    train_item_indices = list()
    train_values = list()
    
    for index, line in enumerate(open(train_filename)):
    
        if index % 1000000 == 0:
            print "2nd pass training:", index
        
        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()
    
        train_user_indices.append(user_indexer[tokens[0]])
        train_item_indices.append(item_indexer[tokens[1]])
        train_values.append(float(tokens[2]))
    
        #if index > 200:
        #    break
    
    
    #print user_indices
    #print item_indices
    #print values
    
    print "form training csr matrix"
    train_mat = csr_matrix( (train_values,(train_user_indices,train_item_indices)), shape=(len(user_indexer),len(item_indexer)) )
    
    print "calculate size of rows"
    train_row_sizes = train_mat.indptr[1:] - train_mat.indptr[:-1]
    
    #print user_indexer
    #print len(user_indexer)
    #print train_row_sizes
    
    #print train_mat
    #print mat.indices
    #print mat.data
    
    print "write train binary file"
    ofile = open(output_path + "/train.dat", "wb")
    ofile.write(struct.pack("=iiiq", 1015, len(user_indexer), len(item_indexer), train_mat.getnnz()))
    ofile.write(struct.pack("=%si" % len(train_row_sizes), *train_row_sizes))
    ofile.write(struct.pack("=%si" % len(train_mat.indices), *train_mat.indices))
    ofile.write(struct.pack("=%sd" % len(train_mat.data), *train_mat.data))
    ofile.close()
    
    logger.info('nnz = %d, mat nnz=%d, row_sizes=%d, indices=%d, datasize=%d', nnz, train_mat.getnnz(),
            len(train_row_sizes), len(train_mat.indices), len(train_mat.data))
    
    #debug only
    #logger.info('users=%s, items=%s, train_valuse=%s', train_user_indices, train_item_indices,train_values)
    #for index in range(nnz / chunk_rowsize + 1):
    #    startpos = index * chunk_rowsize
    #    logger.info('check chunk %s', index)
    #    logger.info('mat.indices=%s', train_mat.indices[startpos:startpos+20])
    #    logger.info('mat.data=%s', train_mat.data[startpos:startpos+20])
    #
    #logger.info('rowsize=%s', train_row_sizes)
    #logger.info('indices=%s', train_mat.indices)

    ##########################################################################
    test_user_indices = list()
    test_item_indices = list()
    test_values = list()
    
    for index, line in enumerate(open(test_filename)):
    
        if index % 1000000 == 0:
            print "2nd pass test:", index
        
        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()
    
        test_user_indices.append(user_indexer[tokens[0]])
        test_item_indices.append(item_indexer[tokens[1]])
        test_values.append(float(tokens[2]))
    
        #if index > 200:
        #    break
    
    
    #print user_indices
    #print item_indices
    #print values
    
    print "form test csr matrix"
    test_mat = csr_matrix( (test_values,(test_user_indices,test_item_indices)), shape=(len(user_indexer),len(item_indexer)) )
    
    print "calculate size of rows"
    test_row_sizes = test_mat.indptr[1:] - test_mat.indptr[:-1]
    
    #print row_sizes
    #print mat.indices
    #print mat.data
    
    print "write test binary file"
    ofile = open(output_path + "/test.dat", "wb")
    #ofile.write(struct.pack("=iiii", 1211216, len(user_indexer), len(item_indexer), test_mat.getnnz()))
    ofile.write(struct.pack("=iiiq", 1015, len(user_indexer), len(item_indexer), test_mat.getnnz()))
    ofile.write(struct.pack("=%si" % len(test_row_sizes), *test_row_sizes))
    ofile.write(struct.pack("=%si" % len(test_mat.indices), *test_mat.indices))
    ofile.write(struct.pack("=%sd" % len(test_mat.data), *test_mat.data))
    ofile.close()
    
    print "write user index mappings"
    ofile = open(output_path + "/user_ids.txt", "w")
    for user_id in user_id_list:
        ofile.write("%s\n" % user_id)
    ofile.close()
    
    print "write item index mappings"
    ofile = open(output_path + "/item_ids.txt", "w")
    for item_id in item_id_list:
        ofile.write("%s\n" % item_id)
    ofile.close()

def hotfix_trainids(train_filename):
    user_ids = set()
    item_ids = set()
    
    # index users and items
    for index, line in enumerate(open(train_filename)):
    
        if index % 1000000 == 0:
            print "1st pass training:", index
        
        tokens = line.split()
        user_ids.add(tokens[0])
        item_ids.add(tokens[1])

    user_id_list = list(user_ids)
    item_id_list = list(item_ids)
 
    print "write user index mappings"
    ofile = open(output_path + "/train_user_ids.txt", "w")
    for user_id in user_id_list:
        ofile.write("%s\n" % user_id)
    ofile.close()
    
    print "write item index mappings"
    ofile = open(output_path + "/train_item_ids.txt", "w")
    for item_id in item_id_list:
        ofile.write("%s\n" % item_id)
    ofile.close()



def hotfix_testset(train_filename, test_filename, output_path = '.'):
    """
        filter out all rows and cols not in train_filename
        based on the converted files with all the rows and cols, including both train and test
    """
    # first, let's read in old ids with all rows and cols
    random.seed(12345)

    user_id_list = []
    item_id_list = []
    print "read user index mappings"
    ofile = open(output_path + "/user_ids.txt", "r")
    for user_id in ofile:
        user_id_list.append(user_id.strip())
    ofile.close()
    
    print "read item index mappings"
    ofile = open(output_path + "/item_ids.txt", "r")
    for item_id in ofile:
        item_id_list.append(item_id.strip())
    ofile.close()

    random.shuffle(user_id_list)
    random.shuffle(item_id_list)
    
    user_indexer = {key:value for value, key in enumerate(user_id_list)}
    item_indexer = {key:value for value, key in enumerate(item_id_list)}

    # rebuild the real id list, with only the rows and cols in train data
    user_ids = set()
    item_ids = set()
 
    print "read user index mappings"
    ofile = open(output_path + "/train_user_ids.txt", "r")
    for user_id in ofile:
        user_ids.add(user_id.strip())
    ofile.close()
    
    print "read item index mappings"
    ofile = open(output_path + "/train_item_ids.txt", "r")
    for item_id in ofile:
        item_ids.add(item_id.strip())
    ofile.close()

    # build the test data only
    if not os.path.exists(output_path + '/test_fix.dat'):
        logger.info('convert test set')
        test_user_indices = list()
        test_item_indices = list()
        test_values = list()

        skipcnt = 0
        for index, line in enumerate(open(test_filename)):
        
            if index % 1000000 == 0:
                print "2nd pass test:", index
            
            #tokens = line.split(SPLIT_SEP)
            tokens = line.split()
        
            if tokens[0] in user_ids and tokens[1] in item_ids:
                test_user_indices.append(user_indexer[tokens[0]])
                test_item_indices.append(item_indexer[tokens[1]])
                test_values.append(float(tokens[2]))
            else:
                skipcnt += 1
 
            #if index > 200:
            #    break
        
        print "skipcnt = %d"%skipcnt
        #print user_indices
        #print item_indices
        #print values
        
        print "form test csr matrix"
        test_mat = csr_matrix( (test_values,(test_user_indices,test_item_indices)), shape=(len(user_indexer),len(item_indexer)) )
        
        print "calculate size of rows"
        test_row_sizes = test_mat.indptr[1:] - test_mat.indptr[:-1]
        
        #print row_sizes
        #print mat.indices
        #print mat.data
        
        print "write test binary file"
        ofile = open(output_path + "/test_fix.dat", "wb")
        ofile.write(struct.pack("=iiiq", 1015, len(user_indexer), len(item_indexer), test_mat.getnnz()))
        ofile.write(struct.pack("=%si" % len(test_row_sizes), *test_row_sizes))
        ofile.write(struct.pack("=%si" % len(test_mat.indices), *test_mat.indices))
        ofile.write(struct.pack("=%sd" % len(test_mat.data), *test_mat.data))
        ofile.close()


 
def big_convert(train_filename, test_filename, output_path = '.', train_rowcolonly = True):
    """
        sparse matrix in scipy does not support large data which can
        not fit in memory.

        here use out memory sort to do the same as crs_matrix() call

    """
    print "start convert: output_path %s, train_rowcolonly %s"%(output_path, train_rowcolonly)

    user_cnt, item_cnt, nnz = 0, 0, 0

    if not os.path.exists(output_path + '/train.id'):
        # bulid the id mapping
        random.seed(12345)

        user_ids = set()
        item_ids = set()
        
        # index users and items
        for index, line in enumerate(open(train_filename)):
        
            if index % 1000000 == 0:
                print "1st pass training:", index
            
            tokens = line.split()
            user_ids.add(tokens[0])
            item_ids.add(tokens[1])

        nnz = index + 1

        if not train_rowcolonly:
            # otherwise, get the row/col ids in the testdat
            for index, line in enumerate(open(test_filename)):
                if index % 1000000 == 0:
                    print "1st pass test:", index
                #tokens = line.split(SPLIT_SEP)
                tokens = line.split()
                user_ids.add(tokens[0])
                item_ids.add(tokens[1])

        user_id_list = list(user_ids)
        item_id_list = list(item_ids)
        random.shuffle(user_id_list)
        random.shuffle(item_id_list)
        
        user_indexer = {key:value for value, key in enumerate(user_id_list)}
        item_indexer = {key:value for value, key in enumerate(item_id_list)}
        print "write user index mappings"
        ofile = open(output_path + "/user_ids.txt", "w")
        for user_id in user_id_list:
            ofile.write("%s\n" % user_id)
        ofile.close()
        
        print "write item index mappings"
        ofile = open(output_path + "/item_ids.txt", "w")
        for item_id in item_id_list:
            ofile.write("%s\n" % item_id)
        ofile.close()

        # rewrite with shuffled id
        id_trainf = open(output_path +'/train.id', 'w', 1024*1024)
        for index, line in enumerate(open(train_filename)):
            if index % 1000000 == 0:
                print "2st pass training:", index
            tokens = line.split()
            id_trainf.write('%d %d %s\n'%(user_indexer[tokens[0]],item_indexer[tokens[1]], tokens[2]))

        id_trainf.close()

        # write status
        statusf = open(output_path + '/train.status','w')
        statusf.write('%d %d %d\n'%(len(user_indexer), len(item_indexer), nnz))
        statusf.close()
        user_cnt = len(user_indexer)
        item_cnt = len(item_indexer)
    else:
        #'.id' exists already, read statusf
        statusf = open(output_path + '/train.status')
        items = statusf.readline().strip().split()
        user_cnt = int(items[0])
        item_cnt = int(items[1])
        nnz = int(items[2])
        statusf.close()
    logger.info('user_cnt=%d, item_ctn=%d, nnz=%d', user_cnt, item_cnt, nnz)
        

    if not os.path.exists(output_path + '/train.sort'):
        logger.info('start sorting....')
        os.system('sort -n -k1,1 -k2,2 -T . --parallel=8 -o %s %s'%(output_path + '/train.sort', output_path +'/train.id'))
        logger.info('end sorting.')

    # now parse the data
    train_item_indices = list()
    train_values = list()

    print "write train binary file"
    ofile = open(output_path + "/train.dat", "wb")
    ofile.write(struct.pack("=iiiq", 1015, user_cnt, item_cnt, nnz))

    indice_pos = 20 + user_cnt *4 
    data_pos =  20 + (user_cnt + nnz)*4 

    row_sizes = [0 for i in range(user_cnt)]
    index = 0

    for index, line in enumerate(open(output_path + '/train.sort')):
    
        if index % 1000000 == 0:
            print "3nd pass training:", index
        
        if index and index % chunk_rowsize == 0:
            #write this chunk
            #logger.info('items=%s, train_valuse=%s', train_item_indices,train_values)
            logger.info('write chunk %d, indices size=%d, data size=%d', index / chunk_rowsize, len(train_item_indices), len(train_values))
    
            #indice pos
            ofile.seek(indice_pos,0)
            ofile.write(struct.pack("=%si" % len(train_item_indices), *train_item_indices))
            indice_pos += len(train_item_indices)*4

            # data pos
            ofile.seek(data_pos, 0)
            ofile.write(struct.pack("=%sd" % len(train_values), *train_values))
            data_pos += len(train_values) * 8
            logger.info('mat.indices=%s', train_item_indices[:20])
            logger.info('mat.data=%s', train_values[:20])

            # release the big memeory
            del train_item_indices
            del train_values

            #reset the data structure
            train_item_indices = list()
            train_values = list()


        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()

        train_item_indices.append(int(tokens[1]))
        train_values.append(float(tokens[2]))
        row_sizes[int(tokens[0])] += 1


    #write the last block
    if index:
        #write this chunk
        #logger.info('items=%s, train_valuse=%s', train_item_indices,train_values)
        logger.info('write last chunk=%d, indices size=%d, data size=%d', index / chunk_rowsize, len(train_item_indices), len(train_values))
    
        #indice pos
        ofile.seek(indice_pos,0)
        ofile.write(struct.pack("=%si" % len(train_item_indices), *train_item_indices))

        # data pos
        ofile.seek(data_pos,0)
        ofile.write(struct.pack("=%sd" % len(train_values), *train_values))
        logger.info('mat.indices=%s', train_item_indices[:20])
        logger.info('mat.data=%s', train_values[:20])
 
    #logger.info('rowsize=%s', row_sizes)

    #write rowsize and indices
    ofile.seek(20, 0)
    ofile.write(struct.pack("=%si" % len(row_sizes), *row_sizes))
 
    ofile.close()
    
    #############################################################################
    if not os.path.exists(output_path + '/test.dat'):
        logger.info('convert test set')
        test_user_indices = list()
        test_item_indices = list()
        test_values = list()
        

        rowids_dict = user_indexer.keys()
        colids_dict = item_indexer.keys()
        skipcnt = 0
        for index, line in enumerate(open(test_filename)):
        
            if index % 1000000 == 0:
                print "2nd pass test:", index
            
            #tokens = line.split(SPLIT_SEP)
            tokens = line.split()
        
            if not train_rowcolonly:
                test_user_indices.append(user_indexer[tokens[0]])
                test_item_indices.append(item_indexer[tokens[1]])
                test_values.append(float(tokens[2]))
            else:
                if tokens[0] in rowids_dict and tokens[1] in colids_dict:
                    test_user_indices.append(user_indexer[tokens[0]])
                    test_item_indices.append(item_indexer[tokens[1]])
                    test_values.append(float(tokens[2]))
                else:
                    skipcnt += 1
 

            #if index > 200:
            #    break
        
        print "skipcnt = %d"%skipcnt
        #print user_indices
        #print item_indices
        #print values
        
        print "form test csr matrix"
        test_mat = csr_matrix( (test_values,(test_user_indices,test_item_indices)), shape=(len(user_indexer),len(item_indexer)) )
        
        print "calculate size of rows"
        test_row_sizes = test_mat.indptr[1:] - test_mat.indptr[:-1]
        
        #print row_sizes
        #print mat.indices
        #print mat.data
        
        print "write test binary file"
        ofile = open(output_path + "/test.dat", "wb")
        ofile.write(struct.pack("=iiiq", 1015, len(user_indexer), len(item_indexer), test_mat.getnnz()))
        ofile.write(struct.pack("=%si" % len(test_row_sizes), *test_row_sizes))
        ofile.write(struct.pack("=%si" % len(test_mat.indices), *test_mat.indices))
        ofile.write(struct.pack("=%sd" % len(test_mat.data), *test_mat.data))
        ofile.close()

def big_convert_csrmatrix(train_filename, test_filename, output_path = '.'):
    random.seed(12345)
    
    user_ids = set()
    item_ids = set()
    
    # index users and items
    
    for index, line in enumerate(open(train_filename)):
    
        if index % 1000000 == 0:
            print "1st pass training:", index
        
        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()
        user_ids.add(tokens[0])
        item_ids.add(tokens[1])
    
    nnz = index + 1

    for index, line in enumerate(open(test_filename)):
    
        if index % 1000000 == 0:
            print "1st pass test:", index
        
        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()
    
        user_ids.add(tokens[0])
        item_ids.add(tokens[1])
    


    user_id_list = list(user_ids)
    item_id_list = list(item_ids)
    random.shuffle(user_id_list)
    random.shuffle(item_id_list)
    
    user_indexer = {key:value for value, key in enumerate(user_id_list)}
    item_indexer = {key:value for value, key in enumerate(item_id_list)}
    
    # now parse the data
    train_user_indices = list()
    train_item_indices = list()
    train_values = list()

    print "write train binary file"
    ofile = open(output_path + "/train.dat", "wb")
    ofile.write(struct.pack("=iiiq", 1015, len(user_indexer), len(item_indexer), nnz))
    #ofile.write(struct.pack("=%si" % len(train_row_sizes), *train_row_sizes))
    #ofile.write(struct.pack("=%si" % len(train_mat.indices), *train_mat.indices))
    #move to data pos
    ofile.seek((len(user_indexer) + nnz) *4 , 1)

    #chunk_rowsize = 100000000
    #chunk_rowsize = 100000000
    row_sizes = [0 for i in range(len(user_id_list))]
    indices = []

    for index, line in enumerate(open(train_filename)):
    
        if index % 1000000 == 0:
            print "2nd pass training:", index
        
        if index and index % chunk_rowsize == 0:
            train_mat = csr_matrix( (train_values,(train_user_indices,train_item_indices)), shape=(len(user_indexer),len(item_indexer)) )
    
            # append new col indices
            indices.extend(train_mat.indices)

            logger.info('users=%s, items=%s, train_valuse=%s', train_user_indices, train_item_indices,train_values)
            logger.info('write chunk %d, indices size=%d, data size=%d', index / chunk_rowsize,
                    len(train_mat.indices), len(train_mat.data))
    
            # data pos
            ofile.write(struct.pack("=%sd" % len(train_mat.data), *train_mat.data))
            logger.info('mat.indices=%s', train_mat.indices[:20])
            logger.info('mat.data=%s', train_mat.data[:20])

            # release the big memeory
            del train_user_indices
            del train_item_indices
            del train_values
            del train_mat

            #reset the data structure
            train_user_indices = list()
            train_item_indices = list()
            train_values = list()


        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()
    
        train_user_indices.append(user_indexer[tokens[0]])
        train_item_indices.append(item_indexer[tokens[1]])
        train_values.append(float(tokens[2]))

        # inc rowsize
        row_sizes[user_indexer[tokens[0]]] += 1
 

    #write the last block
    #if (index+1) % chunk_rowsize != 0:
    if True:
        train_mat = csr_matrix( (train_values,(train_user_indices,train_item_indices)), shape=(len(user_indexer),len(item_indexer)) )
        
        # append new col indices
        indices.extend(train_mat.indices)
        # data pos
        ofile.write(struct.pack("=%sd" % len(train_mat.data), *train_mat.data))
        logger.info('users=%s, items=%s, train_valuse=%s', train_user_indices, train_item_indices,train_values)
        logger.info('write chunk %s', index / chunk_rowsize +1)
        logger.info('mat.indices=%s', train_mat.indices[:20])
        logger.info('mat.data=%s', train_mat.data[:20])


        logger.info('nnz = %d, mat nnz=%d, row_sizes=%d, indices=%d, datasize=%d', nnz, train_mat.getnnz(),
            len(row_sizes), len(indices), len(train_mat.data))

    logger.info('rowsize=%s', row_sizes)
    logger.info('indices=%s', indices)

    #write rowsize and indices
    ofile.seek(20, 0)
    ofile.write(struct.pack("=%si" % len(row_sizes), *row_sizes))
    ofile.write(struct.pack("=%si" % len(indices), *indices))
 
    ofile.close()
    
    #############################################################################

    test_user_indices = list()
    test_item_indices = list()
    test_values = list()
    
    for index, line in enumerate(open(test_filename)):
    
        if index % 1000000 == 0:
            print "2nd pass test:", index
        
        #tokens = line.split(SPLIT_SEP)
        tokens = line.split()
    
        test_user_indices.append(user_indexer[tokens[0]])
        test_item_indices.append(item_indexer[tokens[1]])
        test_values.append(float(tokens[2]))
    
        #if index > 200:
        #    break
    
    
    #print user_indices
    #print item_indices
    #print values
    
    print "form test csr matrix"
    test_mat = csr_matrix( (test_values,(test_user_indices,test_item_indices)), shape=(len(user_indexer),len(item_indexer)) )
    
    print "calculate size of rows"
    test_row_sizes = test_mat.indptr[1:] - test_mat.indptr[:-1]
    
    #print row_sizes
    #print mat.indices
    #print mat.data
    
    print "write test binary file"
    ofile = open(output_path + "/test.dat", "wb")
    ofile.write(struct.pack("=iiiq", 1015, len(user_indexer), len(item_indexer), test_mat.getnnz()))
    ofile.write(struct.pack("=%si" % len(test_row_sizes), *test_row_sizes))
    ofile.write(struct.pack("=%si" % len(test_mat.indices), *test_mat.indices))
    ofile.write(struct.pack("=%sd" % len(test_mat.data), *test_mat.data))
    ofile.close()
    
    print "write user index mappings"
    ofile = open(output_path + "/user_ids.txt", "w")
    for user_id in user_id_list:
        ofile.write("%s\n" % user_id)
    ofile.close()
    
    print "write item index mappings"
    ofile = open(output_path + "/item_ids.txt", "w")
    for item_id in item_id_list:
        ofile.write("%s\n" % item_id)
    ofile.close()


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    
    cmdtype = sys.argv[1]
    train_filename = sys.argv[2]
    test_filename = sys.argv[3]
    train_rowcolonly = True
    if len(sys.argv) >=5:
        output_path = sys.argv[4]
    else:
        output_path = '.'

    if len(sys.argv) >=6:
        train_rowcolonly = False if sys.argv[5]=='false' else True
 
    if cmdtype == '-nomad':
        nomad_convert(train_filename, test_filename, output_path)
    elif cmdtype == '-big':
        big_convert(train_filename, test_filename, output_path, train_rowcolonly)
    elif cmdtype == '-hotfix_trainids':
        hotfix_trainids(train_filename)
    elif cmdtype == '-hotfix_testset':
        hotfix_testset(train_filename, test_filename, output_path)
