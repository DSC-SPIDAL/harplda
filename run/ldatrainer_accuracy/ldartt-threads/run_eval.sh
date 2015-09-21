curdir=`pwd`
export TESTSET=pubmed

cd ldartt-pubmed2m-30-16/model
sh ../../lda-testp evaluate-harp tmp_model
cd $curdir
cd ldartt-pubmed2m-30-32/model
sh ../../lda-testp evaluate-harp tmp_model
cd $curdir
cd ldartt-pubmed2m-30-64/model
sh ../../lda-testp evaluate-harp tmp_model
cd $curdir

