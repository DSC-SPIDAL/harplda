modelsize
==============



```sh

# cdf of modelsize
python ~/hpda/lda-test/src/analysis/plot.py cdf.conf cdf.png . "iter*"

# modelsize shrinks @word rank K
python ~/hpda/lda-test/src/analysis/plot.py modelsize@K.conf modelsize@K.png . "K-*"

# topic cnt distribution
python ~/hpda/lda-test/src/analysis/group.py 50 topiccnt-1 group50-1
python ~/hpda/lda-test/src/analysis/group.py 50 topiccnt-1000 group50-1000
python ~/hpda/lda-test/src/analysis/plot.py topiccnt.conf group50.png . "group50-1*"
python ~/hpda/lda-test/src/analysis/plot.py topiccnt.conf topicdist.png . "topiccnt-1*"
```


