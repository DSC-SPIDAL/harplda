lda-test
========
testbed of harp-lda trainer

### Directory Structure
bin     ---- shared scripts
src     ---- 
|---preprocess  ---- data preprocess, format converters   
|---evaluation  ---- model accuracy evaluator
|---datastat  ---- input data statistics
|---analysis  ---- model data analysis
|---generator  ---- model and data simulation
|---partition  ---- data partition analysis

data    ---- train and test dataset
tool    ---- open source lda trainer source code (modified to add on evaluation code)
run     ---- experiments scripts, data and results

