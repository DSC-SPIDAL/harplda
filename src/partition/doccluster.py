from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark.mllib.linalg import SparseVector
from numpy import array
from math import sqrt

vocab_size = 65334

def parse(line):
    """
    input: modified ldac input format
    docid\tindex:value index:value....

    return:
    (docid, kv map)
    """
    parts = line.strip().split('\t')
    docid = parts[0]
    pairs = parts[1].split(' ')
    kvmap = {}
    for t in pairs:
        kv = t.split(':')
        kvmap[int(kv[0])] = float(kv[1])

    return (docid, kvmap)

# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

#sameModel = KMeansModel.load(sc, "myModelPath")
#def predict(point):
#    cluster_id = clusters.predict(point)
#    return 


def load_data(textfile):
    global sc
    data = sc.textFile(textfile)
    parsedData = data.map(lambda line: (parse(line)[0], SparseVector(vocab_size, parse(line)[1])))
    vectors = parsedData.map(lambda (docid, vector) : vector)


    return parsedData, vectors


def train(vectors, k, maxIter=100, run=10, mode="random"):
    # Build the model (cluster the data)
    clusters = KMeans.train(vectors, k, maxIterations=maxIter,
                    runs= run, initializationMode= mode)
    return clusters


def predictX(model, x):
    """Find the cluster to which x belongs in this model."""
    best = 0
    best_distance = float("inf")
    #x = _convert_to_vector(x)
    for i in xrange(len(model.centers)):
        distance = x.squared_distance(model.centers[i])
        if distance < best_distance:
            best = i
            best_distance = distance
    return best

if __name__ == '__main__':

    inputpath = ""
    textfile ="enwiki_small.tfidf.low"
    modeldir = textfile + "_model"
    predictsfile = textfile + ".predict"

    # Load and parse the data
    parsedData, vectors = load_data(inputpath + textfile)
    
    # Build the model (cluster the data)
    clusters = train(vectors, 2, 100)
    
    WSSSE = vectors.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    print("Within Set Sum of Squared Error = " + str(WSSSE))
    
    # Save and load model
    clusters.save(sc, modeldir)
    
    # 
    predicts = parsedData.map(lambda (docid, vector): (docid, clusters.predict(vector))).collect()

    predicts.saveAsTextFile(predictsfile)


