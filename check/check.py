import sys
sys.path.insert(0, '../modules')
from Logger import *
from DBManager import *
from WorkPool import *
from Reader import *

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import pickle
import re

INDEX = 0
TEXT = 1
POLARITY = 2

MIN_DF = 5
MAX_DF = 0.8

l = Logger()
wp = WorkPool()
r = Reader()
db = DBManager()

dataset = None
dataset_fn = []

collection_dump_models_fn_rf = "models_dump_randomforest"
collection_dump_features_fn_rf = "features_dump_randomforest"
collection_dump_models_sa_nb = "models_dump_naivebayse"
collection_dump_features_sa_nb = "features_dump_tfidf_naivebayse"
collection_dump_models_fn_svm = "models_dump_svm_fn"
collection_dump_features_fn_svm = "features_dump_svm_fn"
collection_dump_models_sa_svm = "models_dump_svm_sa"
collection_dump_features_sa_svm = "features_dump_svm_sa"

model_fn_rf = pickle.loads(db.grid_find(collection_dump_models_fn_rf))
vectorizer_fn_rf = pickle.loads(db.grid_find(collection_dump_features_fn_rf))
model_sa_nb = pickle.loads(db.grid_find(collection_dump_models_sa_nb))
vectorizer_sa_nb = pickle.loads(db.grid_find(collection_dump_features_sa_nb))
model_fn_svm = pickle.loads(db.grid_find(collection_dump_models_fn_svm))
vectorizer_fn_svm = pickle.loads(db.grid_find(collection_dump_features_fn_svm))
model_sa_svm = pickle.loads(db.grid_find(collection_dump_models_sa_svm))
vectorizer_sa_svm = pickle.loads(db.grid_find(collection_dump_features_sa_svm))


def do_read():
    global dataset
    l.log(Severity.INFO, "Started reading")
    r.read()
    dataset = r.train + r.test
    l.log(Severity.INFO, "Finished reading")

def do_clean(news):
    l.log(Severity.INFO, "Started cleaning")
    return news.lower()
    l.log(Severity.INFO, "Finished cleaning")

def do_fn_rf(news):
    news = [news.lower()]
    tf_idf = vectorizer_fn_rf.transform(news)
    result = int(model_fn_rf.predict(tf_idf)[0])
    #l.log(Severity.RESULT, "Random Forest - fake news result: class: {0}".format(result))

    if result == 0:
        return "not fake"
    return "fake"

def do_sa_nb(news):
    news = [news.lower()]
    tf_idf = vectorizer_sa_nb.transform(news)
    result = int(model_sa_nb.predict(tf_idf)[0])
    #l.log(Severity.RESULT, "Naive Bayes - sentiment analysis result: class: {0}".format(result))

    if result == 0:
        return "negative"
    elif result == 4:
        return "negative"
    return "neutral"

def do_fn_svm(news):
    news = [news.lower()]
    tf_idf = vectorizer_fn_svm.transform(news)
    result = int(model_fn_svm.predict(tf_idf)[0])
    #l.log(Severity.RESULT, "SVM - fake news result: class: {0}".format(result))

    if result == 0:
        return "not fake"
    return "fake"

def do_sa_svm(news):
    news = [news.lower()]
    tf_idf = vectorizer_sa_svm.transform(news)
    result = int(model_sa_svm.predict(tf_idf)[0])
    #l.log(Severity.RESULT, "SVM - sentiment analysis result: class: {0}".format(result))

    if result == 0:
        return "positive"
    elif result == 4:
        return "negative"
    return "neutral"

count_fake_positive = []
count_fake_negative = []
count_fake_neutral = []
count_not_fake = []

def do_format(key, value):
    to_ret = ""
    to_ret += "\"" + key + "\""
    to_ret += " : "
    to_ret += "\"" + value + "\""

    return str(to_ret)

def do_check(fn, sa, info):
    global dataset, dataset_fn
    l.log(Severity.RESULT, "Results for: " + info)
    count_fn = 0
    count_sa = 0
    for (index, text, polarity) in dataset:
        result = fn(text)
        if result == "fake":
            dataset_fn.append((index, text, polarity))
            count_fn += 1
    
    for (index, text, polarity) in dataset_fn:
        result = sa(text)
        if result == polarity:
            count_sa += 1
    
    
    l.log(Severity.RESULT, "Number of fake news are: {0} and there are {1} news".format(count_fn, len(dataset)))
    l.log(Severity.RESULT, "Accuracy for detecting sentiment analysis on fake news is: {0}, hit: {1}, total: {2}".format(count_sa * 100 / len(dataset_fn), count_sa, len(dataset_fn)))
    

def main():
    do_read()
    do_check(do_fn_rf, do_sa_nb, "FN-RF SA-NB")
    do_check(do_fn_rf, do_sa_svm, "FN-RF SA-SVM")
    do_check(do_fn_svm, do_sa_nb, "FN-SVM SA-NB")
    do_check(do_fn_svm, do_sa_svm, "FN-SVM SA-SVM")
    wp.abort()

if __name__ == "__main__":
    main()