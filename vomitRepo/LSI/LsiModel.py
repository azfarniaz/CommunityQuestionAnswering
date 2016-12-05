from gensim import corpora, models, similarities
from six import iteritems
from nltk.corpus import stopwords
import logging
import os
import re
import csv
import sys

sys.path.insert(0, os.path.abspath('..'))
from utils.QuestionFileCreator import CreateFilePath, QTLQuestionCreator, getQuestions, getQuestionsFromQTL, getComments, QuestionCleaner, prepModelFolder, initializeLog
from utils.elementParser import elementParser, originalQuestionParser
from utils.sourceFiles import thisList, origQfilePath

initializeLog()

#For Saving the lsi model for later
new_dest = CreateFilePath('LsiModel')

stops = set(stopwords.words('english'))

qtlFiles = ['../crawler/data/questFile.json',
			'../crawler/data/questFile2.json']

QTLQuestions = QTLQuestionCreator(qtlFiles)

sources = QuestionCleaner(getQuestions(thisList))
sources += QuestionCleaner(getComments(thisList))
sources += QuestionCleaner(getQuestionsFromQTL(QTLQuestions))


# Dictionary is generated based on the question content of thisList
dictionary = corpora.Dictionary(line['question'].lower().split() for line in sources)
# remove stopwords
stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
# remove words only appearing once
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()
dictionary.save(new_dest +'.dict')


def generateLSIModel(corpus, dictionary, numTopics):
	corpora.MmCorpus.serialize(new_dest + '.mm', corpus)
	serialized_corpus = corpora.MmCorpus(new_dest + '.mm')
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=numTopics)
	index = similarities.MatrixSimilarity(lsi[serialized_corpus])
	return lsi, index

def createLSIPredictionFile(filePath, dictionary, numFeatures=200, withStops=True):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(withStops):
		predFile = tail +'-lsi' + str(numFeatures) +'-with-stops.pred'
	else:
		predFile = tail + '-lsi' + str(numFeatures) + '.pred'
	modelPath = prepModelFolder()
	predFile = modelPath + predFile
	for oq in testQuestions:
		oq['origQuestion'] = re.sub('[^\w\s]', ' ', oq['origQuestion'])
		oq['origQuestion'] = re.sub('[\s+]', ' ', oq['origQuestion'])
		for q in oq['rel_questions']:
			q['question'] = re.sub('[^\w\s]', ' ', q['question'])
			q['question'] = re.sub('[\s+]', ' ', q['question'])
	with open(predFile, 'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t')
		for t_question in testQuestions:
			corpus = [dictionary.doc2bow(q['question'].lower().split()) for q in t_question['rel_questions']]
			lsi, index = generateLSIModel(corpus, dictionary, numFeatures)
			if(withStops):
				doc = t_question['origQuestion']
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
				doc = t_question['origQNoStops']
			vec_bow = dictionary.doc2bow(doc.lower().split())
			vec_lsi = lsi[vec_bow]
			sims = index[vec_lsi]
			for idx, quest in enumerate(t_question['rel_questions']):
				quest['simVal'] = sims[idx]
				writer.writerow([t_question['quest_ID'], quest['rel_quest_ID'], idx, quest['simVal'], quest['relevant']])


createLSIPredictionFile(origQfilePath, dictionary, 100, False)
createLSIPredictionFile(origQfilePath, dictionary, 100)


