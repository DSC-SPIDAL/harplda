. ~/hpda/lda-test/bin/init_env.sh

mkdir -p out-short out-full
rm out-short/* out-full/* *.pdf

python plotall.py hsw72_lda_clueweb30_convergence.conf TRUE 20000
python plotall.py hsw72_lda_enwiki_convergence.conf TRUE 20000


mv *.pdf out-short
python plotall.py hsw72_lda_clueweb30_convergence.conf
python plotall.py hsw72_lda_enwiki_convergence.conf

mv *.pdf out-full

mkdir -p ~/tmp/final
cp -r out* ~/tmp/final
