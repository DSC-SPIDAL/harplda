import org.apache.spark.mllib.clustering.{KMeans, KMeansModel}
import org.apache.spark.mllib.linalg.{SparseVector, Vector}

def parse(s:String, vocabsize:Int):Vector ={
	//val index = s.split("[: ]").filter(!_.contains('.')).map(s => s.toInt)
	//val value = s.split("[: ]").filter(_.contains('.')).map(s => s.toDouble)
	val sl = s.split("[: ]")
	val index = sl.zipWithIndex.filter(_._2 % 2 == 0).map(_._1.toInt)
	val value = sl.zipWithIndex.filter(_._2 % 2 == 1).map(_._1.toDouble)

	return new SparseVector(vocabsize, index, value)	
}

val textfile = "enwiki_small.tfidf.low"
val vocab_size = 65334
val k = 6
val maxIter = 100
val outdir = "enwiki_small"

val textfile = "enwiki-1M_tfidf.mrlda"
val vocab_size = 1000000
val k = 1000
val maxIter = 1000
val outdir = "enwiki_1M"



// Load and parse the data
val data = sc.textFile(textfile)
val parsedData = data.map(_.split('\t')).map(x => parse(x(1),vocab_size)).cache()

val clusters = KMeans.train(parsedData, k, maxIter)

val WSSSE = clusters.computeCost(parsedData)
println("Within Set Sum of Squared Errors = " + WSSSE)

// Save and load model
clusters.save(sc, outdir + ".model")

val result = clusters.predict(parsedData) 
result.saveAsTextFile(outdir + ".result")

