. ~/hpda/lda-test/bin/init_env.sh

mkdir -p out-short out-full
rm out-short/* out-full/* *.pdf

python plotall.py hsw48_lda_convergence.conf TRUE 20000
python plotall.py hsw48_lda_scale.conf TRUE 20000
python plotconvbar.py lda_clueweb30b_convergebar.conf True

mv *.pdf out-short
python plotall.py hsw48_lda_convergence.conf 
python plotall.py hsw48_lda_scale.conf 
python plotconvbar.py lda_clueweb30b_convergebar.conf 

mv *.pdf out-full

mkdir -p ~/tmp/final
cp -r out* ~/tmp/final
