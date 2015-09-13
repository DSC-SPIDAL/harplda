LDATrainer Accuracy Experiments
================================

Trainset: pubmed-2M  
Testset : pubmed-200k  
Trainer : mallet, ldartt, ylda  

### mallet  
server: m4:/scratch/pengb/hpda/pubmed/mallet/pubmed2m-lh

sh run_mallet.sh ../../pubmed-2M.mrlda.txt.mallet  
python learn.py " ~/hpda/lda-test/tool/mallet/bin/mallet train-topics --input $1 --num-topics 1000 --num-iterations 1000 --inferencer-filename infer --evaluator-filename evaluator --alpha 50 --beta 0.01 --use-symmetric-alpha true --num-threads 16 --output-model-interval 10 --output-model mallet-50-0.01-16

~/hpda/lda-test/bin/lda-test evaluate-mallet convert

### ldartt  
server: changping60:/mnt/disk1/pb/hpda/test/harplda/pubmed/ldartt

ldartt-trainer.sh

ldartt-eval.sh

### ylda  
cluster: madrid:/N/u/pengb/hpda/test/ylda

refer to $lda-test/run/ylda

### experiments result  
morningstar:/home/pb/hpda/test/pubmed

#### exp-1
ldartt,mallet, ylda

#### exp-2
ldartt- four configurations

3. 
