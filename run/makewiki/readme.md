bulid enwiki dataset
======================

Download the latest enwiki data, and build testset for current enwiki-1M dataset.
Current wordids file is enwiki-1M.dict.

```sh

#the wordmap file from wordids
awk '{printf("%s\t%s\n",$2,$3)}' ~/hpda/test/wikicorpus/dict/enwiki-1M.newmap.txt > enwiki-1M.dict

cd enwiki/
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
python ~/hpda/lda-test/src/preprocess/make_wiki.py enwiki-latest-pages-articles.xml.bz2 latest


# id mapping

python ~/hpda/lda-test/src/preprocess/mm2mrlda.py ../latest_all_bow.mm enwiki-latest-1M.mrlda.txt 2 new.wordmap
awk '{printf("%s\t%s\n",$1,$2)}' new.wordmap >new.id

vi new.id    delete first line

python ~/hpda/lda-test/src/preprocess/mm2mrlda.py ../latest_all_bow.mm enwiki-latest-1M.mrlda.txt 2 new.id

# build testset

tail -n 100000 enwiki-latest-1M.mrlda.txt >enwiki-1M-test100k.mrlda.txt
wc -l enwiki-1M-test100k.mrlda.txt 
python ~/hpda/lda-test/src/preprocess/mrlda2ylda.py enwiki-1M-test100k.mrlda.txt 
for f in `ls *.ylda`; do echo $f && ~/hpda/lda-test/tool/mallet/bin/mallet import-file --input $f --output `basename $f .ylda`.mallet --keep-sequence --token-regex "[\p{L}\p{N}_]+|[\p{P}]+"; done
~/hpda/lda-test/tool/mallet/bin/mallet evaluate-topics --dumpAlphabet all.dict --input enwiki-1M-test100k.mrlda.txt.mallet 
mv all.dict.data enwiki-1M-test100k.mallet.dict
python ~/hpda/lda-test/src/datastat/docStat.py enwiki-1M-test100k.mrlda.txt

#end

#
# ERRORLOG
# use enwiki-1M.dict's freq, this means use old vocabulary and it's encoding !!! wrong here, sort is not stable!!!
#

```sh
mkdir dict
cd dict
bzip2 -d ../latest_all_wordids.txt.bz2 
cp ../latest_all_wordids.txt all.wordids.dict
sort -nr -k 3 all.wordids.dict >all.wordids.dict.sort
awk '{print $2, $1}' all.wordids.dict.sort >_all.wordmap
cat <<EOF >all.wordmap
1234
EOF
cat _all.wordmap >>all.wordmap 
python wordmap2wordids.py all.wordmap enwiki-1M.dict all.reid.wordids
sort -nr -k 3 all.reid.wordids >all.reid.wordids.sort
awk '{printf("%s\t%d\t%s\n",$1,cnt,$3);cnt++}' all.reid.wordids.sort >all.reid

cd ..
python mm2mrlda.py latest_all_bow.mm enwiki-latest-1M.txt.mrlda 2 dict/all.reid
```
