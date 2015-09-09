PUBMED Dataset
====================

http://archive.ics.uci.edu/ml/datasets/Bag+of+Words

### Dataset Statistics

    docs: 8M
    vocab: 140K
    words: 737M
    
    doccnt = 8200000
    vocabSize = 141043
    wordcnt = 737869083
    doclen mean= 89, std= 38
    doc-word matrix sparsenes = 0.0006
    highest word freq = 7499755
    lowest word freq = 82
    
### Test set


Build the test set

```sh
tail -200000 pubmed.mrlda.reid.txt >pubmed-test-200k.mrlda.txt
tail -400000 pubmed.mrlda.reid.txt | head -200000 >pubmed-test-200k-2.mrlda.txt

for f in `ls pubmed-test*.ylda`; do echo $f && ~/hpda/lda-test/tool/mallet/bin/mallet import-file --input $f --output `basename $f .ylda`.mallet --keep-sequence --token-regex "[\p{L}\p{N}_]+|[\p{P}]+"; done

python ~/hpda/lda-test/src/datastat/docStat.py pubmed-test-200k.mrlda.txt
doccnt = 200000
vocabSize = 125540
wordcnt = 20372837
doclen mean= 101, std= 38
doc-word matrix sparsenes = 0.0008
highest word freq = 203113
lowest word freq = 1

python ~/hpda/lda-test/src/datastat/docStat.py pubmed-test-200k-2.mrlda.txt
doccnt = 200000
vocabSize = 126220
wordcnt = 20106255
doclen mean= 100, std= 37
doc-word matrix sparsenes = 0.0008
highest word freq = 205236
lowest word freq = 1

~/hpda/lda-test/tool/mallet/bin/mallet evaluate-topics --dumpAlphabet all.dict --input pubmed-test-200k.mrlda.txt.mallet
mv all.dict.data pubmed-test-200k.mallet.dict
mv pubmed-test-200k.mrlda.txt.mallet pubmed-test-200k.mallet.txt

# the training dataset wordids
python ~/hpda/lda-test/src/preprocess/dict2wordids.py pubmed-2M.mrlda.txt.dict pubmed-2M.mrlda.txt.wordid

```


