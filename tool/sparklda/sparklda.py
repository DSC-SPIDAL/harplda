import sys
import collections
from pyspark import SparkContext, SparkConf
from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.mllib.linalg import Vectors

VocabSize = 1000000

def parser(line):
    items = line.strip().split('\t')
    if len(items) > 1:
        words = items[1].split(' ')
        worddict = {}
        for w in words:
            if w in worddict:
                worddict[int(w)] += 1
            else:
                worddict[int(w)] = 1
        worddict = collections.OrderedDict(sorted(worddict.items()))
        return Vectors.sparse(VocabSize, worddict.keys(), worddict.values())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('usage: sparklda <mrlda filename>')
        sys.exit(0)

    conf = (SparkConf().set("spark.driver.maxResultSize", "8g"))

    sc = SparkContext(appName="PythonSparkLDA", conf=conf)
    # Load and parse the data
    data = sc.textFile("hdfs://10.16.0.30/data/" + sys.argv[1])
    parsedData = data.map(lambda line: parser(line))
    # Index documents with unique IDs
    corpus = parsedData.zipWithIndex().map(lambda x: [x[1], x[0]]).cache()
    
    # Cluster the documents into three topics using LDA
    param_name='online'
    param_k = 100
    param_alpha = -1.0 
    param_beta = -1.0
    param_iternum = 50
    print('Start training...')
    trainer = LDA()
    ldaModel = trainer.train(corpus, k=param_k, maxIterations=param_iternum, docConcentration=param_alpha, topicConcentration=param_beta, seed=None, checkpointInterval=10, optimizer=param_name)
    print('End traiing!')

    # Output topics. Each is a distribution over words (matching word count vectors)
    print("Learned topics (as distributions over vocab of " + str(ldaModel.vocabSize()) + " words):")
    #topics = ldaModel.topicsMatrix()
    #for topic in range(3):
    #    print("Topic " + str(topic) + ":")
    #    for word in range(0, ldaModel.vocabSize()):
    #        print(" " + str(topics[word][topic]))
