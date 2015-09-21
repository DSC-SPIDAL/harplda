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

### Dependency

    software                |   reference
    ----------------------  |  -------------
    python, numpy, scipy    |  http://continuum.io/downloads 
    gnu parallel            |  http://www.gnu.org/software/parallel/
    c3                      |  http://www.csm.ornl.gov/torc/C3
