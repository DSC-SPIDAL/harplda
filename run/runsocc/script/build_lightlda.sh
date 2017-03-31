#!/bin/bash

bin=/tmp/hpda/test/lightlda/bin/
inputdir=$1
dataset=pubmed-2M

node=(0 1 2 3)
echo $node
for id in ${node[*]}; do
    echo "$id"
    mkdir -p $id
    python $bin/text2libsvm.py $inputdir/$dataset.mm.$id $inputdir/$dataset.libsvm.$id $inputdir/$dataset.word_id.dict.$id
    $bin/dump_binary $inputdir/$dataset.libsvm.$id $inputdir/$dataset.word_id.dict.$id $id 0
done
