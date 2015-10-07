bulid enwiki dataset
======================

Download the latest enwiki data, and build testset for current enwiki-1M dataset.
Current wordids file is enwiki-1M.dict.

```sh
cd enwiki/
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
python ~/hpda/lda-test/src/preprocess/make_wiki.py enwiki-latest-pages-articles.xml.bz2 latest

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
