zipf law keeps?
===================

```sh
awk '{printf("%s\t%s\n",$2,$3)}' enwiki-1M-reid.wordids.txt >enwiki-1M.dict
python ~/hpda/lda-test/src/datastat/zipf.py enwiki-1M.dict enWikipedia-1M
```
