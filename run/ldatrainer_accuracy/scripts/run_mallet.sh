echo "learn from $1"
python learn.py " ~/hpda/lda-test/tool/mallet/bin/mallet train-topics --input $1 --num-topics 1000 --num-iterations 1000 --inferencer-filename infer --evaluator-filename evaluator --alpha 50 --beta 0.01 --use-symmetric-alpha true --num-threads 16 --output-model-interval 10 --output-model mallet-50-0.01-16"
