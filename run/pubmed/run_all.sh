
#format: mrlda, reid
inputfile=pubmed.mrlda.reid.txt
prefix=pubmed-
suffix=mrlda.txt

#1. get samples
head -1000000 pubmed.mrlda.reid.txt >pubmed-1M.mrlda.txt
head -1500000 pubmed.mrlda.reid.txt >pubmed-1.5M.mrlda.txt
head -2000000 pubmed.mrlda.reid.txt >pubmed-2M.mrlda.txt
head -2500000 pubmed.mrlda.reid.txt >pubmed-2.5M.mrlda.txt

#2. format convert
# mrlda -> ylda
for f in `ls $prefix*`; do echo $f && python ~/hpda/lda-test/src/preprocess/mrlda2ylda.py $f; done

# ylda -> mallet
for f in `ls $prefix*.ylda`; do echo $f && ~/hpda/lda-test/tool/mallet/bin/mallet import-file --input $f --output `basename $f .ylda`.mallet --keep-sequence --token-regex "[\p{L}\p{N}_]+|[\p{P}]+"; done

#3. run experiments
sh do_mallet.sh

sh do_ylda.sh


