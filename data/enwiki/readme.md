enwiki-1m
============

1. original dataset created by gensim

enwiki-1M_wordids.txt
enwiki-1M_all_wordids.txt

these are the mm file dictionary, <mm id , term , freq>

2. when sort by freq, we get reid file

enwiki-1M.reorder   <mmid, reid> mapping
enwiki-1M-reid.wordids.txt  new id dictionary
enwiki-1M.newmap.txt    same as enwiki-1M-reid.wordids.txt

3. harp lda trained by reid files
enwiki-1M.train.dict    <model id, reid>    mapping

4. testset created by enwiki-1M.newmap.txt, using reid ids
refer to ~/run/makewiki/readme.md

5. noreid dictionary
ylda need train on noreid file
the train dict is 
enwiki-1M.reorder    <model id, reid>






