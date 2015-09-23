echo "learn from $1"
~/hpda/lda-test/tool/mallet/bin/mallet train-topics --input $1 --num-topics 1000 --num-iterations 1000 --alpha 50 --beta 0.01 --use-symmetric-alpha true --num-threads 12 --output-model-interval 100 --output-model mallet
