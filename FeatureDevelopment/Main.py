# Andy/Emily/Josh's feature development sandbox
#
# This program loads a set of question-to-question data, runs a set experimental feature vector generators,
# and feeds their combined output into an interative analysis module.
#
# This is not meant to be a complete contest entry, but a place to experiment with three sets of code:
# - loading/preprocessing questions
# - feature generation
# - iterative analysis
#
# By default it runs all features in the Features directory.  To only run specific features, pass
# --features=[Feature1,Feature2,etc] on the command line.


from FeatureFinder import FeatureFinder
from Loader import Loader
from Preprocessor import Preprocessor
from Features import *
from utilities import ellips
from Scorer import Scorer
from pprint import pprint
import pickle, sys
import pandas

# we can cache the output of the loader+preprocessor to disk, to avoid this performance hit
# every time.  If the user wants to use the cached data, load it here and skip the loader+preprocessor

if "--cached" in sys.argv:
    print("Loading cached question and preprocessor data")
    questions = pickle.load(open("questions.pickle", "rb"))

else:
    # Loader

    questionFiles = Loader.getfilenames()
    questions = Loader.loadXMLQuestions(questionFiles)

    # Preprocessors

    Preprocessor.preprocessQuestions(questions)

    # Store the new data as the current cache

    pickle.dump(questions, open("questions.pickle", "wb"))

# Print out question structure for reference

print("\nSample question structure:")
samplequestion = questions[list(questions.keys())[0]]
for key in samplequestion:
    if key != 'related' and key != 'featureVector':
        print("  " + key + " = " + ellips(str(samplequestion[key]), 80))

# Feature Generators

featureGenerators = FeatureFinder.getSelectedFeatureModules()
featureNames = []
print("")
for feature in featureGenerators:
    print("Running feature generator '" + feature + "'")
    featureClass = globals()[feature].__dict__[feature]()
    featureClass.init(questions)
    featureNames += featureClass.getFeatureNames()
    for q in questions:
        questions[q]['featureVector'] += featureClass.createFeatureVector(questions[q], questions[q])
        for r in questions[q]['related']:
            questions[q]['related'][r]['featureVector'] += featureClass.createFeatureVector(questions[q]['related'][r], questions[q])

# Print Initial Results

print("\nSample questions and feature vectors:")
firstquestion = questions[list(questions.keys())[0]]
tempFeatures = [firstquestion['featureVector'] + ['Original']]
tempIndex = [firstquestion['id']]
print('\n' + firstquestion['id'] + ' ' + str(firstquestion['question'].encode('ascii', 'ignore'))[2:-1])
for r in firstquestion['related']:
    print('\n' + firstquestion['related'][r]['id'] + ' ' + str(firstquestion['related'][r]['question'].encode('ascii', 'ignore'))[2:-1])
    tempFeatures.append(firstquestion['related'][r]['featureVector'] + [firstquestion['related'][r]['givenRelevance']])
    tempIndex.append(firstquestion['related'][r]['id'])
print('\nFeature Vector:')
print(pandas.DataFrame(tempFeatures, columns=featureNames+['Label'], index=tempIndex))

# Scoring

print("\nComputing Perfectness\n")
output = Scorer.perfectness(questions, featureNames)
print('')
pprint(output[0:20])

# Ranking

print("\nRanking and Final Results current broken\n")

#print("\nRanking results\n")
#Scorer.rank(questions)

# Print Final Results

#print("\nSample question ranking:")
#firstquestion = questions[list(questions.keys())[0]]
#for r in firstquestion['related']:
#    print("%s correct=%s computed=%s" % (r, firstquestion['related'][r]['givenRank'], firstquestion['related'][r]['rank']))

print("\nFinished")