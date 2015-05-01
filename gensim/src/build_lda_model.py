import logging, gensim, bz2
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load id->word mapping (the dictionary), one of the results of step 2 above
#id2word = gensim.corpora.Dictionary.load_from_text(bz2.BZ2File('wordids.txt.bz2'))
id2word = gensim.corpora.Dictionary.load_from_text('wordids.txt.bz2')
# load corpus iterator
mm = gensim.corpora.MmCorpus('tfidf.mm')
# mm = gensim.corpora.MmCorpus(bz2.BZ2File('wiki_en_tfidf.mm.bz2')) # use this if you compressed the TFIDF output

print(mm)
#MmCorpus(3931787 documents, 100000 features, 756379027 non-zero entries)


# extract 100 LDA topics, using 20 full passes, no online updates
lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=1000, update_every=0, passes=400)

# print the most contributing words for 20 randomly selected topics
lda.print_topics(20)
