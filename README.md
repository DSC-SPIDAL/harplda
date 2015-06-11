lda-test
========

testbed of some opensource lda toolkits

## evaluation on the ap-sample dataset

1. clone this project

   ap-sample dataset under directory: data/ap-sample
   
   Compile the blei's lda code under tool/blei, just enter the directory and type 'make'

2. run your lda estimation program

3. get phi in the final model, convert it to blei's .beta format

    .beta contains the log of the topic distributions.
    Each line is a topic; in line k, each entry is log p(w | z=k)

    Use data/ap-sample/wordmap.txt as id-word dictionary to assign the word id.
    You must use the same id-word mapping when converting the model file

    There is a GibbsLDA++ model file under the directory: data/ap-sample/model
    It runs gibbs sampling on ap-sample with 20 topics and 1000 iterations, default \alpha and \beta

    .other file contains alpha value

4. calculate likelihood

    Calculate likelihood on GibbsLDA++ mode just on the traning data, as below:
    
    ```sh
    $ export TESTROOT="$HOME/lda-test"
    $ python $TESTROOT/src/evaluation/test_likelihood.py $TESTROOT/tool/blei/ $TESTROOT/data/ap-sample/models/ap-sample.gibbslda $TESTROOT/data/ap-sample/ap-sample.txt.ldac
    ```
    
    GibbsLDA++ model likelihood: doccnt = 2248, likelihood = -1621.3218849
    
    You should change the model prefix to yours:
    
    ```sh
    $ python $TESTROOT/src/evaluation/test_likelihood.py $TESTROOT/tool/blei/ YOURMODEL_FILE_PREFIX $TESTROOT/data/ap-sample/ap-sample.txt.ldac
    ```
