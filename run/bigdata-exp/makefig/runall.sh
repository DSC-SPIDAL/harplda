. ~/hpda/lda-test/bin/init_env.sh

mkdir -p out-short out-full
rm out-short/* out-full/* *.pdf

python plotall.py clueweb30-30x60.conf TRUE 25000
python plotall.py clueweb30-60x30.conf TRUE 25000
python plotall.py clueweb30-90x20.conf TRUE 25000
python plotall.py clueweb30-straggler-30x60.conf STRAGGLER 25000

mv *.pdf out-short

#python plotall.py clueweb30-30x60.conf 
#python plotall.py clueweb30-60x30.conf 
#python plotall.py clueweb30-90x20.conf 
#python plotall.py clueweb30-straggler-30x60.conf
#
#mv *.pdf out-full
