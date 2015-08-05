package cc.mallet.topics.tui;

import cc.mallet.util.*;
import cc.mallet.types.*;
import cc.mallet.topics.*;

import java.io.*;

public class EvaluateTopics {
	
    static CommandOption.String modeldataFilename = new CommandOption.String
            (EvaluateTopics.class, "modeldata", "FILENAME", true, null,
    		 "A serialized model data from a trained topic model.\n" + 
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
    		
    		for (int type = 0; type < numTypes; type++) {
    			typeTopicCounts[type] = new int[numTopics];
    		}
    		
    		int count = 0;
    		for (int k=0; k<numTopics; k++){
    			tokensPerTopic[k] = 0;
    		}
    		for (int w = 0; w<numTypes; w++){
    			for (int k=0; k<numTopics; k++){
    				count = in.readInt();
    				
    				typeTopicCounts[w][k] = (count << topicBits) + k;
					
    				tokensPerTopic[k] += count;	
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

		if (modeldataFilename == null && evaluatorFilename.value == null) {
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
			MarginalProbEstimator evaluator; 
			if (evaluatorFilename.value != null) {
				evaluator =	MarginalProbEstimator.read(new File(evaluatorFilename.value));
			}
			else{
				evaluator = readdata(modeldataFilename.value); 
			}	
				
			
			evaluator.setPrintWords(showWords.value);

			InstanceList instances = InstanceList.load (new File(inputFile.value));
			
			// show the Alphabet, the dictionary for wordid-feature
			instances.dumpAlphabet("dict");

			outputStream.println(evaluator.evaluateLeftToRight(instances, numParticles.value, 
															   usingResampling.value,
															   docProbabilityStream));
			

		} catch (Exception e) {
			e.printStackTrace();
			System.err.println(e.getMessage());
		}
	}
}
