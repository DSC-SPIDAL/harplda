/*
 * Copyright 2014 Indiana University
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package edu.iu.ldartt;

import it.unimi.dsi.fastutil.ints.Int2IntMap;
import it.unimi.dsi.fastutil.ints.Int2ObjectMap;
import it.unimi.dsi.fastutil.ints.Int2ObjectOpenHashMap;
import it.unimi.dsi.fastutil.ints.IntAVLTreeSet;
import it.unimi.dsi.fastutil.ints.IntArrayList;
import it.unimi.dsi.fastutil.objects.ObjectIterator;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Calendar;
import java.util.LinkedList;
import java.util.Random;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapred.CollectiveMapper;

import edu.iu.harp.array.ArrPartition;
import edu.iu.harp.array.ArrTable;
import edu.iu.harp.array.IntArrPlus;
import edu.iu.harp.compute.fork.Computation;
import edu.iu.harp.compute.parallel.ParallelCompute;
import edu.iu.harp.keyval.KeyValStatus;
import edu.iu.harp.primitivekv.Int2IntKVTable;
import edu.iu.harp.primitivekv.IntVCombiner;
import edu.iu.harp.resource.ResourcePool;
import edu.iu.harp.trans.IntArray;

public class LDACollectiveMapper
  extends
  CollectiveMapper<String, String, Object, Object> {

  private int numTopics;
  private double alpha;
  private double beta;
  private int numIterations;
  private int numDocsInBatch;
  private int maxNumParInModel;
  private int numThreads;
  private String modelDirPath;
  private String localDirPath;
  private int numSlices;
  private boolean printModel;

  // private long computeTime;

  /**
   * Mapper configuration.
   */
  @Override
  protected void setup(Context context) {
    LOG
      .info("start setup"
        + new SimpleDateFormat("yyyyMMdd_HHmmss")
          .format(Calendar.getInstance()
            .getTime()));
    long startTime = System.currentTimeMillis();
    Configuration configuration =
      context.getConfiguration();
    numTopics =
      configuration.getInt(
        LDAConstants.NUM_TOPICS, 500);
    alpha =
      configuration.getDouble(LDAConstants.ALPHA,
        0.1);
    beta =
      configuration.getDouble(LDAConstants.BETA,
        0.1);
    numIterations =
      configuration.getInt(
        LDAConstants.NUM_ITERATIONS, 20);
    numDocsInBatch =
      configuration.getInt(
        LDAConstants.NUM_DOCS_IN_BATCH, 100);
    maxNumParInModel =
      configuration.getInt(
        LDAConstants.MAX_NUM_PARTITIONS_IN_MODEL,
        1000);
    numThreads =
      configuration.getInt(
        LDAConstants.NUM_THREADS, 16);
    modelDirPath =
      configuration.get(LDAConstants.MODEL_DIR,
        "");
    localDirPath =
      configuration.get(LDAConstants.LOCAL_DIR,
        "");
    numSlices = 2;
    printModel =
      configuration.getBoolean(
        LDAConstants.PRINT_MODEL, false);
    // computeTime = 0L;
    long endTime = System.currentTimeMillis();
    LOG.info("config (ms): "
      + (endTime - startTime));
    LOG.info("Num Topics " + numTopics);
    LOG.info("Alpha " + alpha);
    LOG.info("Beta " + beta);
    LOG.info("Num Iterations " + numIterations);
    LOG.info("Num docs in batch "
      + numDocsInBatch);
    LOG.info("Num partitions in model "
      + maxNumParInModel);
    LOG.info("Num Threads " + numThreads);
    LOG.info("Model Dir Path " + modelDirPath);
    LOG.info("Local Dir Path " + localDirPath);
    LOG.info("Print Model " + printModel);
  }

  protected void mapCollective(
    KeyValReader reader, Context context)
    throws IOException, InterruptedException {
    long startTime = System.currentTimeMillis();
    LinkedList<String> docFiles =
      getDocFiles(reader);
    try {
      runLDA(docFiles,
        context.getConfiguration(), context);
    } catch (Exception e) {
      e.printStackTrace();
    }
    LOG.info("Total iterations in master view: "
      + (System.currentTimeMillis() - startTime));
  }

  private LinkedList<String> getDocFiles(
    final KeyValReader reader)
    throws IOException, InterruptedException {
    final LinkedList<String> docFiles =
      new LinkedList<>();
    while (reader.nextKeyValue()) {
      final String value =
        reader.getCurrentValue();
      LOG.info("File: " + value);
      docFiles.add(value);
    }
    return docFiles;
  }

  private void runLDA(
    final LinkedList<String> docFilePaths,
    final Configuration configuration,
    final Context context) throws Exception {
    final DocumentStore docStore =
      new DocumentStore(docFilePaths,
        numDocsInBatch, numThreads,
        this.getSelfID(), localDirPath,
        configuration, true);
    // --------------------------------------------------------
    // Count word range
    int[] wordIDRange = getWordIDRange(docStore);
    final int expectedNumWords =
      (int) Math.ceil((wordIDRange[1]
        - wordIDRange[0] + 1)
        / (double) maxNumParInModel);
    wordIDRange = null;
    TopicCountVWordKTable globalWordTable =
      new TopicCountVWordKTable(1,
        expectedNumWords, this.getResourcePool());
    TopicCountVWordKTable localWordTable =
      new TopicCountVWordKTable(1,
        expectedNumWords, this.getResourcePool());
    // Initialize topic assignment of these docs
    long opID = 0L;
    while (docStore.loadNextDocs()) {
      LinkedList<Document> docList =
        docStore.getCurrentDocs();
      createLocalWordTable(docList,
        localWordTable, this.getResourcePool());
      initializeZ(docList, globalWordTable,
        localWordTable, opID,
        this.getResourcePool());
      this.releaseTable(localWordTable);
      opID++;
    }
    docStore.setPassAgain();
    localWordTable = null;
    // -------------------------------------------------------
    // Get the vocabulary size
    final int vocabularySize =
      getVocabularySize("get-vocabulary-size",
        globalWordTable);
    // Slicing the global model
    final Int2ObjectOpenHashMap<TopicCountVWordKTable> globalWordTableMap =
      new Int2ObjectOpenHashMap<>(numSlices);
    sliceGlobalWordTable(globalWordTable,
      globalWordTableMap, numSlices,
      expectedNumWords, this.getResourcePool());
    globalWordTable = null;
    // Calculate topic sums
    final int[] topicSums = new int[numTopics];
    final double[] commons =
      new double[numTopics];
    final double[] rCoeffDistr =
      new double[numTopics];
    getTopicSums("get-initial-topics-word-sum",
      topicSums, globalWordTableMap);
    double rCoeffSum =
      calculateCommons(vocabularySize, topicSums,
        commons, rCoeffDistr);
    // -------------------------------------------------------
    // Create computation and tasks
    final LinkedList<SampleZTask3> sampleZTasks =
      new LinkedList<>();
    for (int i = 0; i < numThreads; i++) {
      SampleZTask3 sampleZTask =
        new SampleZTask3(numTopics, alpha, beta,
          commons, rCoeffDistr);
      // sampleZTask
      // .setLocal(new TopicCountVWordKTable(1,
      // expectedNumWords, this
      // .getResourcePool()));
      // sampleZTask
      // .setDelta(new TopicCountVWordKTable(1,
      // expectedNumWords, this
      // .getResourcePool()));
      sampleZTasks.add(sampleZTask);
    }
    final ParallelCompute<SampleZTask3> computation1 =
      new ParallelCompute<>(sampleZTasks);
    final LinkedList<RotateGTask> rotateGTasks =
      new LinkedList<>();
    rotateGTasks.add(new RotateGTask(this,
      globalWordTableMap));
    final Computation<RotateGTask> computation2 =
      new Computation<>(rotateGTasks);
    computation1.start();
    computation2.start();
    // -------------------------------------------------------
    // For iteration
    final int numWorkers = this.getNumWorkers();
    for (int i = 1; i <= numIterations; i++) {
      long iteStart = System.currentTimeMillis();
      this.logMemUsage();
      this.logGCTime();
      for (SampleZTask3 sampleZTask : sampleZTasks) {
        sampleZTask.setRCoeffSum(rCoeffSum);
      }
      rmEmptyEntries(globalWordTableMap);
      while (docStore.loadNextDocs()) {
        // Split docs and set docs to tasks
        final LinkedList<Document> docList =
          docStore.getCurrentDocs();
        final Int2ObjectOpenHashMap<LinkedList<Document>> docMap =
          splitDocList(docList, numThreads);
        int splitID = 0;
        for (SampleZTask3 sampleZTask : sampleZTasks) {
          sampleZTask.setDocuments(docMap
            .get(splitID));
          splitID++;
        }
        for (int j = 0; j < numWorkers; j++) {
          // For the first time to start the
          // rotation
          if (i == 1 && j == 0) {
            for (int k = 0; k < numSlices; k++) {
              sampleZSparse1(
                globalWordTableMap.get(k),
                sampleZTasks, computation1);
              computation2.submit(new Integer(k));
            }
          } else {
            for (int k = 0; k < numSlices; k++) {
              final int sliceID =
                ((Integer) computation2
                  .waitOutput()).intValue();
              sampleZSparse1(
                globalWordTableMap.get(sliceID),
                sampleZTasks, computation1);
              computation2.submit(new Integer(
                sliceID));
            }
          }
        }
      }
      docStore.setPassAgain();
      computation2.waitAndPause();
      // LOG.info("Computation took: " +
      // computeTime);
      // computeTime = 0L;
      // Get global word count per topic
      getTopicSums("get-topics-word-sum-" + i,
        topicSums, globalWordTableMap);
      rCoeffSum =
        calculateCommons(vocabularySize,
          topicSums, commons, rCoeffDistr);
      computation2.start();
      //if (printModel && (i % 50 == 0 || i == 1)) {
      if (printModel && (i % 100 == 0 )) {
        LOG
          .info("Print global model at iteration "
            + i);
        try {
          printWordTable(globalWordTableMap,
            modelDirPath + "/tmp_model/" + i
              + "/", this.getSelfID(),
            configuration);
        } catch (Exception e) {
          LOG.error(
            "Fail to output intermediate model.",
            e);
        }
      }
      context.progress();
      long iteEnd = System.currentTimeMillis();
      LOG.info("Iteration " + i + " took: "
        + (iteEnd - iteStart));
    }
    // Stop computation 1
    computation1.stop();
    // Stop computation 2
    computation2.stop();
    Object output = null;
    do {
      output = computation2.waitOutput();
    } while (output != null);
    // Free all the objects cached
    // They are not used any more.
    this.getResourcePool().freeResourcePool();
    // Output Cword
    if (printModel) {
      getTopicSums("get-final-topics-word-sum",
        topicSums, globalWordTableMap);
      int maxNumPartitions =
        this.numThreads * this.getNumWorkers();
      try {
        outputWordProbabilityPerTopic(
          configuration, globalWordTableMap,
          topicSums, vocabularySize,
          maxNumPartitions,
          this.getResourcePool());
      } catch (IOException e) {
        LOG.error(
          "Fail to output the final results.", e);
      }
    }
  }

  private double calculateCommons(
    final int vocabularySize,
    final int[] topicSums,
    final double[] commons,
    final double[] rCoeffDistr) {
    double rCoeffSum = 0.0;
    for (int i = 0; i < numTopics; i++) {
      commons[i] =
        1.0 / ((double) topicSums[i] + beta
          * (double) vocabularySize);
      rCoeffDistr[i] = alpha * commons[i];
      rCoeffSum += rCoeffDistr[i];
    }
    return rCoeffSum;
  }

  private
    void
    sliceGlobalWordTable(
      final TopicCountVWordKTable globalWordTable,
      final Int2ObjectOpenHashMap<TopicCountVWordKTable> globalWordTableMap,
      final int numSlices,
      final int expectedNumWords,
      final ResourcePool resourcePool) {
    final IntAVLTreeSet partitionIDs =
      new IntAVLTreeSet(
        globalWordTable.getPartitionIDs());
    int i = 0;
    for (int partitionID : partitionIDs) {
      final int sliceID = i % numSlices;
      TopicCountVWordKTable tmpGlobalWordTable =
        globalWordTableMap.get(sliceID);
      if (tmpGlobalWordTable == null) {
        tmpGlobalWordTable =
          new TopicCountVWordKTable(1,
            expectedNumWords, resourcePool);
        globalWordTableMap.put(sliceID,
          tmpGlobalWordTable);
      }
      final TopicCountVWordKPartition partition =
        globalWordTable
          .removePartition(partitionID);
      partition.getKVMap().trim();
      tmpGlobalWordTable.addPartition(partition);
      i++;
    }
    if (globalWordTableMap.size() < numSlices) {
      for (int j = globalWordTableMap.size(); j < numSlices; j++) {
        globalWordTableMap.put(j,
          new TopicCountVWordKTable(1,
            expectedNumWords, resourcePool));
      }
    }
    for (Int2ObjectMap.Entry<TopicCountVWordKTable> entry : globalWordTableMap
      .int2ObjectEntrySet()) {
      LOG.info("Slice ID: " + entry.getIntKey()
        + ", num partitions: "
        + entry.getValue().getNumPartitions());
      entry.getValue().getPartitionMap().trim();
    }
  }

  private
    void
    rmEmptyEntries(
      final Int2ObjectOpenHashMap<TopicCountVWordKTable> wordTableMap) {
    long time1 = System.currentTimeMillis();
    IntArrayList rmTopicIDList =
      new IntArrayList();
    int rmTopicIDCount = 0;
    int localNumPartitions = 0;
    int localNumWords = 0;
    long localSize = 0;
    for (TopicCountVWordKTable wordTable : wordTableMap
      .values()) {
      wordTable.getPartitionMap().trim();
      for (TopicCountVWordKPartition partition : wordTable
        .getPartitions()) {
        partition.getKVMap().trim();
        for (TopicCount topicCount : partition
          .getKVMap().values()) {
          final ObjectIterator<Int2IntMap.Entry> iterator =
            topicCount.getTopicCountMap()
              .int2IntEntrySet().fastIterator();
          while (iterator.hasNext()) {
            final Int2IntMap.Entry entry =
              iterator.next();
            if (entry.getIntValue() <= 0) {
              rmTopicIDList
                .add(entry.getIntKey());
            }
          }
          for (int rmTopicID : rmTopicIDList) {
            topicCount.getTopicCountMap().remove(
              rmTopicID);
          }
          rmTopicIDCount += rmTopicIDList.size();
          rmTopicIDList.clear();
          topicCount.getTopicCountMap().trim();
        }
        localNumWords +=
          partition.getKVMap().size();
        localSize += partition.getSizeInBytes();
      }
      localNumPartitions +=
        wordTable.getNumPartitions();
    }
    long time2 = System.currentTimeMillis();
    LOG
      .info("Remove and trim: "
        + rmTopicIDCount
        + " empty entries in global word table took: "
        + (time2 - time1));
    LOG.info("localNumPartitions: "
      + localNumPartitions + ", localNumWords: "
      + localNumWords + ", localSize: "
      + localSize);
  }

  private int[] getWordIDRange(
    final DocumentStore docStore) {
    final int[] wordIDRange = new int[2];
    wordIDRange[0] = Integer.MAX_VALUE;
    wordIDRange[1] = Integer.MIN_VALUE;
    ArrTable<IntArray> arrTable =
      new ArrTable<>(new WordIDRangeArrCombiner());
    arrTable
      .addPartition(new ArrPartition<IntArray>(0,
        new IntArray(wordIDRange, 0, 2)));
    while (docStore.loadNextDocs()) {
      final LinkedList<Document> docList =
        docStore.getCurrentDocs();
      for (Document doc : docList) {
        for (int i = 0; i < doc.words.length; i++) {
          if (wordIDRange[0] > doc.words[i]) {
            wordIDRange[0] = doc.words[i];
          }
          if (wordIDRange[1] < doc.words[i]) {
            wordIDRange[1] = doc.words[i];
          }
        }
      }
    }
    docStore.setPassAgain();
    this.allreduce("lda", "get-word-id-range",
      arrTable);
    LOG.info("Word MIN ID: " + wordIDRange[0]
      + ", word MAX ID: " + wordIDRange[1]);
    return wordIDRange;
  }

  private void initializeZ(
    final LinkedList<Document> docList,
    final TopicCountVWordKTable globalWordTable,
    final TopicCountVWordKTable localWordTable,
    final long operationID,
    final ResourcePool pool) {
    long start = System.currentTimeMillis();
    final LinkedList<InitZTask> initZTasks =
      new LinkedList<>();
    for (int i = 0; i < numThreads; i++) {
      initZTasks.add(new InitZTask(
        localWordTable, numTopics));
    }
    final Computation<InitZTask> computation =
      new Computation<>(initZTasks);
    for (Document doc : docList) {
      computation.submit(doc);
    }
    computation.start();
    Object output = null;
    do {
      output = computation.waitOutput();
    } while (output != null);
    computation.stop();
    printLocalWordTableSize(localWordTable);
    long time1 = System.currentTimeMillis();
    this
      .syncGlobalWithLocal("lda",
        "upload-initial-local-model-"
          + operationID, localWordTable,
        globalWordTable, false, 8);
    long end = System.currentTimeMillis();
    LOG.info("initialize Z took: "
      + (end - start) + ", compute took: "
      + (time1 - start)
      + ", upload local table took: "
      + (end - time1));
  }

  private void createLocalWordTable(
    final LinkedList<Document> docList,
    final TopicCountVWordKTable table,
    final ResourcePool pool) {
    long time1 = System.currentTimeMillis();
    TopicCount tmpVal = new TopicCount();
    for (Document doc : docList) {
      final int[] words = doc.words;
      for (int i = 0; i < words.length; i++) {
        final TopicCount val =
          table.getVal(words[i]);
        if (val == null) {
          // Try to add tmpVal
          final KeyValStatus status =
            table.addKeyVal(words[i], tmpVal);
          if (status == KeyValStatus.ADDED) {
            tmpVal = new TopicCount();
          }
        }
      }
    }
    long time2 = System.currentTimeMillis();
    LOG.info("create local table took: "
      + (time2 - time1));
  }

  private void printLocalWordTableSize(
    final TopicCountVWordKTable wordTable) {
    long time1 = System.currentTimeMillis();
    int count = 0;
    long size = 0;
    for (TopicCountVWordKPartition partition : wordTable
      .getPartitions()) {
      size += partition.getSizeInBytes();
      count += partition.getKVMap().size();
    }
    long time2 = System.currentTimeMillis();
    LOG.info("localWordTable size: " + size
      + ", word count: " + count
      + ", partition count: "
      + wordTable.getNumPartitions() + ", took: "
      + (time2 - time1));
  }

  private
    void
    getTopicSums(
      final String opName,
      final int[] topicSums,
      final Int2ObjectOpenHashMap<TopicCountVWordKTable> globalWordTableMap) {
    long time1 = System.currentTimeMillis();
    Arrays.fill(topicSums, 0);
    for (TopicCountVWordKTable wordTable : globalWordTableMap
      .values()) {
      for (TopicCountVWordKPartition partition : wordTable
        .getPartitions()) {
        final ObjectIterator<Int2ObjectMap.Entry<TopicCount>> iterator1 =
          partition.getKVMap()
            .int2ObjectEntrySet().fastIterator();
        while (iterator1.hasNext()) {
          final Int2ObjectMap.Entry<TopicCount> entry1 =
            iterator1.next();
          final ObjectIterator<Int2IntMap.Entry> iterator2 =
            entry1.getValue().getTopicCountMap()
              .int2IntEntrySet().fastIterator();
          while (iterator2.hasNext()) {
            final Int2IntMap.Entry entry2 =
              iterator2.next();
            topicSums[entry2.getIntKey()] +=
              entry2.getIntValue();
          }
        }
      }
    }
    ArrTable<IntArray> arrTable =
      new ArrTable<>(new IntArrPlus());
    arrTable
      .addPartition(new ArrPartition<IntArray>(0,
        new IntArray(topicSums, 0, numTopics)));
    long time2 = System.currentTimeMillis();
    this.allreduce("lda", opName, arrTable);
    long time3 = System.currentTimeMillis();
    long numTokens = 0L;
    // for (int i = 0; i < numTopics; i++) {
    // numTokens += topicSums[i];
    // }
    LOG.info("getTopicsWordSum took: "
      + (time3 - time1)
      + ", local compute took: "
      + (time2 - time1) + ", allreduce took: "
      + (time3 - time2) + ", total tokens: "
      + numTokens);
  }

  private int getVocabularySize(
    final String opName,
    final TopicCountVWordKTable wordTable) {
    final Int2IntKVTable vocabularySumTable =
      new Int2IntKVTable(new IntVCombiner(), 1,
        1, this.getResourcePool());
    int localNumWords = 0;
    for (TopicCountVWordKPartition partition : wordTable
      .getPartitions()) {
      localNumWords +=
        partition.getKVMap().size();
    }
    vocabularySumTable
      .addKeyVal(0, localNumWords);
    this.allreduce("lda", opName,
      vocabularySumTable);
    final int vocabularySize =
      vocabularySumTable.getVal(0);
    this.releaseTable(vocabularySumTable);
    LOG
      .info("Vocabulary Size: " + vocabularySize);
    return vocabularySize;
  }

  private
    Int2ObjectOpenHashMap<LinkedList<Document>>
    splitDocList(
      final LinkedList<Document> docList,
      final int numSplits) {
    final Int2ObjectOpenHashMap<LinkedList<Document>> docMap =
      new Int2ObjectOpenHashMap<>(numSplits);
    final Random random =
      new Random(System.currentTimeMillis());
    for (Document doc : docList) {
      final int splitID =
        random.nextInt(numSplits);
      LinkedList<Document> tmpDocList =
        docMap.get(splitID);
      if (tmpDocList == null) {
        tmpDocList = new LinkedList<>();
        docMap.put(splitID, tmpDocList);
      }
      tmpDocList.add(doc);
    }
    return docMap;
  }

  private
    void
    sampleZSparse1(
      final TopicCountVWordKTable globalWordTable,
      final LinkedList<SampleZTask3> sampleZTasks,
      final ParallelCompute<SampleZTask3> computation1) {
    // long t1 = System.currentTimeMillis();
    for (SampleZTask3 sampleZTask : sampleZTasks) {
      sampleZTask.setGlobal(globalWordTable);
    }
    computation1.run();
    // long t2 = System.currentTimeMillis();
    // computeTime += (t2 - t1);
  }

  private void sampleZSparse2(
    TopicCountVWordKTable globalWordTable,
    LinkedList<SampleZTask2> sampleZTasks,
    ParallelCompute<SampleZTask2> computation1) {
    // long t1 = System.currentTimeMillis();
    for (SampleZTask2 sampleZTask : sampleZTasks) {
      sampleZTask.setGlobal(globalWordTable);
    }
    computation1.run();
    for (SampleZTask2 sampleZTask : sampleZTasks) {
      sampleZTask.updateGlobal();
      this.releaseTable(sampleZTask.getLocal());
      this.releaseTable(sampleZTask.getDelta());
    }
    // long t2 = System.currentTimeMillis();
    // computeTime += (t2 - t1);
  }

  private
    void
    printWordTable(
      Int2ObjectOpenHashMap<TopicCountVWordKTable> wordTableMap,
      String folderPath, int workerID,
      Configuration congfiguration)
      throws IOException {
    FileSystem fs =
      FileSystem.get(congfiguration);
    Path folder = new Path(folderPath);
    if (!fs.exists(folder)) {
      fs.mkdirs(folder);
    }
    Path file =
      new Path(folderPath + "/" + workerID);
    PrintWriter writer =
      new PrintWriter(new BufferedWriter(
        new OutputStreamWriter(fs.create(file))));
    for (TopicCountVWordKTable wordTable : wordTableMap
      .values()) {
      for (TopicCountVWordKPartition partition : wordTable
        .getPartitions()) {
        for (Int2ObjectMap.Entry<TopicCount> entry : partition
          .getKVMap().int2ObjectEntrySet()) {
          writer.print(entry.getIntKey() + " ");
          for (int i = 0; i < numTopics; i++) {
            writer.print(entry.getValue()
              .getTopicCountMap().get(i)
              + " ");
          }
          writer.println();
        }
      }
    }
    writer.flush();
    writer.close();
  }

  private
    void
    outputWordProbabilityPerTopic(
      Configuration configuration,
      Int2ObjectOpenHashMap<TopicCountVWordKTable> wordTableMap,
      int[] topicSums, int vocabularySize,
      int maxNumPartitions,
      ResourcePool resourcePool)
      throws IOException {
    int expectNumTopics =
      numTopics / maxNumPartitions + 1;
    WordCountVTopicKTable topicTable =
      new WordCountVTopicKTable(expectNumTopics,
        expectNumTopics, resourcePool);
    // For each partition, add topic key and word
    // count value in the new table.
    WordCount wordCount = null;
    WordCount tmpWordCount = new WordCount();
    KeyValStatus status = null;
    for (TopicCountVWordKTable wordTable : wordTableMap
      .values()) {
      for (TopicCountVWordKPartition partition : wordTable
        .getPartitions()) {
        for (Int2ObjectMap.Entry<TopicCount> entry : partition
          .getKVMap().int2ObjectEntrySet()) {
          int word = entry.getIntKey();
          TopicCount topicCount =
            entry.getValue();
          if (topicCount.getTopicCountMap() != null) {
            for (Int2IntMap.Entry entry2 : topicCount
              .getTopicCountMap()
              .int2IntEntrySet()) {
              int topic = entry2.getIntKey();
              int tpcCount = entry2.getIntValue();
              wordCount =
                topicTable.getVal(topic);
              if (wordCount == null) {
                status =
                  topicTable.addKeyVal(topic,
                    tmpWordCount);
                if (status == KeyValStatus.ADDED) {
                  wordCount = tmpWordCount;
                  tmpWordCount = new WordCount();
                } else {
                  wordCount =
                    topicTable.getVal(topic);
                }
              }
              wordCount.getWordCountMap().addTo(
                word, tpcCount);
            }
          }
        }
      }
    }
    // Transpose and regroup based on the bucket
    this.regroup("lda", "regroup-topic-table",
      topicTable);
    // output based on the partition ID
    // calculate probability based on the count
    int numDigits =
      (maxNumPartitions + "").length();
    FileSystem fs = FileSystem.get(configuration);
    // Output word topic
    for (WordCountVTopicKPartition partition : topicTable
      .getPartitions()) {
      String topicWordFilePath =
        this.modelDirPath
          + "/topic_"
          + String.format("%0" + numDigits + "d",
            partition.getPartitionID());
      Path topicWordFile =
        new Path(topicWordFilePath);
      PrintWriter writer =
        new PrintWriter(new BufferedWriter(
          new OutputStreamWriter(
            fs.create(topicWordFile))));
      IntAVLTreeSet sortedTopicSet =
        new IntAVLTreeSet(partition.getKVMap()
          .keySet());
      for (int topic : sortedTopicSet) {
        int sum = topicSums[topic];
        wordCount = partition.getVal(topic);
        for (int i = 0; i < vocabularySize; i++) {
          int count =
            wordCount.getWordCountMap().get(i);
          double probability =
            ((double) count + beta)
              / ((double) sum + (double) vocabularySize
                * beta);
          writer.print(Math.log(probability)
            + " ");
        }
        writer.println();
      }
      writer.flush();
      writer.close();
    }
  }
}
