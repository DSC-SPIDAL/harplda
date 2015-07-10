import org.apache.spark.mllib.clustering.{KMeans, KMeansModel}
import org.apache.spark.mllib.linalg.{SparseVector, Vector}

def parse(s:String):Vector ={
	val vocab_size = 65334
	val index = s.split("[: ]").filter(!_.contains('.')).map(s => s.toInt)
	val value = s.split("[: ]").filter(_.contains('.')).map(s => s.toDouble)
	return new SparseVector(vocab_size, index, value)	
}

// Load and parse the data
val data = sc.textFile("enwiki_small.tfidf.low")
val vocab_size = 65334
val parsedData = data.map(_.split('\t')).map(x => parse(x(1))).cache()

val clusters = KMeans.train(parsedData, 6, 100)

// Save and load model
clusters.save(sc, "kmeans-enwiki-small")

val result = clusters.predict(parsedData) 

result.saveAsTextFile("clustersoutput.txt")

