. ~/hpda/lda-test/bin/init_env.sh

python plotall.py enwiki_10/hsw72_lda_enwiki_convergence.conf 
cp enwiki_10/*.pdf ~/tmp/bingjing

python plotall.py enwiki_tango5/knl_lda_enwiki_convergence.conf 
cp enwiki_tango5/*.pdf ~/tmp/bingjing


python plotall.py clueweb30b_tango12/knl_lda_clueweb30b_convergence.conf 
cp clueweb30b_tango12/*.pdf ~/tmp/bingjing

python plotall.py clueweb30b_24/hsw72_lda_clueweb30b_convergence.conf 
cp clueweb30b_24/*.pdf ~/tmp/bingjing
