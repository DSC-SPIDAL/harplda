curdir=`pwd`
export TESTSET=pubmed
#cd ldartt-pubmed2m-1000-0.05-0.01/model
#~/hpda/lda-test/bin/lda-test evaluate-harp tmp_model

cd ldartt-pubmed2m-10_5threads/model
~/hpda/lda-test/bin/lda-test evaluate-harp tmp_model
cd $curdir

cd ldartt-pubmed2m-10kpart/model
~/hpda/lda-test/bin/lda-test evaluate-harp tmp_model
cd $curdir

cd ldartt-pubmed2m-5_10threads/model
~/hpda/lda-test/bin/lda-test evaluate-harp tmp_model
cd $curdir
