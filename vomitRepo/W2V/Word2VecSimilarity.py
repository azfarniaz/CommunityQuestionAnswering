import re
import nltk
import gensim
import numpy as np
from utilities import cosineSimilarity

class Word2VecSimilarity:

    # Any one-time initialization code can go here.  There entire nested question-and-answer
    # dataset is passed as a parameter, in case the initialization requires any of that data.

    def init(self, allQuestions):
        DIM = 300
        TOKEN_LIMIT = 30000
        WORKERS = 8
        WINDOW = 10
        DYNAMIC_WINDOW = False
        NEGATIVE = 0
        
        Word2VecSimilarity.cleanQuestions(allQuestions)
        questionList = Word2VecSimilarity.generateQuestionList(allQuestions)
        id2word = gensim.corpora.Dictionary(questionList)
        word2id = dict((v,k) for k,v in id2word.iteritems())
        corpus = lambda: ([word.lower() for word in allQuestions[q]['clean_question_words'] if word in word2id] for q in allQuestions)
        model = gensim.models.Word2Vec(size=DIM, window=WINDOW, workers=WORKERS,hs=0,negative=NEGATIVE)
        model.build_vocab(corpus())
        #model.train(corpus())
        for q in allQuestions:
            allQuestions[q]['word2vec'] = Word2VecSimilarity.generateQuestionVector(model, allQuestions[q]['clean_question_words'], DIM)
            for r in allQuestions[q]['related']:
                allQuestions[q]['related'][r]['word2vec'] = Word2VecSimilarity.generateQuestionVector(model, allQuestions[q]['clean_question_words'], DIM)
        return

    # Given a specific question, return a feature vector (one-dimensional array of one
    # or more features.

    def createFeatureVector(self, question, parentQuestion):
        # This is just placeholder code - insert code that actually generates a feature vector here
        # for the given question, and then return that feature vector instead of [0].
        similarity = cosineSimilarity(question['word2vec'], parentQuestion['word2vec'])
        print(similarity)
        return [similarity]

    # Returns a list of names for the features generated by this module.  Each entry in the
    # list should correspond to a feature in the createFeatureVector() response.

    def getFeatureNames(self):
        return ['word2vec-similarity']


    def cleanQuestions(questionDict):
        for q in questionDict:
            questionDict[q]['question'] = re.sub('[^\w\s]', ' ', questionDict[q]['question'])
            questionDict[q]['question'] = re.sub('[\s+]', ' ', questionDict[q]['question'])
            questionDict[q]['clean_question_words'] = nltk.word_tokenize(questionDict[q]['question'])


    def generateQuestionList(questionDict):
        questionList = []
        for q in questionDict:
            questionList.append(questionDict[q]['clean_question_words'])
        return questionList


    def generateQuestionVector(model, question, numFeatures):
        featureVec = np.zeros((numFeatures,),dtype="float32")
        num_words = 0
        index2word_set = set(model.index2word)
        for word in question:
            if word in index2word_set: 
                num_words = num_words + 1
                featureVec = np.add(featureVec,model[word])
        featureVec = np.divide(featureVec,num_words)
        return featureVec


    def generateAvgVectors(model, questionDict, numFeatures):
        for q in questionDict:
            questionDict[q]['word2vec'] = generateQuestionVector(model, questionDict[q]['clean_question_words'], numFeatures)

