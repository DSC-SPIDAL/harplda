package cc.mallet.topics.tui;

import cc.mallet.util.*;
import cc.mallet.types.*;
import cc.mallet.topics.*;

import java.io.*;

public class EvaluateTopics {

	static CommandOption.String printModel = new CommandOption.String(
			EvaluateTopics.class, "printModel", "FILENAME", true, null,
	         "Print the logLikelihood of the model only.  " +
			 "By default this is null, indicating that work not in print mode.", null);
	
	static CommandOption.String dumpAlphabet = new CommandOption.String(
			EvaluateTopics.class, "dumpAlphabet", "FILENAME", true, null,
	         "The filename in which to write the dictionary of the dataset.  " +
			 "By default this is null, indicating that no file will be written.", null);	
	
	static CommandOption.String wordTopicCountsFile = new CommandOption.String(EvaluateTopics.class, "word-topic-counts-file", "FILENAME", true, null,
	         "The filename in which to write a sparse representation of topic-word assignments.  " +
			 "By default this is null, indicating that no file will be written.", null);	
	
    static CommandOption.String modeldataFilename = new CommandOption.String
            (EvaluateTopics.class, "modeldata", "FILENAME", true, null,
    		 "A serialized partial model data from a third-party trainer's result.\n" + 
             "By default this is null, indicating that no file will be read.", null);

    static CommandOption.String modelFilename = new CommandOption.String
            (EvaluateTopics.class, "modelfile", "FILENAME", true, null,
    		 "A serialized model data from a trained topic model by mallet.\n" + 
             "By default this is null, indicating that no file will be read.", null);
    
    static CommandOption.String evaluatorFilename = new CommandOption.String
        (EvaluateTopics.class, "evaluator", "FILENAME", true, null,
		 "A serialized topic evaluator from a trained topic model.\n" + 
         "By default this is null, indicating that no file will be read.", null);

	static CommandOption.String inputFile = new CommandOption.String
		(EvaluateTopics.class, "input", "FILENAME", true, null,
		 "The filename from which to read the list of instances\n" +
		 "for which topics should be inferred.  Use - for stdin.  " +
		 "The instances must be FeatureSequence or FeatureSequenceWithBigrams, not FeatureVector", null);
	
    static CommandOption.String docProbabilityFile = new CommandOption.String
        (EvaluateTopics.class, "output-doc-probs", "FILENAME", true, null,
         "The filename in which to write the inferred log probabilities\n" +
		 "per document.  " +
         "By default this is null, indicating that no file will be written.", null);

    static CommandOption.String probabilityFile = new CommandOption.String
        (EvaluateTopics.class, "output-prob", "FILENAME", true, "-",
         "The filename in which to write the inferred log probability of the testing set\n" +
         "Use - for stdout, which is the default.", null);

	static CommandOption.Integer numParticles = new CommandOption.Integer
        (EvaluateTopics.class, "num-particles", "INTEGER", true, 10,
         "The number of particles to use in left-to-right evaluation.", null);

	static CommandOption.Boolean showWords = new CommandOption.Boolean
        (EvaluateTopics.class, "show-words", "TRUE|FALSE", false, false,
         "If true, print the log likelihood of each individual token to standard out.", null);

	static CommandOption.Boolean usingResampling = new CommandOption.Boolean
        (EvaluateTopics.class, "use-resampling", "TRUE|FALSE", false, false,
         "Whether to resample topics in left-to-right evaluation. Resampling is more accurate, but leads to quadratic scaling in the lenght of documents.", null);

	static CommandOption.Integer numIterations = new CommandOption.Integer
        (EvaluateTopics.class, "num-iterations", "INTEGER", true, 100,
         "The number of iterations of Gibbs sampling.", null);

    static CommandOption.Integer sampleInterval = new CommandOption.Integer
        (EvaluateTopics.class, "sample-interval", "INTEGER", true, 10,
         "The number of iterations between saved samples.", null);

    static CommandOption.Integer burnInIterations = new CommandOption.Integer
        (EvaluateTopics.class, "burn-in", "INTEGER", true, 10,
         "The number of iterations before the first sample is saved.", null);

    static CommandOption.Integer randomSeed = new CommandOption.Integer
        (EvaluateTopics.class, "random-seed", "INTEGER", true, 0,
         "The random seed for the Gibbs sampler.  Default is 0, which will use the clock.", null);

    static MarginalProbEstimator readdata(String modeldataFileName){
    	int numTopics = 0, numTypes = 0; // Number of topics to be fit

    	double[] alpha;	 // Dirichlet(alpha,alpha,...) is the distribution over topics
    	double alphaSum = 0;
    	double beta = 0;   // Prior on per-topic multinomial distribution over words
    	
    	int[][] typeTopicCounts; // indexed by <feature index, topic index>
    	int[] tokensPerTopic; // indexed by <topic index>    	
    	int topicMask;
    	int topicBits;
    	
    	MarginalProbEstimator estimator = null;
   	
    	
    	try {
    		DataInputStream in;
			in = new DataInputStream(new FileInputStream(modeldataFileName));
	
    		//numTopics
    		numTopics = in.readInt();
    		numTypes = in.readInt();
    		
    		
    		
        	System.out.printf("numTopcis:%d\n", numTopics);
        	System.out.printf("numTypes: %d\n",numTypes);   		
        	
    		if (Integer.bitCount(numTopics) == 1) {
    			// exact power of 2
    			topicMask = numTopics - 1;
    			topicBits = Integer.bitCount(topicMask);
    		}
    		else {
    			// otherwise add an extra bit
    			topicMask = Integer.highestOneBit(numTopics) * 2 - 1;
    			topicBits = Integer.bitCount(topicMask);
    		} 
    		
    		
    		alpha = new double[numTopics];
    		alphaSum = in.readDouble();
    		for (int i=0; i< numTopics; i++){
    			alpha[i] = alphaSum;
    		}
    		alphaSum *= numTopics;
    		beta = in.readDouble();
    	
    		
    		typeTopicCounts = new int[numTypes][];
    		tokensPerTopic = new int[numTopics];
    		
    		//for (int type = 0; type < numTypes; type++) {
    		//	typeTopicCounts[type] = new int[numTopics];
    		//}
    		
    		for (int k=0; k<numTopics; k++){
    			tokensPerTopic[k] = 0;
    		}
 
    		boolean useSparseMatrixFormat = true;
    		int count[] = new  int[numTopics];
    		int topic[] = new  int[numTopics];
    		if (useSparseMatrixFormat){
	    		for (int w = 0; w<numTypes; w++){
	    			int nonzeroCnt = 0;
	    			for (int k=0; k<numTopics; k++){
	    				count[k] = in.readInt();
	    				topic[k] = in.readInt();
	    				if (count[k] == 0){
	    					//row end 
	    					break;
	    				}
	    				nonzeroCnt ++;
	    				tokensPerTopic[topic[k]] += count[k];
	    			}
	    			
	    			typeTopicCounts[w] = new int[nonzeroCnt];
	    			//update to sparse vector
	    			for (int j=0; j<nonzeroCnt; j++){
	    				typeTopicCounts[w][j] = (count[j] << topicBits) + topic[j];
	    			}
	    		}
    		}
    		else{
	    		for (int w = 0; w<numTypes; w++){
	    			int nonzeroCnt = 0;
	    			for (int k=0; k<numTopics; k++){
	    				count[k] = in.readInt();
	    				tokensPerTopic[k] += count[k];
	    				if (count[k] > 0){
	    					nonzeroCnt ++;
	    				}
	    			}
	    			
	    			typeTopicCounts[w] = new int[nonzeroCnt];
	    			//update to sparse vector
	    			for (int k=0, j=0; k<numTopics; k++){
	    				if (count[k] > 0){
	    					typeTopicCounts[w][j] = (count[k] << topicBits) + k;
	    					j ++;
	    				}
	    			}
	    		}
    		}
    		
        	in.close();
        	
        	//debug only
        	System.out.printf("alpha: %f\n",alpha[0]);
        	System.out.printf("beta:%f\n",beta);
        	
/*    		for (int w = 0; w<numTypes; w++){
    			String show = "";
    			for (int k=0; k<numTopics; k++){
    				show += Integer.toString(typeTopicCounts[w][k] & topicMask) + ' ' + Integer.toString(typeTopicCounts[w][k] >> topicBits) + ' ';	
    			}
    			System.out.print(show + "\n");
    		}*/
       	
        	estimator = new MarginalProbEstimator(numTopics, alpha, alphaSum, beta,
   				 typeTopicCounts, tokensPerTopic);        	

    	} catch (EOFException ignored) {
    	    System.out.println("[EOF]");
		} catch (Exception e) {
			e.printStackTrace();
			System.err.println(e.getMessage());
		}
    	
    	return estimator;
		
    }
    
	public static void main (String[] args) {

        // Process the command-line options
		CommandOption.setSummary (EvaluateTopics.class,
                                  "Estimate the marginal probability of new documents under ");
        CommandOption.process (EvaluateTopics.class, args);

		if (modelFilename == null && modeldataFilename == null && evaluatorFilename.value == null) {
			System.err.println("You must specify a serialized topic evaluator. Use --help to list options.");
			System.exit(0);
		}

		if (inputFile.value == null) {
			System.err.println("You must specify a serialized instance list. Use --help to list options.");
			System.exit(0);
		}

		try {
			
			PrintStream docProbabilityStream = null;
			if (docProbabilityFile.value != null) {
				docProbabilityStream = new PrintStream(docProbabilityFile.value);
			}
			
			PrintStream outputStream = System.out;
			if (probabilityFile.value != null &&
				! probabilityFile.value.equals("-")) {
				outputStream = new PrintStream(probabilityFile.value);
			}

			// add a new load estimator method, from converted model data --modeldata
			MarginalProbEstimator evaluator = null; 
			if (evaluatorFilename.value != null) {
				evaluator =	MarginalProbEstimator.read(new File(evaluatorFilename.value));
			}
			else if (modeldataFilename.value != null){
				
				evaluator = readdata(modeldataFilename.value); 
			}	
			else if (modelFilename.value != null){
				ParallelTopicModel topicModel = null;
				try {
					topicModel = ParallelTopicModel.read(new File(modelFilename.value));
					evaluator = topicModel.getProbEstimator();
				} catch (Exception e) {
					System.out.println("Unable to restore saved topic model " + 
								   modelFilename.value + ": " + e);
					System.exit(1);
				}				
			}
			
			if (printModel.value != null){
				int totalTokens = evaluator.totalTokensNum();
				
				double modelLogLikelihood, perplexity;
				modelLogLikelihood = evaluator.modelLogLikelihood();
				
				//write to .dat file
				outputStream = new PrintStream(modeldataFilename.value + "-mallet-lhood.dat");
				outputStream.printf("%e\n", modelLogLikelihood);
			
				perplexity = Math.exp(-modelLogLikelihood/totalTokens);
				
				outputStream = new PrintStream(modeldataFilename.value + "-mallet-perplexity.dat");
				outputStream.printf("%e\n", perplexity);
				System.out.printf("totalTokens=%d, model logLikelihood=%e, perplexity=%e\n",
						totalTokens, modelLogLikelihood,perplexity);
				
				
				System.exit(1);
			}

		
			InstanceList instances = InstanceList.load (new File(inputFile.value));
			
			// show the total tokens number
			if (instances.size() > 0 &&
					instances.get(0) != null) {
					Object data = instances.get(0).getData();
					if (! (data instanceof FeatureSequence)) {
						System.out.println("Topic modeling currently only supports feature sequences: use --keep-sequence option when importing data.");
						System.exit(1);
					}
					
					int maxTokens = 0,	totalTokens = 0;
					int seqLen;

					for (int doc = 0; doc < instances.size(); doc++) {
						FeatureSequence fs = (FeatureSequence) instances.get(doc).getData();
						seqLen = fs.getLength();
						if (seqLen > maxTokens)
							maxTokens = seqLen;
						totalTokens += seqLen;
					}

					System.out.println("input max tokens: " + maxTokens);
					System.out.println("input total documents: " + instances.size());
					System.out.println("input total tokens: " + totalTokens);
				}
			
			if (dumpAlphabet.value != null){
				// 	show the Alphabet, the dictionary for wordid-feature
				instances.dumpAlphabet(dumpAlphabet.value);
			}

			if (evaluator == null){
				System.out.println("Unable to initialize a evaluator, quit");
				System.exit(1);				
			}

			evaluator.printmodel();
			System.out.printf("model logLikelihood=%e",evaluator.modelLogLikelihood());
			
			if (wordTopicCountsFile.value != null){
				
				evaluator.printTypeTopicCounts(new File (wordTopicCountsFile.value));
                System.exit(1);
			}
			
			evaluator.setPrintWords(showWords.value);
			
			outputStream.println(evaluator.evaluateLeftToRight(instances, numParticles.value, 
															   usingResampling.value,
															   docProbabilityStream));
			

		} catch (Exception e) {
			e.printStackTrace();
			System.err.println(e.getMessage());
		}
	}
}
