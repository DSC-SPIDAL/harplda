### ap-sample testset

** files **

ap-sample.txt       original text file(mrlda input)  
ap-sample.txt.low   gibbslda input  
ap-sample.txt.ldac  blei's lda input  
ap-sample-id.txt    bingjing's harp-lda input
wordmap.txt         gibbslda id-word mapping file  
wordids.txt         gensim's id-word mapping file  

** test likelihood **

    $python ../src/evaluation/test_likelihood.py ~/hpda/lda-test/tool/blei/ ap-sample.ldac ap-sample.txt.ldac


