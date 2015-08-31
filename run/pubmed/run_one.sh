echo "learn from $1"
python learn.py " ~/hpda/lda-test/tool/mallet/bin/mallet train-topics --input $1 --num-topics 2000 --num-iterations 1000 --inferencer-filename infer --evaluator-filename evaluator --alpha 20 --beta 0.01 --use-symmetric-alpha true"
#python learn.py " ~/hpda/lda-test/tool/mallet/bin/mallet train-topics --input $1 --num-topics 2000 --num-iterations 1000 --inferencer-filename infer --evaluator-filename evaluator --num-threads 8  --alpha 20 --beta 0.01 --use-symmetric-alpha true"


