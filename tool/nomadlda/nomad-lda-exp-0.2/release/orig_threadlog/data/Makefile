nips:
	mkdir nips
	wget https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/docword.nips.txt.gz -O nips/docword.nips.txt.gz
	gunzip nips/docword.nips.txt.gz
	cd nips; ../gendata.py docword.nips.txt 1500
	../lda-converter -m 1024 nips

moreclean:
	rm -rf nips


