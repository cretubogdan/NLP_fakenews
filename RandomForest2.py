import sys
sys.path.insert(0, 'modules')
from Logger import *
from DbManager import *
from WorkPool import *
from Reader import *

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
import nltk
import re

POLARITY = 0
ID = 1
DATETIME = 2
QUERY = 3
USER = 4
TEXT = 5

logger = Logger()
wp = WorkPool()
wp.run()

header = None
train = None
test = None

def DoRead():
    csv = Reader()
    logger.Log(Severity.INFO, "Starting reading datasets")
    csv.Read()
    logget.Log(Severity.INFO, "Finished reading datasets")

    header = csv.GetHeaderTrain()
    train = csv.GetBodyTrain()
    test = csv.GetBodyTest()

def DoCleanHelper(reviews):
    stops = set(stopwords.words("english"))

    for review in reviews:
        review = re.sub("[^a-zA-Z]"," ", review)
        review = review.lower().split()

        words = [w for w in review if not w in stops]

        review = " ".join(words)

    return reviews

def DoClean():
    train_copy = []
    test_copy = []
    for i in range(10):
        

def main():
    DoRead()
    DoClean()

    clean_train = []
    train_labeled = []
    for i in range(len(train)):
        clean_train.append(DoClean(train[i][TEXT]))
        train_labeled.append(train[i][POLARITY])

    vectorizer = CountVectorizer()
    train_data_features = vectorizer.fit_transform(clean_train)
    train_data_features = train_data_features.toarray()

    print("Am terminat de facut dictionarul")

    forest = RandomForestClassifier(n_estimators = 10000)
    forest = forest.fit(train_data_features, train_labeled)

    print("Am terminat de aplicat random forest")


    clean_test = []
    test_labeled = []
    for i in range(len(test)):
        clean_test.append(DoClean(test[i][TEXT]))
        test_labeled.append(test[i][POLARITY])

    print("Am terminat de testat datele")

    test_data_features = vectorizer.transform(clean_test).toarray()

    result = forest.predict(test_data_features)

    
    if len(result) != len(test):
        print("AU LUNGIMI DIFERITE")

    shots = 0
    for i in range(len(result)):
        if result[i] == test[i][POLARITY]:
            shots += 1

    print("Am o probabilitate de " + str(((shots / len(result)) * 100)))



if __name__ == '__main__':
    main()
